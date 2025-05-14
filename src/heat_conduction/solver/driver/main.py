# Heat Conduction Simulation (Steady-State)
# -----------------------------------------
# Governing Equation:
#     ∇·(k ∇T) + Q = 0
#     - T(x, y, z): Temperature scalar field [K]
#     - k: Thermal conductivity [W/m·K]
#     - ∇T: Temperature gradient [K/m]
#     - k ∇T: Heat flux vector field [W/m²]
#     - ∇·(k ∇T): Divergence of heat flux [W/m³]
#     - Q: Volumetric heat source term [W/m³]
#
# Interpretation:
#     At steady state, the net heat flowing into any volume plus the internal heat generation must be zero.
#     For constant k, this simplifies to:
#         ∇²T = -Q / k
#
# This script discretizes the domain using finite differences and solves the steady-state equation iteratively.

import argparse
import json
import logging
import os
import sys

import numpy as np
import pyvista as pv
from heat_conduction.solver.driver.api_models import Simulation

# Enum-like constant for boundary face names
DIRICHLET_FACES = ["xmin", "xmax", "ymin", "ymax", "zmin", "zmax"]

# --- CLI Argument Parsing ---
parser = argparse.ArgumentParser(description="Heat Conduction Solver")
parser.add_argument(
    "-i",
    "--inputfile",
    type=str,
    required=True,
    help="Path to simulation input JSON file containing model parameters"
)
parser.add_argument(
    "-o", 
    "--outputfolder", 
    type=str, 
    required=True, 
    help="Path to output folder for solver results and visualization files"
)
args = parser.parse_args()

# --- Setup Logging ---
# Configure both console and file logging to track solver execution
input_path = os.path.abspath(args.inputfile)
output_dir = os.path.abspath(args.outputfolder)
os.makedirs(output_dir, exist_ok=True)
log_path = os.path.join(output_dir, "solver.log")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# --- Load and Parse Input JSON ---
# Load the simulation configuration created through the S4L UI
with open(args.inputfile, "r") as f:
    sim = Simulation.from_json(f.read())  # pyright: ignore[reportGeneralTypeIssues]

material = sim.material_settings[0]
grid = sim.grid_settings
solver = sim.solver_settings

# --- Log Input Summary ---
# Log the key simulation parameters for reference and debugging
logger.info("=== Simulation Configuration Summary ===")
logger.info(f"Log level: {sim.setup_settings.log_level.upper()}")
logger.info(
    f"Domain Extents: x=[{material.xmin}, {material.xmax}], y=[{material.ymin}, {material.ymax}], z=[{material.zmin}, {material.zmax}]"
)
logger.info(f"Grid Spacing: dx={grid.dx}, dy={grid.dy}, dz={grid.dz}")
logger.info(
    f"Solver: method={solver.solver_method}, tol={solver.tolerance}, max_iter={solver.max_iter}"
)
logger.info(f"Material: thermal_conductivity={material.thermal_conductivity}")
for idx, src in enumerate(sim.source_setings):
    logger.info(
        f"  Source {idx+1}: location=({src.x}, {src.y}, {src.z}), value={src.volumetric_heat_source}"
    )
for bc in sim.boundary_settings:
    logger.info(f"  Boundary: {bc.face}, Temperature={bc.temperature}")
logger.info("========================================")

# --- Grid Setup ---
# Create the computational grid based on domain size and grid spacing
nx = int((material.xmax - material.xmin) / grid.dx) + 1
ny = int((material.ymax - material.ymin) / grid.dy) + 1
nz = int((material.zmax - material.zmin) / grid.dz) + 1
k = material.thermal_conductivity
T = np.zeros((nx, ny, nz))  # Temperature field
Q = np.zeros((nx, ny, nz))  # Heat source field

# --- Insert Heat Sources ---
# Place volumetric heat sources at their specified locations
for src in sim.source_setings:
    i = int((src.x - material.xmin) / grid.dx)
    j = int((src.y - material.ymin) / grid.dy)
    k_ = int((src.z - material.zmin) / grid.dz)
    if 0 <= i < nx and 0 <= j < ny and 0 <= k_ < nz:
        Q[i, j, k_] = src.volumetric_heat_source
    else:
        logger.warning(f"Source at ({src.x}, {src.y}, {src.z}) is out of bounds.")

# --- Apply Dirichlet Boundary Conditions ---
# Set temperature values at domain boundaries based on user settings
bc_map = {face: None for face in DIRICHLET_FACES}
for bc in sim.boundary_settings:
    bc_map[bc.face] = bc.temperature
if bc_map["xmin"] is not None:
    T[0, :, :] = bc_map["xmin"]
if bc_map["xmax"] is not None:
    T[-1, :, :] = bc_map["xmax"]
if bc_map["ymin"] is not None:
    T[:, 0, :] = bc_map["ymin"]
if bc_map["ymax"] is not None:
    T[:, -1, :] = bc_map["ymax"]
if bc_map["zmin"] is not None:
    T[:, :, 0] = bc_map["zmin"]
if bc_map["zmax"] is not None:
    T[:, :, -1] = bc_map["zmax"]

# --- Jacobi Solver ---
# Iteratively solve the finite difference equations for steady-state heat conduction
# This simple solver updates each interior grid point based on its neighbors and heat sources
logger.info("Starting solver...")
tol = solver.tolerance
max_iter = solver.max_iter
it = 0
for it in range(max_iter):
    T_old = T.copy()
    for i in range(1, nx - 1):
        for j in range(1, ny - 1):
            for k_ in range(1, nz - 1):
                # Finite difference approximation of Laplacian(T) = -Q/k
                # For uniform grid: T[i,j,k] = avg(neighbors) + dx²*Q/6k
                T[i, j, k_] = (
                    T_old[i + 1, j, k_]
                    + T_old[i - 1, j, k_]
                    + T_old[i, j + 1, k_]
                    + T_old[i, j - 1, k_]
                    + T_old[i, j, k_ + 1]
                    + T_old[i, j, k_ - 1]
                    + grid.dx ** 2 * Q[i, j, k_] / k
                ) / 6.0
    error = np.max(np.abs(T - T_old))
    if it % 100 == 0:
        logger.info(f"Iteration {it}, max error: {error:.6f}")
    if error < tol:
        logger.info(f"Converged after {it} iterations, max error: {error:.6f}")
        break

# --- Write Summary Statistics ---
# Capture key results for quick analysis and reporting
summary = {
    "min_temperature": float(np.min(T)),
    "max_temperature": float(np.max(T)),
    "mean_temperature": float(np.mean(T)),
    "argmin_index": tuple(int(i) for i in np.unravel_index(np.argmin(T), T.shape)),
    "argmax_index": tuple(int(i) for i in np.unravel_index(np.argmax(T), T.shape)),
    "total_heat_input": float(np.sum(Q)),
    "iterations": int(it),
}
with open(os.path.join(output_dir, "summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

# --- VTK Export ---
# Export simulation results as VTK files that can be visualized in ParaView or other tools

# Common grid coordinates
x_coords = np.linspace(material.xmin, material.xmax, nx)
y_coords = np.linspace(material.ymin, material.ymax, ny)
z_coords = np.linspace(material.zmin, material.zmax, nz)

# --- Temperature Field ---
# Export the calculated temperature field as a VTK rectilinear grid file
vtk_temp_grid = pv.RectilinearGrid(x_coords, y_coords, z_coords)
vtk_temp_grid.point_data.clear()
vtk_temp_grid["Temperature"] = T.flatten(
    order="F"
)  # pyright: ignore[reportGeneralTypeIssues]
vtk_temp_grid.save(os.path.join(output_dir, "Temperature.vtr"))

# --- Heat Flux Vector Field ---
# Compute and export the heat flux vector field (q = -k∇T)
vtk_flux_grid = pv.RectilinearGrid(x_coords, y_coords, z_coords)

# Compute gradients and heat flux 
grad_x, grad_y, grad_z = np.gradient(T, grid.dx, grid.dy, grid.dz)
q_x = -k * grad_x  # Negative gradient gives heat flow direction
q_y = -k * grad_y
q_z = -k * grad_z
heat_flux = np.stack([q_x, q_y, q_z], axis=-1)  # shape: (nx, ny, nz, 3)

# Flatten and assign to VTK grid
vectors = heat_flux.reshape(-1, 3, order="F")
vtk_flux_grid.point_data.clear()
vtk_flux_grid["HeatFlux"] = vectors
vtk_flux_grid.point_data.SetActiveVectors("HeatFlux")
vtk_flux_grid.save(os.path.join(output_dir, "HeatFlux.vtr"))

print(f"Files are stored in {output_dir}")
