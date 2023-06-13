import utils.utils as utils
from random import seed, uniform
import numpy as np
from simulator.simulator import Simulator
from eval.eval import f_objective

if __name__ == '__main__':

    # 1. Parse the SMB file that contains specifications about the biological interaction graph
    variables, _, initialHybridState, _, BK = utils.parse('test', True)

    # 2. Set up the simulator
    simulator = Simulator(variables, initialHybridState, BK)

    allCelerities = simulator.getAllCelerities()

    nbOfVariables = len(allCelerities)
    print("Number of celerities in the simulator:", nbOfVariables)

    # Example of a random simulation
    for j in range(100):
        x = []
        for i in range(len(allCelerities)):
            allCelerities[i].setValue(uniform(-2, 2))
            x.append(allCelerities[i].getValue())


        simulator.simulation(allCelerities)

        # trace = simulator.getTrace()
        #
        # for path in trace:
        #     print(path[0], " ", path[1])


        f_score = f_objective(x, simulator, BK)
        print(j, f_score[0], x)
