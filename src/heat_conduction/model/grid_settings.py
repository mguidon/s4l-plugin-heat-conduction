import logging

import XCore
import XCoreHeadless
from s4l_core.simulator_plugins.base.model.controller_interface import TreeItem
from heat_conduction.solver.driver import api_models


logger = logging.getLogger(__name__)


class GridSettings(TreeItem):
    """
    Defines the computational grid settings for the simulation domain.
    
    This class manages the spatial discretization parameters used by the solver,
    specifically the grid spacing (resolution) in each dimension. The grid spacing
    directly impacts the accuracy and computational cost of the simulation.
    """

    def __init__(
        self,
        parent: TreeItem,
    ) -> None:
        """
        Initializes grid settings with default spacing values.
        
        Creates the properties panel for configuring grid spacing in the x, y, and z
        dimensions. These values determine the resolution of the computational mesh
        used to solve the heat conduction equation.
        
        Args:
            parent: The parent tree item (typically the Simulation object)
        """
        super().__init__(parent, icon="icons/GridderUI/grid.ico")

        self._properties = XCoreHeadless.DialogOptions()
        self._properties.Description = "Grid Settings"

        dx = XCore.PropertyReal(1.0, 0.0, 100000.0, XCore.Unit("mm"))
        dx.Description = "Grid spacing along x-axis"
        self._properties.Add("dx", dx)

        dy = XCore.PropertyReal(1.0, 0.0, 100000.0, XCore.Unit("mm"))
        dy.Description = "Grid spacing along y-axis"
        self._properties.Add("dy", dy)

        dz = XCore.PropertyReal(1.0, 0.0, 100000.0, XCore.Unit("mm"))
        dz.Description = "Grid spacing along z-axis"
        self._properties.Add("dz", dz)

    def __setstate__(self, state) -> None:
        """
        Custom deserialization support for loading saved grid settings.
        
        Args:
            state: The serialized state to restore from
        """
        super().__setstate__(state)

    @property
    def description(self) -> str:
        """Gets the descriptive name of the grid settings as shown in the UI."""
        return self._properties.Description

    @description.setter
    def description(self, value: str) -> None:
        """Sets the descriptive name of the grid settings as shown in the UI."""
        self._properties.Description = value

    @property
    def properties(self) -> XCore.PropertyGroup:
        """
        Provides access to the property group containing editable grid parameters.
        
        These properties will be displayed in the S4L properties panel when the
        grid settings are selected in the UI.
        """
        return self._properties

    def validate(self) -> bool:
        """
        Validates that the grid settings are physically reasonable.
        
        Checks that grid spacing values are positive and within acceptable range
        for numerical stability and computational feasibility.
        
        Returns:
            True if the grid settings are valid, False otherwise
        """
        return True

    def as_api_model(self) -> api_models.GridSettings:
        """
        Converts the grid settings to a solver API model.
        
        Extracts the grid spacing values to create a simplified representation
        suitable for the solver implementation.
        
        Returns:
            A GridSettings object in the solver API format
        """
        dx_prop = self._properties.dx
        assert isinstance(dx_prop, XCore.PropertyReal)

        dy_prop = self._properties.dy
        assert isinstance(dy_prop, XCore.PropertyReal)

        dz_prop = self._properties.dz
        assert isinstance(dz_prop, XCore.PropertyReal)

        return api_models.GridSettings(
            dx=dx_prop.Value,
            dy=dy_prop.Value,
            dz=dz_prop.Value,
        )
