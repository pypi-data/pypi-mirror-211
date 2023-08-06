"""Existing app extensions to `customize the app <../../how_tos/customize_the_app.html>`__."""


from collections.abc import Mapping
from pathlib import Path

from ._path import DATA_DIRECTORY

_APP_EXTENSIONS_DIRECTORY = DATA_DIRECTORY / "app-extensions"

_ADVANCED_APP_EXTENSION_NAME = "@activeviam/advanced-extension"

ADVANCED_APP_EXTENSION: Mapping[str, Path] = {
    _ADVANCED_APP_EXTENSION_NAME: _APP_EXTENSIONS_DIRECTORY.joinpath(
        *_ADVANCED_APP_EXTENSION_NAME.split("/")
    ),
}
"""The ``{name: path}`` of an app extension providing the following features:

* MDX editor
* Context values editor
* State editor
* Text editor widget

:meta hide-value:
"""
