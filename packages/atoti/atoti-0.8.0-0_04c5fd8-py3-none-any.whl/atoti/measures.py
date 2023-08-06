from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
    overload,
)

from typeguard import typeguard_ignore

from ._java_api import JavaApi
from ._local_measures import LocalMeasures
from ._measure_convertible import MeasureConvertible
from ._measure_definition import MeasureDefinition, get_measure_convertible_and_metadata
from ._measure_description import MeasureDescription, convert_to_measure_description
from ._measure_metadata import MeasureMetadata
from .measure import Measure

if TYPE_CHECKING:
    from _typeshed import SupportsKeysAndGetItem  # pylint: disable=nested-import


def _validate_name(name: str, /) -> None:
    if "," in name:
        raise ValueError(f'Invalid measure name "{name}". "," are not allowed.')
    if name != name.strip():
        raise ValueError(
            f'Invalid measure name "{name}". Leading or trailing whitespaces are not allowed.'
        )
    if name.startswith("__hidden_"):
        raise ValueError(
            f'Invalid measure name "{name}". Name cannot start with "__hidden_".'
        )


class Measures(LocalMeasures[Measure]):
    """Manage the measures of a cube.

    The built-in measure :guilabel:`contributors.COUNT` indicates how many rows from the cube's base table took part in each aggregate of a query:

    Example:
        >>> df = pd.DataFrame(
        ...     columns=["City", "Price"],
        ...     data=[
        ...         ("London", 240.0),
        ...         ("New York", 270.0),
        ...         ("Paris", 200.0),
        ...     ],
        ... )
        >>> table = session.read_pandas(
        ...     df, keys=["City"], table_name="Built-in measures"
        ... )
        >>> cube = session.create_cube(table)
        >>> l, m = cube.levels, cube.measures
        >>> cube.query(m["contributors.COUNT"])
          contributors.COUNT
        0                  3
        >>> cube.query(m["contributors.COUNT"], levels=[l["City"]])
                 contributors.COUNT
        City
        London                    1
        New York                  1
        Paris                     1

    The caption of this measure can be changed with an :class:`~atoti.I18nConfig`.
    """

    def __init__(
        self,
        *,
        cube_name: str,
        java_api: JavaApi,
    ):
        super().__init__(java_api=java_api)

        self._cube_name = cube_name

    @typeguard_ignore
    def _build_measure(
        self, name: str, description: JavaApi.JavaMeasureDescription
    ) -> Measure:
        return Measure(
            name,
            cube_name=self._cube_name,
            data_type=description.underlying_type,
            description=description.description,
            folder=description.folder,
            formatter=description.formatter,
            java_api=self._java_api,
            visible=description.visible,
        )

    def _get_underlying(self) -> dict[str, Measure]:
        """Fetch the measures from the JVM each time they are needed."""
        cube_measures = self._java_api.get_measures(self._cube_name)
        return {
            name: self._build_measure(name, cube_measures[name])
            for name in cube_measures
        }

    def __getitem__(self, key: str, /) -> Measure:
        cube_measure = self._java_api.get_measure(key, cube_name=self._cube_name)
        return self._build_measure(key, cube_measure)

    # Custom override with same value type as the one used in `update()`.
    def __setitem__(self, key: str, value: MeasureConvertible, /) -> None:
        self.update({key: value})

    @overload
    def update(
        self,
        __m: SupportsKeysAndGetItem[str, MeasureDefinition],
        **kwargs: MeasureDefinition,
    ) -> None:
        ...

    @overload
    def update(
        self,
        __m: Iterable[tuple[str, MeasureDefinition]],
        **kwargs: MeasureDefinition,
    ) -> None:
        ...

    @overload
    def update(self, **kwargs: MeasureDefinition) -> None:
        ...

    # Custom override types on purpose so that measure convertible objects can be inserted.
    def update(  # type: ignore[misc] # pyright: ignore[reportGeneralTypeIssues]
        self,
        __m: Optional[
            Union[
                Mapping[str, MeasureDefinition],
                Iterable[tuple[str, MeasureDefinition]],
            ]
        ] = None,
        **kwargs: MeasureDefinition,
    ) -> None:
        other: dict[str, MeasureDefinition] = {}

        if __m is not None:
            other.update(__m)
        other.update(**kwargs)

        self._update(
            {
                measure_name: get_measure_convertible_and_metadata(measure_definition)
                for measure_name, measure_definition in other.items()
            }
        )

    # Custom override types on purpose so that measure-like objects can be inserted.
    def _update(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        other: Mapping[str, tuple[MeasureConvertible, MeasureMetadata]],  # type: ignore[override]
    ) -> None:
        for measure_name, (
            measure,
            measure_metadata,
        ) in other.items():
            _validate_name(measure_name)

            if not isinstance(measure, MeasureDescription):
                measure = convert_to_measure_description(measure)  # noqa: PLW2901

            try:
                measure._distil(
                    java_api=self._java_api,
                    cube_name=self._cube_name,
                    measure_name=measure_name,
                    measure_metadata=measure_metadata,
                )
            except AttributeError as err:
                raise ValueError(f"Cannot create a measure from {measure}") from err

        self._java_api.publish_measures(self._cube_name)

    def _delete_keys(self, keys: Optional[Iterable[str]] = None, /) -> None:
        keys = self._default_to_all_keys(keys)
        for key in keys:
            self._java_api.delete_measure(key, cube_name=self._cube_name)
