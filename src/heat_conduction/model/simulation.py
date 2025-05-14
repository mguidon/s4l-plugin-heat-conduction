import logging
from typing import TYPE_CHECKING
import asyncio

import heat_conduction.model.boundary_settings as boundary_settings
import heat_conduction.model.grid_settings as grid_settings
import heat_conduction.model.material_settings as material_settings
import heat_conduction.model.setup_settings as setup_settings
import heat_conduction.model.solver_settings as solver_settings
import heat_conduction.model.source_settings as source_settings
import XPostProPython as pp
import XCore as xc
from s4l_core.simulator_plugins.base.model.help import create_help_button, display_help
from s4l_core.simulator_plugins.base.model.simulation_base import SimulationBase
from s4l_core.simulator_plugins.base.solver.project_runner import SolverBackend, config_type_t
from heat_conduction.solver.driver import api_models

if TYPE_CHECKING:
    from s4l_core.simulator_plugins.base.model.controller_interface import TreeItem

logger = logging.getLogger(__name__)

domain_id_map_t = dict[str, int]  # map from uuid (as str) to the domain id


class Simulation(SimulationBase):
    """
    Central model class representing a Heat Conduction simulation.
    
    This class serves as the main container for all simulation settings and components,
    including setup parameters, material properties, sources, boundary conditions,
    grid settings, and solver parameters. It provides methods for validating the simulation
    configuration and converting the model to a format suitable for the solver.
    """

    @classmethod
    def get_simulation_type_name(cls) -> str:
        """
        Returns the display name used to identify this simulation type in the S4L interface.
        
        This name appears in the UI when users are selecting which type of simulation to create.
        """
        return "Heat Conduction"

    @classmethod
    def get_simulation_description(cls) -> str:
        """
        Returns a brief description of what this simulation type does.
        
        This description appears in the UI to help users understand the purpose of this
        simulation type.
        """
        return "A simulation plugin for S4L"

    @classmethod
    def get_simulation_icon(cls) -> str:
        """
        Returns the path to the icon used to represent this simulation type in the UI.
        """
        return "icons/XSimulatorUI/new_simulation.ico"

    def __init__(
        self,
        parent: "TreeItem",
        sim_desc: str = "Simulation",
        sim_notes: str = "Solves ∇·(k∇T) + Q = 0",
    ) -> None:
        """
        Initializes a new simulation instance with default settings.
        
        Creates a help button in the properties panel and schedules the connection
        of the help button event handler.
        
        Args:
            parent: The parent tree item
            sim_desc: A brief description of this specific simulation instance
            sim_notes: Additional notes about this simulation (default shows the equation)
        """
        super().__init__(parent, sim_desc, sim_notes)

        self._properties.Add("help_button", create_help_button())

        asyncio.get_event_loop().call_soon(self._connect_help)

    def on_initialize_settings(self) -> None:
        """
        Creates all the settings objects for this simulation.
        
        This method is called during initialization to set up the various settings 
        components that make up the simulation (setup, materials, sources, boundaries, etc.).
        Each component is responsible for a specific aspect of the simulation configuration.
        """
        self._setup_settings = setup_settings.SetupSettings(self)
        self._material_settings: "material_settings.Materials" = (
            material_settings.Materials(self)
        )
        self._source_settings = source_settings.Sources(self)
        self._boundary_settings = boundary_settings.Boundaries(self)
        self._grid_settings = grid_settings.GridSettings(self)
        self._solver_settings = solver_settings.SolverSettings(self)

    def _connect_help(self):
        """
        Connects the help button click event to the help display handler.
        
        This method is scheduled to run soon after initialization to ensure the
        help button property is properly set up before connecting the event handler.
        """
        help_button = self._properties.help_button
        assert isinstance(help_button, xc.PropertyPushButton)
        help_button.OnClicked.Connect(self._display_help)

    def _display_help(self) -> None:
        """
        Displays help information about this simulation type when the help button is clicked.
        
        Shows a dialog with the simulation type title and a basic description of what
        the simulation does and how it works.
        """
        sim_type = "Heat Conduction"
        title = f"{sim_type} Simulation"
        text = (
            f"This simulation solves the {sim_type} equation using finite difference methods."
            "\n\n"
            "For more information, please refer to the documentation."
        )
        display_help(title, text)

    @property
    def setup_settings(self) -> setup_settings.SetupSettings:
        return self._setup_settings

    @property
    def material_settings(self) -> material_settings.Materials:
        return self._material_settings

    @property
    def source_setings(self) -> source_settings.Sources:
        return self._source_settings

    @property
    def boundary_settings(self) -> boundary_settings.Boundaries:
        return self._boundary_settings

    @property
    def grid_settings(self) -> grid_settings.GridSettings:
        return self._grid_settings

    @property
    def solver_settings(self) -> solver_settings.SolverSettings:
        return self._solver_settings

    def register_extractor(self) -> pp.PythonModuleAlgorithm:
        """
        Registers a post-processing extractor for simulation results.
        
        This method is called by the S4L framework to set up result extraction and
        visualization capabilities for this simulation type.
        
        Returns:
            A PostPro algorithm that can extract and process simulation results
        """
        return pp.PythonModuleAlgorithm(
            "heat_conduction.model.simulation_extractor",
            0,
            1,
        )

    def solver_backend(self) -> tuple[SolverBackend, config_type_t | None]:
        """
        Specifies which type of solver backend to use for running this simulation.
        
        This method determines how the solver will be executed (as a process, thread, etc.)
        and any configuration needed for that execution mode.
        
        Returns:
            A tuple containing the solver backend type and optional configuration
        """
        return SolverBackend.PROCESS, None
    
    def get_solver_src(self) -> str:
        """
        Returns the Python module path to the solver implementation.
        
        The S4L framework uses this to locate and load the solver code when
        running a simulation of this type.
        
        Returns:
            The fully qualified module name for the solver implementation
        """
        return "heat_conduction.solver.driver"

    def clear_status_recursively(self) -> None:
        """
        Clears status indicators for this simulation and its components.
        
        This method is typically called before validation to ensure a clean
        slate for reporting validation issues.
        """
        super().clear_status_recursively()
        self.solver_settings.clear_status()

    def validate(self) -> bool:
        """
        Validates that the simulation configuration is complete and ready to run.
        
        Performs checks to ensure all required settings are provided and within
        acceptable ranges. Sets status indicators to highlight any issues found.
        
        Returns:
            True if the simulation is valid and ready to run, False otherwise
        """
        self.clear_status_recursively()
        self.boundary_settings.clear_status_recursively()
        ok = True
        if len(self.boundary_settings.elements) == 0:
            self.boundary_settings.status_icons = [
                "icons/TaskManager/Warning.ico",
            ]
            self.boundary_settings.status_icons_tooltip = "No boundaries defined"
            ok = False

        return ok

    def as_api_model(self) -> api_models.Simulation:
        """
        Converts the simulation model to a format suitable for the solver API.
        
        This method transforms the UI-oriented model objects into a simplified
        representation that can be passed to the simulation solver. It validates
        the simulation first to ensure it is ready to run.
        
        Returns:
            A solver API model representation of this simulation
            
        Raises:
            RuntimeError: If validation fails
        """
        if not self.validate():
            raise RuntimeError("Validation failed")

        api_materials: list[api_models.MaterialSettings] = []
        for material in self._material_settings.elements:
            api_materials.append(material.as_api_model())

        api_sources: list[api_models.SourceSettings] = []
        for source in self._source_settings.elements:
            api_sources.append(source.as_api_model())

        api_boundaries: list[api_models.BoundarySettings] = []
        for boundary in self._boundary_settings.elements:
            api_boundaries.append(boundary.as_api_model())

        return api_models.Simulation(
            setup_settings=self._setup_settings.as_api_model(),
            material_settings=api_materials,
            source_setings=api_sources,
            boundary_settings=api_boundaries,
            grid_settings=self._grid_settings.as_api_model(),
            solver_settings=self._solver_settings.as_api_model(),
        )
