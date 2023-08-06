from abc import abstractmethod
from collections.abc import Mapping
from typing import Protocol, TypeVar, Union

from atoti_core import BaseHierarchies, BaseHierarchyBound, DelegateMutableMapping

from ._hierarchy_arguments import HierarchyArguments
from ._java_api import JavaApi
from .column import Column
from .level import Level

LevelOrColumn = Union[Level, Column]

_HierarchyT = TypeVar("_HierarchyT", bound=BaseHierarchyBound, covariant=True)


class CreateHierarchyFromArguments(Protocol[_HierarchyT]):
    def __call__(self, arguments: HierarchyArguments, /) -> _HierarchyT:
        ...


class LocalHierarchies(  # type: ignore[misc,type-var]
    DelegateMutableMapping[
        tuple[str, str],
        _HierarchyT,  # pyright: ignore[reportGeneralTypeIssues]
    ],
    BaseHierarchies[_HierarchyT],
):
    """Local hierarchies class."""

    def __init__(
        self,
        *,
        create_hierarchy_from_arguments: CreateHierarchyFromArguments[_HierarchyT],
        java_api: JavaApi,
    ) -> None:
        super().__init__()

        self._create_hierarchy_from_arguments = create_hierarchy_from_arguments
        self._java_api = java_api

    @abstractmethod
    def _get_underlying(self) -> dict[tuple[str, str], _HierarchyT]:
        """Fetch the hierarchies from the JVM each time they are needed."""

    def _update(
        self,
        other: Mapping[tuple[str, str], _HierarchyT],  # noqa: ARG002
        /,
    ) -> None:
        raise AssertionError(f"{self._get_name()} cube hierarchies cannot be changed.")

    def _get_name(self) -> str:
        return self.__class__.__name__.replace("Hierarchies", "")
