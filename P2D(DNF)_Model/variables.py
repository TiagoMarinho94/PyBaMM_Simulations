import pybamm
import pandas as pd
import numpy as np

# 1. Load and modify the parameter set
param = pybamm.ParameterValues(pybamm.parameter_sets["Chen2020"])
param.update({
    "Current function [A]": 2.0,
    "Negative electrode porosity": 0.35,
    "Positive electrode active material volume fraction": 0.6,
    "Electrolyte conductivity [S.m-1]": 1.2,
    "Initial temperature [K]": 298.15
})

# 2. Save updated parameters
params_list = [(k, v) for k, v in param.items()]
pd.DataFrame(params_list, columns=["Parameter", "Value"]).to_csv("variables_Chen2020_Parameters.csv", index=False)

# 3. Solve the DFN model
model = pybamm.lithium_ion.DFN()
sim = pybamm.Simulation(model, parameter_values=param, solver=pybamm.CasadiSolver())
solution = sim.solve([0, 3600])  # 1 hour

# 4. Time-dependent variables
time_vars = [
    "Time [s]",
    "Terminal voltage [V]",
    "Current [A]",
    "Discharge capacity [A.h]",
    "Cell temperature [K]",
    "Total lithium loss [mol]",
    "State of Charge",
]

time_data = {}
time_ref = solution["Time [s]"].entries.flatten()
time_data["Time [s]"] = time_ref

for var in time_vars[1:]:  # skip Time [s], already added
    try:
        data = solution[var].entries.flatten()
        if len(data) == len(time_ref):
            time_data[var] = data
        else:
            print(f"[Time] Skipped (length mismatch): {var}")
    except KeyError:
        print(f"[Time] Skipped (not found): {var}")
    except Exception as e:
        print(f"[Time] Skipped (error in '{var}'): {e}")

# Save results to CSV
pd.DataFrame(time_data).to_csv("Time_Dependent_Results.csv", index=False)
print("Time-dependent variables saved successfully.")

# 5. Export time-dependent variables
time_vars = [
    "Time [s]",
    "Terminal voltage [V]",
    "Current [A]",
    "Discharge capacity [A.h]",
    "Cell temperature [K]",
    "Total lithium loss [mol]",
    "State of Charge",
]

time_data = {}
time_ref = solution["Time [s]"].entries.flatten()
time_data["Time [s]"] = time_ref

for var in time_vars[1:]:  # skip Time [s], already added
    try:
        data = solution[var].entries.flatten()
        if len(data) == len(time_ref):
            time_data[var] = data
        else:
            print(f"[Time] Skipped (length mismatch): {var}")
    except KeyError:
        print(f"[Time] Skipped (not found): {var}")
    except Exception as e:
        print(f"[Time] Skipped (error in '{var}'): {e}")

pd.DataFrame(time_data).to_csv("Time_Dependent_Results.csv", index=False)
print("Time-dependent variables saved successfully.")

# 6. Export x-dependent variables
x_vars = [
    "Electrolyte concentration [mol.m-3]",
    "Electrolyte potential [V]",
    "Electrolyte current density [A.m-2]",
]

x_data_all = []
x_time = solution["Time [s]"].entries

# Get mesh from solver's problem (CasadiSolver exposes this)
mesh = sim._solver.problem.mesh
x_nodes = mesh.combine_submeshes("x").nodes

for var in x_vars:
    try:
        y = solution[var]
        vals = y.entries  # shape: (time, x)

        if vals.shape[1] != len(x_nodes):
            raise ValueError(f"Mismatch: {vals.shape[1]} values but {len(x_nodes)} x-nodes")

        for i, t in enumerate(x_time):
            df = pd.DataFrame(
                vals[i].reshape(1, -1),
                columns=[f"x={xi:.4e}" for xi in x_nodes]
            )
            df.insert(0, "Time [s]", t)
            df["Variable"] = var
            x_data_all.append(df)

        print(f"[x] Exported: {var}")
    except KeyError:
        print(f"[x] Skipped (not found): {var}")
    except Exception as e:
        print(f"[x] Skipped (error with {var}): {e}")

if x_data_all:
    pd.concat(x_data_all, ignore_index=True).to_csv("X_Spatial_Results.csv", index=False)
    print("X-dependent variables saved successfully.")
else:
    print("No x-dependent variables saved.")