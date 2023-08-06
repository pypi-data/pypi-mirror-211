"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

# from magicgui import magic_factory
from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget

if TYPE_CHECKING:
    import napari  # noqa: F401


class UtilsQWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        btn = QPushButton("Toggle Scalebar Units")
        btn.clicked.connect(self._on_scalebar_click)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(btn)

        # btn = QPushButton("Save Screenshot")
        # btn.clicked.connect(self._screenshot)
        # self.layout().addWidget(btn)

    def _on_scalebar_click(self):
        unit = self.viewer.scale_bar.unit
        if unit == "um":
            self.viewer.scale_bar.unit = ""
            for layer in self.viewer.layers:
                layer.scale = [1, 1, 1]
                self.viewer.reset_view()
        else:
            self.viewer.scale_bar.unit = "um"
            for layer in self.viewer.layers:
                layer.scale = [1, 0.55, 0.55]
                self.viewer.reset_view()

        print("napari has", len(self.viewer.layers), "layers")


# @magic_factory
# def example_magic_widget(img_layer: "napari.layers.Image"):
#    print(f"you have selected {img_layer}")


# Uses the `autogenerate: true` flag in the plugin manifest
# to indicate it should be wrapped as a magicgui to autogenerate
# a widget.
# def example_function_widget(img_layer: "napari.layers.Image"):
#    print(f"you have selected {img_layer}")
