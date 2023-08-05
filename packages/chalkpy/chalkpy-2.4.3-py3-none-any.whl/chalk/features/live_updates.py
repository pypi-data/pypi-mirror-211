from collections import OrderedDict
from typing import Any, Dict, List, Tuple, Type, Union

import cloudpickle

from chalk.utils import notebook
from chalk.utils.log_with_context import get_logger

_logger = get_logger(__name__)

NO_CLIENT_HELPTEXT = """A Chalk client has not yet been initialized in this notebook.
This means that you can create resolvers and features and test them locally, but
they will not be synced to Chalk's servers. To create a client, run the following
in your notebook:

>>> from chalk.client import ChalkClient
>>> client = ChalkClient(branch="my_branch_name")

This will create a Chalk connection pointed at the branch of your choice. New resolvers
or features that you create will be automatically uploaded to that branch. To create a
new branch, use the Chalk CLI:

$ chalk apply --branch my_branch_name
"""

NO_BRANCH_HELPTEXT = """The Chalk client on this notebook does not have a branch set.
Modifications to resolvers or features cannot be uploaded to Chalk until a branch is
specified. You can create a new branch via the Chalk CLI by running:

$ chalk apply --branch my_branch_name

Then, in Python you can point a Chalk client at an existing branch with the following code:

>>> from chalk.client import ChalkClient
>>> client = ChalkClient(branch="my_branch_name")
"""


def _upload_object(obj: Any) -> "UpdatedGraphEntityResponse":
    pickled_obj = cloudpickle.dumps(obj)
    from chalk.client.client_impl import ChalkAPIClientImpl

    client = ChalkAPIClientImpl._latest_client
    if client is None:
        raise RuntimeError(NO_CLIENT_HELPTEXT)
    if client._config.branch is None:
        raise RuntimeError(NO_BRANCH_HELPTEXT)

    resp = client._send_updated_entity(environment=None, pickled_entity=pickled_obj)
    return resp


def _print_responses(responses: List["UpdateGraphEntityResponse"]):
    print(f"Uploaded {len(responses)} resolvers/features to branch server.")
    from chalk.client.models import SingleEntityUpdate

    all_errors = [e for r in responses for e in (r.errors or [])]
    if all_errors:
        for e in all_errors:
            _logger.error(e.message)
        return

    all_updated_objects: List[Tuple[str, SingleEntityUpdate]] = []
    for resp in responses:
        all_updated_objects.extend(("+", o) for o in (resp.added or []))
        all_updated_objects.extend(("*", o) for o in (resp.modified or []))
        all_updated_objects.extend(("-", o) for o in (resp.removed or []))
        all_updated_objects.sort(key=lambda p: p[1].entity_fqn)
    for update_char, update_resp in all_updated_objects:
        if update_resp.entity_fqn.split(".")[-1].startswith("__chalk"):
            continue
        print(f"{update_char}\t{update_resp.entity_type}: {update_resp.entity_fqn}")


def _validate_current_graph() -> List["UpdateGraphError"]:
    # TODO figure out circular imports
    from chalk.features import unwrap_feature
    from chalk.features.feature_set import FeatureSetBase
    from chalk.features.resolver import Resolver
    from chalk.parsed._graph_validation import validate_graph
    from chalk.parsed.duplicate_input_gql import UpsertGraphGQL
    from chalk.parsed.json_conversions import convert_type_to_gql

    resolvers = [convert_type_to_gql(r) for r in Resolver.registry]
    features = []
    for fs in FeatureSetBase.registry.values():
        all_features = [f for f in fs.features if not f.is_autogenerated]
        deduped_features = list({unwrap_feature(f).fqn: f for f in all_features}.values())
        features.extend(convert_type_to_gql(f) for f in deduped_features)
    graph_gql = UpsertGraphGQL(
        resolvers=resolvers,
        features=features,
        # TODO
        config=None,  # load_project_config()
    )
    return validate_graph(graph_gql)


def _remove_object_from_registries(obj: Any):
    """
    If an object fails validation and we keep it registered, all future resolvers/features will cause validation to fail as well.
    """
    from chalk.features.feature_set import FeatureSetBase, is_features_cls
    from chalk.features.resolver import Resolver

    if isinstance(obj, Resolver):
        obj.registry.remove(obj)
    elif is_features_cls(obj):
        FeatureSetBase.registry.pop(obj.namespace)
    else:
        raise ValueError(f"Can't remove object from registry, unrecognized type: {obj}")


def _add_object_to_cache(obj):
    if notebook.is_defined_in_module(obj):
        # If resolver is defined in a module that's imported by a notebook, don't deploy it.
        # This is to avoid re-deploying every feature if customer imports their existing codebase into a notebook.
        return
    from chalk.features.feature_set import is_features_cls
    from chalk.features.resolver import OfflineResolver, OnlineResolver

    if isinstance(obj, (OnlineResolver, OfflineResolver)):
        _UPDATED_RESOLVERS_CACHE[obj.fqn] = obj
    elif is_features_cls(obj):
        _UPDATED_FEATURES_CACHE[obj.namespace] = obj
    else:
        raise ValueError(f"Unsupported entity type: {obj}")


# features.namespace => features
_UPDATED_FEATURES_CACHE: Dict[str, "Features"] = OrderedDict()
# resolver.fqn => resolver
_UPDATED_RESOLVERS_CACHE: Dict[str, Union["OnlineResolver", "OfflineResolver"]] = OrderedDict()


def _clear_entity_update_cache(*_, **__):
    """
    :param _, __: IPython runtime might pass in some objects; ignored
    """
    _UPDATED_RESOLVERS_CACHE.clear()
    _UPDATED_FEATURES_CACHE.clear()


def _deploy_objects(entities: List[Union["Features", "Resolver"]]):
    try:
        # Validation
        from chalk.parsed.duplicate_input_gql import GraphLogSeverity

        if len(errors := _validate_current_graph()) > 0:
            for err in errors:
                _logger.error(f"{err.severity}: {err.subheader}")
            if any(err.severity == GraphLogSeverity.ERROR for err in errors):
                raise ValueError(f"Failed to validate updated graph ({len(errors)} errors).")
        # Upload
        resps = []
        for e in entities:
            resps.append(_upload_object(e))
        _print_responses(resps)
    except Exception as e:
        for obj in entities:
            _remove_object_from_registries(obj)
        _logger.error(f"Failed to upload features/resolvers to branch server: {e}")


def _deploy_objects_from_cache(result: "IPython.ExecutionResult"):
    """
    Runs after a Jupyter cell has finished execution.
    Validates and deploys any new entities defined in the cell to the branch server.
    TODO (rkargon): Currently this uploads objects one at a time.
    This works and should still avoid the forward reference/validation issues in the client.
    :param result: IPython result object.
    """
    if result.error_in_exec is not None:
        return
    if len(_UPDATED_FEATURES_CACHE) == 0 and len(_UPDATED_RESOLVERS_CACHE) == 0:
        return
    _deploy_objects(list(_UPDATED_FEATURES_CACHE.values()) + list(_UPDATED_RESOLVERS_CACHE.values()))
    _clear_entity_update_cache()


def register_cell_hooks_if_in_notebook():
    if not notebook.is_notebook():
        return
    # noinspection PyUnresolvedReferences
    ip = get_ipython()
    ip.events.register(notebook.IPythonEvents.PRE_RUN_CELL.value, _clear_entity_update_cache)
    ip.events.register(notebook.IPythonEvents.POST_RUN_CELL.value, _deploy_objects_from_cache)


register_cell_hooks_if_in_notebook()


def register_live_updates_if_in_notebook(cls: Type):
    """
    This is called manually by the modules containing FeatureSetBase and Resolver due to circular imports
    :param cls:
    :return:
    """
    if notebook.is_notebook():
        setattr(cls, "hook", _add_object_to_cache)
