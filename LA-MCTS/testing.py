from lamcts import MCTS
from functions.functions import *
#
# f = Levy(dims=2, bb_opt='de')
f = Rosenbrock(dims=2, complement='de')
# f = Ackley(dims=2, bb_opt='de')

agent = MCTS(
    lb=f.lb,  # the lower bound of each problem dimensions
    ub=f.ub,  # the upper bound of each problem dimensions
    dims=f.dims,  # the problem dimensions
    ninits=f.ninits,  # the number of random samples used in initializations
    func=f,  # function object to be optimized
    Cp=f.Cp,  # Cp for MCTS
    leaf_size=f.leaf_size,  # tree leaf size
    kernel_type=f.kernel_type,  # SVM configruation
    gamma_type=f.gamma_type,  # SVM configruation
    solver_type=f.bb_opt,
    de_type='best',
    solver_evals=1
)

agent.search(iterations=100)

# from diffevo import de_simple
# from diffevo.cost_functions import sphere
#
# bounds = [(-1, 1), (-1, 1)]  # bounds [(x1_min, x1_max), (x2_min, x2_max),...]
# popsize = 10  # population size, must be >= 4
# mutate = 0.5  # mutation factor [0,2]
# recombination = 0.7  # recombination rate [0,1]
# maxiter = 20  # max number of generations
# print("f.lb",f.lb)
# print("f.ub",f.ub)
# print("bounds",bounds)
# de_simple.minimize(sphere, bounds, popsize, mutate, recombination, maxiter)
