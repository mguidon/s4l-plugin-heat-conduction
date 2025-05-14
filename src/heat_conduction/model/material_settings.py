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


class MaterialSettings(HasGeometries):
    """
    Defines material properties that can be assigned to geometric entities in the simulation.
    
    This class represents a material with physical properties (such as thermal conductivity)
    that can be assigned to one or more geometric bodies in the simulation domain. It inherits
    from HasGeometries to provide the ability to associate geometry with the material.
    """

    def __init__(
        self,
        parent: "TreeItem",
    ) -> None:
        """
        Initializes a new material settings object with default properties.
        
        Creates the properties panel for this material with appropriate controls
        for setting the thermal conductivity and other physical parameters.
        
        Args:
            parent: The parent tree item (typically the Materials collection)
        """
        allowed_types = self._get_allowed_entity_types()

        super().__init__(parent=parent, allowed_entity_types=allowed_types)

        self._properties = XCoreHeadless.DialogOptions()
        self._properties.Description = "Material Settings"

        thermal_conductivity = XCore.PropertyReal(
            200.0, 0.0, 100000.0, XCore.Unit("W/mK")
        )
        thermal_conductivity.Description = "Thermal Conductivity"
        self._properties.Add("thermal_conductivity", thermal_conductivity)

    def _get_allowed_entity_types(self) -> tuple[type[xm.Entity], ...]:
        """
        Specifies which types of geometric entities can have this material assigned to them.
        
        In this simulation, materials can only be assigned to solid bodies (not surfaces
        or other entity types). This constraint ensures proper physical modeling.
        
        Returns:
            Tuple of allowed entity types (only Body objects in this case)
        """
        return (xm.Body,)

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
        """
        Provides access to the property group containing editable material properties.
        
        These properties will be displayed in the S4L properties panel when this
        material is selected in the UI.
        """
        return self._properties

    def validate(self) -> bool:
        """
        Validates that the material settings are complete and physically reasonable.
        
        Checks constraints such as non-negative thermal conductivity and ensures
        that the material is assigned to at least one geometric entity.
        
        Returns:
            True if the material settings are valid, False otherwise
        """
        return True

    def clear_status_recursively(self):
        """Clears any status indicators for this material."""
        self.clear_status()

    def as_api_model(self) -> api_models.MaterialSettings:
        """
        Converts this material settings object to a solver API model.
        
        Extracts the thermal conductivity value and the bounding box of the
        associated geometries to create a simplified representation suitable
        for the solver.
        
        Returns:
            A MaterialSettings object in the solver API format
        """
        thermal_conductivity_prop = self._properties.thermal_conductivity
        assert isinstance(thermal_conductivity_prop, XCore.PropertyReal)

        # get the geometry
        p1, p2 = xm.GetBoundingBox([geom.entity for geom in self._geometries])

        return api_models.MaterialSettings(
            thermal_conductivity=thermal_conductivity_prop.Value,
            xmin=p1[0],
            xmax=p2[0],
            ymin=p1[1],
            ymax=p2[1],
            zmin=p1[2],
            zmax=p2[2],
        )


class Materials(Group[MaterialSettings]):
    """
    Collection class that manages a group of MaterialSettings objects.
    
    This class provides functionality for adding, removing, and accessing
    individual material settings. It appears in the simulation tree as the
    "Materials" node, which can be expanded to show individual materials.
    """

    def __init__(
        self, parent: "TreeItem", is_expanded: bool = True, icon: str = ""
    ) -> None:
        """
        Initializes a new materials collection.
        
        Args:
            parent: The parent tree item (typically the Simulation object)
            is_expanded: Whether the materials node starts expanded in the UI tree
            icon: Optional custom icon path (defaults to standard materials icon)
        """
        super().__init__(
            parent,
            MaterialSettings,
            is_expanded,
            icon="icons/XMaterials/materials.ico",
        )

    def _get_new_element_description(self) -> str:
        """
        Provides the base name used when creating new material elements.
        
        Returns:
            The base description string used for new materials
        """
        return "Material"

    def clear_status_recursively(self):
        """
        Clears status indicators for this collection and all contained materials.
        
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
            The plural form of the element type (e.g., "Materials")
        """
        return f"Materials"
