import pybamm
import pandas as pd
import numpy as np

# 1. Load and modify the parameter set
param_set_name = "Chen2020"
param = pybamm.ParameterValues(pybamm.parameter_sets[param_set_name])

# Modify specific parameters
param.update({
    "Current function [A]": 2.0,
    "Negative electrode porosity": 0.35,
    "Positive electrode active material volume fraction": 0.6,
    "Electrolyte conductivity [S.m-1]": 1.2,
    "Initial temperature [K]": 298.15
})

# 2. Save modified parameters to CSV
param_dict = param._dict_items
df_params = pd.DataFrame(list(param_dict.items()), columns=["Parameter", "Value"])
df_params.to_csv("Modified_Chen2020_Parameters.csv", index=False)
print("Modified parameters saved to 'Modified_Chen2020_Parameters.csv'")

# 3. Load the P2D model (DFN)
model = pybamm.lithium_ion.DFN()

# 4. Set up and run simulation
sim = pybamm.Simulation(model, parameter_values=param)
solution = sim.solve([0, 3600])  # simulate for 1 hour

# 5. Extract and save selected results
variables_to_save = [
    "Time [s]",
    "Terminal voltage [V]",
    "Current [A]",
]

data = {"Time [s]": solution["Time [s]"].entries}

for var in variables_to_save[1:]:
    try:
        values = solution[var].entries
        
        # These variables should be 1D in time, so no need to average spatially
        data[var] = values
        
    except KeyError:
        print(f"Variable '{var}' not found in solution.")

df_results = pd.DataFrame(data)
df_results.to_csv("Modified_Chen2020_Results.csv", index=False)
print("Simulation results saved to 'Modified_Chen2020_Results.csv'")

# 6. Plot
sim.plot()