from dataclasses import dataclass
from enum import Enum

from dataclasses_json import dataclass_json
from s4l_core.simulator_plugins.base.solver.driver.api_models import (
    ApiSimulationBase,
    BaseSimulations,
)


class LogLevel(Enum):
    """
    Enumeration of available logging levels for the simulation.
    
    These values control how verbose the solver output will be during execution.
    """
    INFO = "info"   # Standard information messages
    DEBUG = "debug" # Detailed debugging information
    ERROR = "error" # Only error messages


@dataclass_json
@dataclass
class SetupSettings:
    """
    General simulation setup parameters.
    
    This class defines basic settings that apply to the entire simulation,
    such as logging verbosity.
    """
    log_level: str = LogLevel.INFO.value


@dataclass_json
@dataclass
class MaterialSettings:
    """
    Physical material properties and spatial extents.
    
    This class defines both the physical properties of the material (thermal conductivity)
    and the spatial region it occupies in the simulation domain.
    """
    xmin: float  # Minimum x-coordinate of the material region
    xmax: float  # Maximum x-coordinate of the material region
    ymin: float  # Minimum y-coordinate of the material region
    ymax: float  # Maximum y-coordinate of the material region
    zmin: float  # Minimum z-coordinate of the material region
    zmax: float  # Maximum z-coordinate of the material region
    thermal_conductivity: float = 200.0  # Thermal conductivity in W/mK


@dataclass_json
@dataclass
class SourceSettings:
    """
    Heat source properties and location.
    
    This class defines a point heat source with a specific volumetric heat
    generation rate at a specific location in the simulation domain.
    """
    x: float  # x-coordinate of the heat source
    y: float  # y-coordinate of the heat source
    z: float  # z-coordinate of the heat source
    volumetric_heat_source: float = 100.0  # Heat generation rate in W/m³


class DirichletFace(Enum):
    """
    Enumeration of domain boundary faces where temperature can be specified.
    
    These values identify the six faces of the rectangular simulation domain
    where Dirichlet (fixed temperature) boundary conditions can be applied.
    """
    XMIN = "xmin"  # Minimum x boundary face
    XMAX = "xmax"  # Maximum x boundary face
    YMIN = "ymin"  # Minimum y boundary face
    YMAX = "ymax"  # Maximum y boundary face
    ZMIN = "zmin"  # Minimum z boundary face
    ZMAX = "zmax"  # Maximum z boundary face


@dataclass_json
@dataclass
class BoundarySettings:
    """
    Boundary condition specification.
    
    This class defines a Dirichlet (fixed temperature) boundary condition
    that can be applied to one of the six faces of the rectangular domain.
    """
    face: str = DirichletFace.XMIN.value  # Which boundary face this applies to
    temperature: float = 0.0  # Fixed temperature value in K


@dataclass_json
@dataclass
class GridSettings:
    """
    Computational grid parameters.
    
    This class defines the resolution of the finite difference grid used
    to discretize the simulation domain.
    """
    dx: float = 1.0  # Grid spacing in x-direction (m)
    dy: float = 1.0  # Grid spacing in y-direction (m)
    dz: float = 1.0  # Grid spacing in z-direction (m)


class SolverMethod(Enum):
    """
    Enumeration of available numerical solution methods.
    
    These values identify the different numerical algorithms that can be
    used to solve the heat equation.
    """
    JACOBI = "jacobi"  # Simple Jacobi iteration method


@dataclass_json
@dataclass
class SolverSettings:
    """
    Numerical solver parameters.
    
    This class defines settings that control the behavior of the numerical
    solver, including convergence criteria and algorithm selection.
    """
    solver_method: str = SolverMethod.JACOBI.value  # Solution algorithm to use
    tolerance: float = 1e-4  # Convergence tolerance
    max_iter: int = 100  # Maximum number of iterations


@dataclass_json
@dataclass
class Simulation(ApiSimulationBase):
    """
    Complete simulation configuration.
    
    This class combines all the individual settings components into a single
    structure that fully defines a simulation. This is the main data structure
    passed from the UI to the solver code.
    """
    setup_settings: SetupSettings  # General simulation settings
    material_settings: list[MaterialSettings]  # List of materials in the domain
    source_setings: list[SourceSettings]  # List of heat sources in the domain
    boundary_settings: list[BoundarySettings]  # List of boundary conditions
    grid_settings: GridSettings  # Computational grid parameters
    solver_settings: SolverSettings  # Numerical solver settings


@dataclass_json
@dataclass
class Simulations(BaseSimulations):
    """
    Container for multiple simulation configurations.
    
    This class is used when multiple simulations need to be defined and
    executed as a batch.
    """
    simulations: list[Simulation]  # List of individual simulation configurations
