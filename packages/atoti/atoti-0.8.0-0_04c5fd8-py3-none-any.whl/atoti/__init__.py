# ruff: noqa: E402

import sys

from atoti_core import BaseSession

from ._runtime_type_checking_utils import _instrument_typechecking, typecheck

# This needs to be done here so that the runtime type checking decoration can be done before evaluating any classes inheriting from `BaseSession`.
# Otherwise the monkey-patching mechanism used by plugins will target the incorrect method references.
if __debug__:
    typecheck(BaseSession)

from atoti_query import (
    Auth as Auth,
    BasicAuthentication as BasicAuthentication,
    ClientCertificate as ClientCertificate,
    OAuth2ResourceOwnerPasswordAuthentication as OAuth2ResourceOwnerPasswordAuthentication,
    QueryCube as QueryCube,
    QueryHierarchy as QueryHierarchy,
    QueryLevel as QueryLevel,
    QueryMeasure as QueryMeasure,
    QueryResult as QueryResult,
    QuerySession as QuerySession,
    TokenAuthentication as TokenAuthentication,
)

from . import (  # noqa: A001
    agg as agg,
    array as array,
    experimental as experimental,
    math as math,
    scope as scope,
    string as string,
    type as type,
)
from ._condition_to_json_serializable_dict import *
from ._eula import (  # noqa: N811
    EULA as __license__,  # noqa: F401
    hide_new_eula_message as hide_new_eula_message,
    print_eula_message,
)
from ._measure_metadata import *
from ._py4j_utils import patch_databricks_py4j
from ._telemetry import telemeter
from ._user_service_client import UserServiceClient as UserServiceClient
from .aggregate_provider import AggregateProvider as AggregateProvider
from .app_extension import *
from .client_side_encryption_config import *
from .column import *
from .config import *
from .cube import Cube as Cube
from .directquery import *
from .function import *
from .hierarchy import *
from .level import *
from .measure import *
from .order import *

# Replace imported symbols with `*` once the deprecated scope factory functions are removed.
from .scope import (
    CumulativeScope as CumulativeScope,
    OriginScope as OriginScope,
    SiblingsScope as SiblingsScope,
)
from .session import Session as Session, _sessions as sessions
from .table import Table as Table
from .type import *

print_eula_message()


def close() -> None:
    """Close all opened sessions."""
    sessions.close()


if __debug__:
    _instrument_typechecking(sys.modules[__name__])

patch_databricks_py4j()
telemeter()
