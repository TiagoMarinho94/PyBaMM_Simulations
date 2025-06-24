import pybamm
import pandas as pd

# 0. Load the Available Models
print("Available parameter sets:", list(pybamm.parameter_sets.keys()))

# 1. Load the P2D model and parameter set
param_set_name = "Chen2020"
param = pybamm.ParameterValues(pybamm.parameter_sets[param_set_name])

# 2. Access the parameter dict
param_dict = param._dict_items

# 3. Save parameters to CSV
df = pd.DataFrame(list(param_dict.items()), columns=["Parameter", "Value"])
df.to_csv("P2D_Parameters.csv", index=False)

print(f"Parameters from '{param_set_name}' saved to P2D_Parameters.csv")