# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
# 
from functions.functions import *
from functions.mujoco_functions import *
from lamcts import MCTS
import argparse

parser = argparse.ArgumentParser(description='Process inputs')
parser.add_argument('--func', help='specify the test function')
parser.add_argument('--dims', type=int, help='specify the problem dimensions')
parser.add_argument('--iterations', type=int, help='specify the iterations to collect in the search')
parser.add_argument('--bb-optimizer', type=str, help='specify the black-box optimizer to use', default='bo')
parser.add_argument('--samples-optimizer', type=int,
                    help='number of samples/evaluations (for bo, de, and pso) or max number of samples/evaluations (for turbo)',
                    default=None)
parser.add_argument('--ninits', type=int, help='specify the number of random samples used in initializations')
parser.add_argument('--cp', type=float, help='specify the Cp for MCTS')
parser.add_argument('--leaf-size', type=int, help='specify the tree leaf size')
parser.add_argument('--kernel-type', type=str, help='specify the kernel type')
parser.add_argument('--de-type', type=str, help='specify type of DE regarding the mutation step', default=None)
parser.add_argument('--hgrn-criterium', type=int, help='scoring criterium for hgrn functions', choices=[3, 4],
                    default=None)

args = parser.parse_args()

if args.samples_optimizer is None:
    args.samples_optimizer = 10000 if args.bb_optimizer == 'turbo' else 1

if args.bb_optimizer == 'de' and args.de_type is None:
    args.de_type = 'rand'

if args.hgrn_criterium is None and args.func in ["circadianClock", "cellCycle", "testHgrn"]:
    args.hgrn_criterium = 3

complement = '_' + args.bb_optimizer + ('_' + args.de_type if args.de_type is not None else '') + '_' + \
             str(args.samples_optimizer) + ('samples' if args.bb_optimizer != 'turbo' else 'max_samples') + \
             ('_crit' + str(args.hgrn_criterium) if args.hgrn_criterium is not None else '')

f = None
iteration = 0
if args.func == 'ackley':
    assert args.dims > 0
    f = Ackley(dims=args.dims, complement=complement)
elif args.func == 'levy':
    assert args.dims > 0
    f = Levy(dims=args.dims, complement=complement)
elif args.func == 'rosenbrock':
    assert args.dims > 0
    f = Rosenbrock(dims=args.dims, complement=complement)
elif args.func == 'lunar':
    f = Lunarlanding()
elif args.func == 'swimmer':
    f = Swimmer()
elif args.func == 'hopper':
    f = Hopper()
elif args.func == 'circadianClock':
    f = circadianClock(complement=complement)
elif args.func == 'cellCycle':
    f = cellCycleBehaegel(complement=complement)
elif args.func == 'testHgrn':
    f = testHgrn(complement=complement)
else:
    print('function not defined')
    os._exit(1)

assert f is not None
assert args.iterations > 0

# f = Ackley(dims = 10)
# f = Levy(dims = 10)
# f = Swimmer()
# f = Hopper()
# f = Lunarlanding()

agent = MCTS(
    lb=f.lb,  # the lower bound of each problem dimensions
    ub=f.ub,  # the upper bound of each problem dimensions
    dims=f.dims,  # the problem dimensions
    ninits=f.ninits if args.ninits is None else args.ninits,  # the number of random samples used in initializations
    func=f,  # function object to be optimized
    Cp=f.Cp if args.cp is None else args.cp,  # Cp for MCTS
    leaf_size=f.leaf_size if args.leaf_size is None else args.leaf_size,  # tree leaf size
    kernel_type=f.kernel_type if args.kernel_type is None else args.kernel_type,  # SVM configruation
    gamma_type=f.gamma_type,  # SVM configruation
    solver_type=args.bb_optimizer,
    solver_evals=args.samples_optimizer,
    de_type=args.de_type
)

agent.search(iterations=args.iterations)

"""
FAQ:

1. How to retrieve every f(x) during the search?

During the optimization, the function will create a folder to store the f(x) trace; and
the name of the folder is in the format of function name + function dimensions, e.g. Ackley10.

Every 100 samples, the function will write a row to a file named results + total samples, e.g. result100 
mean f(x) trace in the first 100 samples.

Each last row of result file contains the f(x) trace starting from 1th sample -> the current sample.
Results of previous rows are from previous experiments, as we always append the results from a new experiment
to the last row.

Here is an example to interpret a row of f(x) trace.
[5, 3.2, 2.1, ..., 1.1]
The first sampled f(x) is 5, the second sampled f(x) is 3.2, and the last sampled f(x) is 1.1 

2. How to improve the performance?
Tune Cp, leaf_size, and improve BO sampler with others.

"""
