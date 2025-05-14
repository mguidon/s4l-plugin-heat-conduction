import logging

import XCore
import XCoreHeadless
from s4l_core.simulator_plugins.base.model.controller_interface import TreeItem
from heat_conduction.solver.driver import api_models

logger = logging.getLogger(__name__)


class SetupSettings(TreeItem):
    """
    Manages general simulation setup parameters and preferences.
    
    This class provides control over basic simulation settings such as
    logging verbosity. These settings affect the overall behavior of the
    simulation but are not directly related to the physics being modeled.
    """

    def __init__(
        self,
        parent: TreeItem,
    ) -> None:
        """
        Initializes setup settings with default values.
        
        Creates the properties panel with basic simulation configuration options
        such as logging level for the solver.
        
        Args:
            parent: The parent tree item (typically the Simulation object)
        """
        super().__init__(parent, icon="icons/XSimulatorUI/SetupSettings.ico")

        self._properties = XCoreHeadless.DialogOptions()
        self._properties.Description = "Setup Settings"

        log_level = XCore.PropertyEnum(
            (
                api_models.LogLevel.INFO.value,
                api_models.LogLevel.DEBUG.value,
                api_models.LogLevel.ERROR.value,
            ),
            0,
        )
        log_level.Description = "Solver Log Level"
        self._properties.Add("log_level", log_level)

    def __setstate__(self, state) -> None:
        """
        Custom deserialization support for loading saved setup settings.
        
        Args:
            state: The serialized state to restore from
        """
        super().__setstate__(state)

    @property
    def description(self) -> str:
        """Gets the descriptive name of the setup settings as shown in the UI."""
        return self._properties.Description

    @description.setter
    def description(self, value: str) -> None:
        """Sets the descriptive name of the setup settings as shown in the UI."""
        self._properties.Description = value

    @property
    def properties(self) -> XCore.PropertyGroup:
        """
        Provides access to the property group containing general setup options.
        
        These properties will be displayed in the S4L properties panel when the
        setup settings are selected in the UI.
        """
        return self._properties

    def validate(self) -> bool:
        """
        Validates that the setup settings are properly configured.
        
        Checks that all required settings have valid values for simulation execution.
        
        Returns:
            True if the setup settings are valid, False otherwise
        """
        return True

    def as_api_model(self) -> api_models.SetupSettings:
        """
        Converts the setup settings to a solver API model.
        
        Extracts the configuration values to create a simplified representation
        suitable for the solver implementation.
        
        Returns:
            A SetupSettings object in the solver API format
        """
        log_level_prop = self._properties.log_level
        assert isinstance(log_level_prop, XCore.PropertyEnum)

        return api_models.SetupSettings(
            log_level=log_level_prop.ValueDescription,
        )
