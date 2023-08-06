from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .._java_api import JavaApi
from .._measure_description import MeasureDescription
from .._measure_metadata import MeasureMetadata


@dataclass(eq=False, frozen=True)
class PublishedMeasure(MeasureDescription):  # pylint: disable=keyword-only-dataclass
    _name: str

    def _do_distil(
        self,
        *,
        java_api: JavaApi,  # noqa: ARG002
        cube_name: str,  # noqa: ARG002
        measure_name: Optional[str] = None,  # noqa: ARG002
        measure_metadata: Optional[MeasureMetadata] = None,  # noqa: ARG002
    ) -> str:
        raise RuntimeError("Cannot create a measure that already exists in the cube.")
