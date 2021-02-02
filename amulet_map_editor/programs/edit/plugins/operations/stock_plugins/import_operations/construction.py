import os
import wx
from typing import TYPE_CHECKING

from amulet.api.level import Structure
from amulet.api.selection import SelectionGroup
from amulet.api.data_types import Dimension
from amulet.level.formats.construction import ConstructionFormatWrapper

from amulet_map_editor.programs.edit.api.operations import (
    SimpleOperationPanel,
    OperationError,
)

if TYPE_CHECKING:
    from amulet.api.level import BaseLevel
    from amulet_map_editor.programs.edit.api.canvas import EditCanvas


class ImportConstruction(SimpleOperationPanel):
    def __init__(
        self, parent: wx.Window, canvas: "EditCanvas", world: "BaseLevel", options_path: str
    ):
        SimpleOperationPanel.__init__(self, parent, canvas, world, options_path)

        options = self._load_options({})

        self._file_picker = wx.FilePickerCtrl(
            self,
            path=options.get("path", ""),
            wildcard="Construction file (*.construction)|*.construction",
            style=wx.FLP_USE_TEXTCTRL | wx.FLP_OPEN,
        )
        self._sizer.Add(self._file_picker, 0, wx.ALL | wx.CENTER, 5)
        self._add_run_button("Load")
        self.Layout()

    def unload(self):
        self._save_options({"path": self._file_picker.GetPath()})

    def _operation(
        self, world: "BaseLevel", dimension: Dimension, selection: SelectionGroup
    ):
        path = self._file_picker.GetPath()
        if (
            isinstance(path, str)
            and path.endswith(".construction")
            and os.path.isfile(path)
        ):
            wrapper = ConstructionFormatWrapper(path)
            wrapper.translation_manager = world.translation_manager
            self.canvas.paste(Structure(path, wrapper), wrapper.dimensions[0])
        else:
            raise OperationError(
                "Please specify a construction file in the options before running."
            )


export = {
    "name": "\tImport Construction",  # the name of the plugin
    "operation": ImportConstruction,  # the UI class to display
}
