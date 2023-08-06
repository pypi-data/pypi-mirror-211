from collections.abc import Iterable, Mapping
from typing import Optional

from atoti_core import DelegateMutableMapping

from ._java_api import JavaApi
from .aggregate_provider import AggregateProvider


class AggregateProviders(DelegateMutableMapping[str, AggregateProvider]):
    def __init__(
        self,
        *,
        cube_name: str,
        java_api: JavaApi,
    ):
        self._cube_name = cube_name
        self._java_api = java_api

    def _delete_keys(self, keys: Optional[Iterable[str]] = None, /) -> None:
        self._java_api.remove_aggregate_providers(keys, cube_name=self._cube_name)
        self._java_api.refresh()

    def _update(self, other: Mapping[str, AggregateProvider], /) -> None:
        self._java_api.add_aggregate_providers(other, cube_name=self._cube_name)
        self._java_api.refresh()

    def _get_underlying(self) -> dict[str, AggregateProvider]:
        return self._java_api.get_aggregate_providers_attributes(self._cube_name)
