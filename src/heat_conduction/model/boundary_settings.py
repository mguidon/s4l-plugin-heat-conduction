import logging

import XCore
import XCoreHeadless
from s4l_core.simulator_plugins.base.model.controller_interface import TreeItem
from s4l_core.simulator_plugins.base.model.group import Group
from heat_conduction.solver.driver import api_models

logger = logging.getLogger(__name__)


class BoundarySettings(TreeItem):
    def __init__(
        self,
        parent: TreeItem,
    ) -> None:
        super().__init__(parent, icon="icons/XSimulatorUI/BoundarySettings.ico")

        self._properties = XCoreHeadless.DialogOptions()
        self._properties.Description = "Boundary Settings"

        face = XCore.PropertyEnum(
            (
                api_models.DirichletFace.XMIN.value,
                api_models.DirichletFace.XMAX.value,
                api_models.DirichletFace.YMIN.value,
                api_models.DirichletFace.YMAX.value,
                api_models.DirichletFace.ZMIN.value,
                api_models.DirichletFace.ZMAX.value,
            ),
            0,
        )
        face.Description = "Boundary Face"
        self._properties.Add("face", face)

        temperature = XCore.PropertyReal(0.0, 0.0, 100000.0, XCore.Unit("K"))
        temperature.Description = "Prescribed Temperature"
        self._properties.Add("temperature", temperature)

    def __setstate__(self, state) -> None:
        super().__setstate__(state)

    @property
    def description(self) -> str:
        return self._properties.Description

    @description.setter
    def description(self, value: str) -> None:
        self._properties.Description = value

    @property
    def properties(self) -> XCore.PropertyGroup:
        return self._properties

    def validate(self) -> bool:
        return True

    def clear_status_recursively(self):
        self.clear_status()

    def as_api_model(self) -> api_models.BoundarySettings:
        face_prop = self._properties.face
        assert isinstance(face_prop, XCore.PropertyEnum)

        temperature_prop = self._properties.temperature
        assert isinstance(temperature_prop, XCore.PropertyReal)

        return api_models.BoundarySettings(
            face=face_prop.ValueDescription, temperature=temperature_prop.Value
        )


class Boundaries(Group[BoundarySettings]):
    def __init__(
        self, parent: TreeItem, is_expanded: bool = True, icon: str = ""
    ) -> None:
        super().__init__(
            parent,
            BoundarySettings,
            is_expanded,
            icon="icons/XSimulatorUI/BoundarySettings.ico",
        )

    def _get_new_element_description(self) -> str:
        return "Boundary"

    def clear_status_recursively(self):
        self.clear_status()
        for mat in self._elements:
            mat.clear_status_recursively()

    @property
    def description_text(self) -> str:
        return "Boundaries"
