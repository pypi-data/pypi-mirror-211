"""
This module is an example of a barebones writer plugin for napari.

It implements the Writer specification.
see: https://napari.org/plugins/guides.html?#writers

Replace code below according to your needs.
"""
from __future__ import annotations

import napari
import imageio

from typing import TYPE_CHECKING, Any, List, Sequence, Tuple, Union

if TYPE_CHECKING:
    DataType = Union[Any, Sequence[Any]]
    FullLayerData = Tuple[DataType, dict, str]


def write_single_image(path: str, data: Any, meta: dict):
    """Writes a single image layer"""


def write_multiple(path: str, data: List[FullLayerData]):
    """Writes multiple layers of different types."""
    print('******', path)
    print('******', data)
    return [path]


def write_screenshot(path: str, data: List[FullLayerData]):
    viewer = napari.current_viewer()
    screenshot = viewer.screenshot(scale=4, canvas_only=True)
    imageio.imwrite(path, screenshot)
    print('****', data)
    return [path]
