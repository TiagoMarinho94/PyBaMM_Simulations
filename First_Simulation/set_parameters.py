import pybamm

parameter_values = pybamm.ParameterValues("Chen2020")
parameter_values
parameter_values["Electrode height [m]"]
parameter_values.search("electrolyte")
model = pybamm.lithium_ion.DFN()
sim = pybamm.Simulation(model, parameter_values=parameter_values)
sim.solve([0, 3600])
sim.plot()