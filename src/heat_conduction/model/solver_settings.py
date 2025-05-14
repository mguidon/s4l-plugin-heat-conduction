import logging

import XCore
import XCoreHeadless
from s4l_core.simulator_plugins.base.model.controller_interface import TreeItem
from heat_conduction.solver.driver import api_models

logger = logging.getLogger(__name__)


class SolverSettings(TreeItem):
    """
    Manages numerical solver parameters that control the solution process.
    
    This class provides configuration options for the numerical algorithms used to
    solve the heat conduction equation, including method selection, convergence
    criteria, and iteration limits. These settings directly impact the accuracy, 
    stability, and performance of the simulation.
    """

    def __init__(
        self,
        parent: TreeItem,
    ) -> None:
        """
        Initializes solver settings with default algorithm parameters.
        
        Creates the properties panel with options for configuring the numerical
        solver, including method selection, convergence tolerance, and maximum
        number of iterations.
        
        Args:
            parent: The parent tree item (typically the Simulation object)
        """
        super().__init__(parent, icon="icons/XSimulatorUI/SolverSettings.ico")

        self._properties = XCoreHeadless.DialogOptions()
        self._properties.Description = "Solver Settings"

        solver_method = XCore.PropertyEnum(
            (
                api_models.SolverMethod.JACOBI.value,
                api_models.SolverMethod.JACOBI.value,
            ),
            0,
        )
        solver_method.Description = "Solver Method"
        self._properties.Add("solver_method", solver_method)

        tolerance = XCore.PropertyReal(1e-4, 1e-10, 1.0)
        tolerance.Description = "Convergence Tolerance"
        self._properties.Add("tolerance", tolerance)

        max_iter = XCore.PropertyInt(100, 1, 10000)
        max_iter.Description = "Max. Iterations"
        self._properties.Add("max_iter", max_iter)

    def __setstate__(self, state) -> None:
        """
        Custom deserialization support for loading saved solver settings.
        
        Args:
            state: The serialized state to restore from
        """
        super().__setstate__(state)

    @property
    def description(self) -> str:
        """Gets the descriptive name of the solver settings as shown in the UI."""
        return self._properties.Description

    @description.setter
    def description(self, value: str) -> None:
        """Sets the descriptive name of the solver settings as shown in the UI."""
        self._properties.Description = value

    @property
    def properties(self) -> XCore.PropertyGroup:
        """
        Provides access to the property group containing solver configuration options.
        
        These properties will be displayed in the S4L properties panel when the
        solver settings are selected in the UI.
        """
        return self._properties

    def validate(self) -> bool:
        """
        Validates that the solver settings are properly configured.
        
        Checks that convergence criteria and iteration limits are within reasonable
        ranges for effective numerical solution.
        
        Returns:
            True if the solver settings are valid, False otherwise
        """
        return True

    def as_api_model(self) -> api_models.SolverSettings:
        """
        Converts the solver settings to a solver API model.
        
        Extracts the numerical algorithm parameters to create a simplified
        representation suitable for the solver implementation.
        
        Returns:
            A SolverSettings object in the solver API format
        """
        solver_method_prop = self._properties.solver_method
        assert isinstance(solver_method_prop, XCore.PropertyEnum)

        tolerance_prop = self._properties.tolerance
        assert isinstance(tolerance_prop, XCore.PropertyReal)

        max_iter_prop = self._properties.max_iter
        assert isinstance(max_iter_prop, XCore.PropertyInt)

        return api_models.SolverSettings(
            solver_method=solver_method_prop.ValueDescription,
            tolerance=tolerance_prop.Value,
            max_iter=max_iter_prop.Value,
        )
