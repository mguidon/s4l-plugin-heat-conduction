import logging
from typing import TYPE_CHECKING, Any, cast

import s4l_core.simulator_plugins.base.model.geometry as geometry
import heat_conduction.model.boundary_settings as boundary_settings
import heat_conduction.model.grid_settings as grid_settings
import heat_conduction.model.material_settings as material_settings
import heat_conduction.model.simulation as sim
import heat_conduction.model.setup_settings as setup_settings
import heat_conduction.model.solver_settings as solver_settings
import heat_conduction.model.source_settings as source_settings
import XController
import XCoreHeadless
from s4l_core.simulator_plugins.base.controller.simulation_manager_interface import (
    ISimulationManager,
)

if TYPE_CHECKING:
    from s4l_core.simulator_plugins.base.model.controller_interface import TreeItem

logger = logging.getLogger(__name__)


class SimulationManager(ISimulationManager):
    """Manager implementation that handles UI interactions and property display for the simulation.
    
    This class is responsible for creating and managing UI actions, handling user selections,
    and displaying appropriate properties in the property panel based on the selected simulation
    components.
    """

    def __init__(self, simulation: sim.Simulation):
        """
        Initializes the simulation manager with UI actions for manipulating simulation components.
        
        Creates action buttons for adding materials, sources, and boundaries to the simulation,
        which will appear in the S4L interface when appropriate items are selected.
        
        Args:
            simulation: The simulation model instance to manage
        """
        super().__init__(simulation)

        self._new_material_action = XController.Action(
            "Material",
            "Add new material property",
            XController.Icon("icons/XPostProcessor/PhysicalScalarQuantity.ico"),
        )
        self._new_material_action.OnTriggered.Connect(self.on_new_material_triggered)

        self._new_source_action = XController.Action(
            "Source",
            "Add new sources property",
            XController.Icon("icons/XPostProcessor/PhysicalScalarQuantity.ico"),
        )
        self._new_source_action.OnTriggered.Connect(self.on_new_source_triggered)

        self._new_boundary_action = XController.Action(
            "Boundary",
            "Add new boundary property",
            XController.Icon("icons/XPostProcessor/PhysicalScalarQuantity.ico"),
        )
        self._new_boundary_action.OnTriggered.Connect(self.on_new_boundary_triggered)

    @property
    def simulation(self) -> sim.Simulation:
        return cast("sim.Simulation", self._simulation)

    def collect_actions(self, selection: Any) -> list[XController.Action]:
        """
        Provides appropriate UI actions based on the current user selection in the UI.
        
        Determines which action buttons should be enabled based on the currently selected
        item in the simulation tree, then returns all available actions for the S4L
        interface to display.

        Args:
            selection: Currently selected items in the S4L UI

        Returns:
            List of actions that should be available for the current selection
        """

        self._new_material_action.Enabled = (
            len(selection) == 1 and len(selection[0].Path()) > 1
        )
        self._new_source_action.Enabled = (
            len(selection) == 1 and len(selection[0].Path()) > 1
        )
        self._new_boundary_action.Enabled = (
            len(selection) == 1 and len(selection[0].Path()) > 1
        )

        return [
            self._new_material_action,
            self._new_source_action,
            self._new_boundary_action,
        ]

    def update_properties(
        self,
        properties_registry: XCoreHeadless.PropertyRegistry,
        selected_item: "TreeItem",
        parent_item: "TreeItem | None",
    ) -> None:
        """
        Updates the property panel in the UI based on the selected simulation component.
        
        When a user selects an item in the simulation tree, this method determines what
        properties should be displayed for editing in the properties panel. Different
        simulation components (materials, sources, etc.) have different property sets.

        Args:
            properties_registry: Registry to populate with properties
            selected_item: The currently selected tree item
            parent_item: The parent of the selected tree item, if any
        """
        # Handle Settings
        if isinstance(
            selected_item,
            (
                setup_settings.SetupSettings,
                material_settings.MaterialSettings,
                source_settings.SourceSettings,
                boundary_settings.BoundarySettings,
                grid_settings.GridSettings,
                solver_settings.SolverSettings,
                sim.Simulation,
            ),
        ):
            properties_registry.SetProperties([selected_item.properties])
            return

        # Handle Geometries -> Show properties of the parent item
        if isinstance(selected_item, geometry.Geometry):
            if isinstance(
                parent_item,
                (
                    material_settings.MaterialSettings,
                    source_settings.SourceSettings,
                    boundary_settings.BoundarySettings,
                ),
            ):
                properties_registry.SetProperties([parent_item.properties])
                return

        # For any other items, clear properties
        properties_registry.SetProperties([])

    def on_new_material_triggered(self) -> None:
        self.simulation.material_settings.add(material_settings.MaterialSettings)

    def on_new_source_triggered(self) -> None:
        self.simulation.source_setings.add(source_settings.SourceSettings)

    def on_new_boundary_triggered(self) -> None:
        self.simulation.boundary_settings.add(boundary_settings.BoundarySettings)
