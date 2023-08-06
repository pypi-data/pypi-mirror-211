from dataclasses import dataclass
from itertools import chain
from typing import Optional

from atoti_core import (
    Coordinates,
    CoordinatesT,
    Operand,
    Operation,
    keyword_only_dataclass,
)


@keyword_only_dataclass
@dataclass(eq=False, frozen=True)
class FunctionOperation(Operation[CoordinatesT]):
    function_key: str
    operands: tuple[Optional[Operand[CoordinatesT]], ...] = ()

    @property
    def _coordinates_classes(self) -> frozenset[type[Coordinates]]:
        return frozenset(
            chain(
                *(self._get_coordinates_classes(operand) for operand in self.operands)
            )
        )
