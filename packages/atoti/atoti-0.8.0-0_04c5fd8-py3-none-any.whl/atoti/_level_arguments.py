from atoti_core import ColumnCoordinates

from .order._order import Order
from .type import DataType

LevelArguments = tuple[str, ColumnCoordinates, DataType, Order]
