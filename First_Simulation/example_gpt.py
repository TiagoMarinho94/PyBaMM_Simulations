import pybamm
import numpy as np
import pandas as pd

# Load the DFN model
model = pybamm.lithium_ion.DFN()

# Load default parameters and geometry
parameter_values = model.default_parameter_values
geometry = model.default_geometry

# Process geometry
parameter_values.process_geometry(geometry)

# Create mesh
mesh = pybamm.Mesh(geometry, model.default_submesh_types, model.default_var_pts)

# Discretisation
disc = pybamm.Discretisation(mesh, model.default_spatial_methods)

# Process model parameters
parameter_values.process_model(model)

# Discretise the model
disc.process_model(model)

# Make sure t_eval is an array (Time vector)
t_eval = np.linspace(0, 3600, 100)  # 1 hour

# Solve
solver = pybamm.CasadiSolver()
solution = solver.solve(model, t_eval)

# Plot
pybamm.dynamic_plot(solution)

# Inspect available variables
print("Available variables:")
for name in model.variables.keys():
    print("-", name)

# Extract data
time = solution["Time [s]"].entries
voltage = solution["Terminal voltage [V]"].entries
current = solution["Current [A]"].entries
temperature = solution["X-averaged cell temperature [K]"].entries

# Create a DataFrame
df = pd.DataFrame({
    "Time [s]": time,
    "Voltage [V]": voltage,
    "Current [A]": current,
    "X-avg Temperature [K]": temperature
})

# Save to CSV
df.to_csv("dfn_results.csv", index=False)

print("Scalar time-series saved to dfn_scalar_results.csv")