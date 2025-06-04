import logging
from typing import TYPE_CHECKING

import XCore
import XCoreHeadless
import XCoreModeling as xm
from s4l_core.simulator_plugins.base.model.geometry_interface import HasGeometries
from s4l_core.simulator_plugins.base.model.group import Group
from heat_conduction.solver.driver import api_models

if TYPE_CHECKING:
    from s4l_core.simulator_plugins.base.model.controller_interface import TreeItem


logger = logging.getLogger(__name__)


class SourceSettings(HasGeometries):
    """
    Defines heat source properties that introduce energy into the simulation domain.
    
    This class represents a volumetric heat source with a specific power density that
    can be placed at specific locations in the simulation. Heat sources act as energy
    inputs to the system, creating temperature gradients that drive heat conduction.
    """

    def __init__(
        self,
        parent: "TreeItem",
    ) -> None:
        """
        Initializes a heat source with default properties.
        
        Creates the properties panel for configuring the volumetric heat source
        power density. Heat sources are associated with geometric points (vertices)
        to specify their location in the simulation domain.
        
        Args:
            parent: The parent tree item (typically the Sources collection)
        """
        allowed_types = self._get_allowed_entity_types()

        super().__init__(
            parent=parent,
            icon="icons/EmFdtdSimulatorUI/semx_pointsensor.ico",
            allowed_entity_types=allowed_types,
        )

        self._properties = XCoreHeadless.DialogOptions()
        self._properties.Description = "Source Settings"

        volumetric_heat_source = XCore.PropertyReal(100.0, 0.0, 0.0, XCore.Unit("W/m³"))
        volumetric_heat_source.Description = "Volumetric Heat Source"
        self._properties.Add("volumetric_heat_source", volumetric_heat_source)

    def _get_allowed_entity_types(self) -> tuple[type[xm.Entity], ...]:
        """
        Specifies which types of geometric entities can have heat sources assigned to them.
        
        In this simulation, heat sources can only be assigned to point entities (vertices),
        as they represent localized heat generation points in the domain.
        
        Returns:
            Tuple of allowed entity types (only Vertex objects in this case)
        """
        return (xm.Vertex,)

    def __setstate__(self, state) -> None:
        """
        Custom deserialization support for loading saved source settings.
        
        Args:
            state: The serialized state to restore from
        """
        super().__setstate__(state)

    @property
    def description(self) -> str:
        """Gets the descriptive name of this heat source as shown in the UI."""
        return self._properties.Description

    @description.setter
    def description(self, value: str) -> None:
        """Sets the descriptive name of this heat source as shown in the UI."""
        self._properties.Description = value

    @property
    def properties(self) -> XCore.PropertyGroup:
        """
        Provides access to the property group containing heat source parameters.
        
        These properties will be displayed in the S4L properties panel when this
        heat source is selected in the UI.
        """
        return self._properties

    def validate(self) -> bool:
        """
        Validates that the heat source settings are complete and physically meaningful.
        
        Checks that the source is associated with exactly one geometric vertex and
        that the power density is non-negative.
        
        Returns:
            True if the heat source settings are valid, False otherwise
        """
        if not len(self._geometries) == 1:
            return False

        return True

    def clear_status_recursively(self):
        """Clears any status indicators for this heat source."""
        self.clear_status()

    def as_api_model(self) -> api_models.SourceSettings:
        """
        Converts this heat source settings object to a solver API model.
        
        Extracts the volumetric heat source power density and the position of
        the associated vertex to create a simplified representation suitable
        for the solver.
        
        Returns:
            A SourceSettings object in the solver API format
        """
        volumetric_heat_source_prop = self._properties.volumetric_heat_source
        assert isinstance(volumetric_heat_source_prop, XCore.PropertyReal)

        assert len(self._geometries) == 1

        point = self._geometries[0].entity

        points = xm.GetVertices(point)

        assert len(points)
        point = points[0]
        assert isinstance(point, xm.Vertex)

        return api_models.SourceSettings(
            volumetric_heat_source=volumetric_heat_source_prop.Value,
            x=point.Position[0],
            y=point.Position[1],
            z=point.Position[2],
        )


class Sources(Group[SourceSettings]):
    """
    Collection class that manages a group of SourceSettings objects.
    
    This class provides functionality for adding, removing, and accessing
    individual heat sources. It appears in the simulation tree as the
    "Sources" node, which can be expanded to show individual heat sources.
    """

    def __init__(
        self, parent: "TreeItem", is_expanded: bool = True, icon: str = ""
    ) -> None:
        """
        Initializes a new heat sources collection.
        
        Args:
            parent: The parent tree item (typically the Simulation object)
            is_expanded: Whether the sources node starts expanded in the UI tree
            icon: Optional custom icon path (defaults to standard sources icon)
        """
        super().__init__(
            parent,
            SourceSettings,
            is_expanded,
            icon="icons/EmFdtdSimulatorUI/semx_pointsensor.ico",
        )

    def _get_new_element_description(self) -> str:
        """
        Provides the base name used when creating new heat source elements.
        
        Returns:
            The base description string used for new heat sources
        """
        return "Source"

    def clear_status_recursively(self):
        """
        Clears status indicators for this collection and all contained heat sources.
        
        This method is called before validation to ensure a clean slate for
        reporting any validation issues.
        """
        self.clear_status()
        for mat in self._elements:
            mat.clear_status_recursively()

    @property
    def description_text(self) -> str:
        """
        Gets the display text for this collection shown in the simulation tree.
        
        Returns:
            The plural form of the element type (e.g., "Sources")
        """
        return f"Sources"
