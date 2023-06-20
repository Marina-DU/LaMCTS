# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
# 
import gym
import json
import os

import utils.utils as utils
import numpy as np
from simulator.simulator import Simulator
from eval.eval import f_objective


class tracker:
    def __init__(self, foldername):
        self.counter = 0
        self.results = []
        self.curt_best = float("inf")
        self.foldername = "results/" + foldername
        try:
            os.mkdir(self.foldername)
        except OSError:
            print("Creation of the directory %s failed" % foldername)
        else:
            print("Successfully created the directory %s " % foldername)

    def dump_trace(self):
        trace_path = self.foldername + '/result' + str(len(self.results))
        final_results_str = json.dumps(self.results)
        with open(trace_path, "a") as f:
            f.write(final_results_str + '\n')

    def track(self, result):
        if result < self.curt_best:
            self.curt_best = result
        self.results.append(self.curt_best)
        if len(self.results) % 100 == 0:
            self.dump_trace()


class Levy:
    def __init__(self, dims=10, complement=''):
        self.dims = dims
        self.lb = -10 * np.ones(dims)
        self.ub = 10 * np.ones(dims)
        self.complement = complement
        self.tracker = tracker('Levy' + str(dims) + str(self.complement))

        # tunable hyper-parameters in LA-MCTS
        self.Cp = 10
        self.leaf_size = 8
        self.kernel_type = "poly"
        self.ninits = 40
        self.gamma_type = "auto"
        print("initialize levy at dims:", self.dims)

    def __call__(self, x):
        assert len(x) == self.dims
        assert x.ndim == 1
        assert np.all(x <= self.ub) and np.all(x >= self.lb)

        w = []
        for idx in range(0, len(x)):
            w.append(1 + (x[idx] - 1) / 4)
        w = np.array(w)

        term1 = (np.sin(np.pi * w[0])) ** 2;

        term3 = (w[-1] - 1) ** 2 * (1 + (np.sin(2 * np.pi * w[-1])) ** 2);

        term2 = 0;
        for idx in range(1, len(w)):
            wi = w[idx]
            new = (wi - 1) ** 2 * (1 + 10 * (np.sin(np.pi * wi + 1)) ** 2)
            term2 = term2 + new

        result = term1 + term2 + term3
        self.tracker.track(result)

        return result


class Ackley:
    def __init__(self, dims=10, complement=''):
        self.dims = dims
        self.lb = -5 * np.ones(dims)
        self.ub = 10 * np.ones(dims)
        self.counter = 0
        self.complement = complement
        self.tracker = tracker('Ackley' + str(dims) + str(self.complement))

        # tunable hyper-parameters in LA-MCTS
        self.Cp = 1
        self.leaf_size = 10
        self.ninits = 40
        self.kernel_type = "rbf"
        self.gamma_type = "auto"

    def __call__(self, x):
        self.counter += 1
        assert len(x) == self.dims
        assert x.ndim == 1
        assert np.all(x <= self.ub) and np.all(x >= self.lb)
        result = (-20 * np.exp(-0.2 * np.sqrt(np.inner(x, x) / x.size)) - np.exp(
            np.cos(2 * np.pi * x).sum() / x.size) + 20 + np.e)
        self.tracker.track(result)

        return result


class Rosenbrock:
    def __init__(self, dims=10, complement=''):
        self.dims = dims
        self.lb = -10 * np.ones(dims)
        self.ub = 10 * np.ones(dims)
        self.counter = 0
        self.complement = complement
        self.tracker = tracker('Rosenbrock' + str(dims) + str(self.complement))

        # tunable hyper-parameters in LA-MCTS
        self.Cp = 10
        self.leaf_size = 10
        self.kernel_type = "poly"
        self.ninits = 40
        self.gamma_type = "auto"
        print("initialize rosenbrock at dims:", self.dims)

    def __call__(self, x):
        self.counter += 1
        assert len(x) == self.dims
        assert x.ndim == 1
        assert np.all(x <= self.ub) and np.all(x >= self.lb)

        result = sum(100.0 * (x[1:] - x[:-1] ** 2.0) ** 2.0 + (1 - x[:-1]) ** 2.0)
        # result = -1 * result
        self.tracker.track(result)

        return result


class circadianClock:
    def __init__(self, complement='', score_criterium = 3):
        # tunable hyper-parameters in LA-MCTS
        self.Cp = 10
        self.leaf_size = 10
        self.kernel_type = "poly"
        self.ninits = 40
        self.gamma_type = "auto"
        self.complement = complement
        self.score_criterium = score_criterium

        # 1. Parse the SMB file that contains specifications about the biological interaction graph
        self.variables, _, self.initialHybridState, _, self.BK = utils.parse('circadian_clock', False)

        # 2. Set up the simulator
        self.simulator = Simulator(self.variables, self.initialHybridState, self.BK)

        self.celerities = self.simulator.getAllCelerities()
        self.dims = len(self.celerities)  # problem dimensions
        self.lb = np.ones(self.dims) * -2  # lower bound for each dimensions
        self.ub = np.ones(self.dims) * 2  # upper bound for each dimensions
        self.tracker = tracker('circadianClock' + str(self.complement))  # defined in functions.py

    def objective_function(self, x):
        for i in range(self.dims):
            self.celerities[i].setValue(x[i])

        self.simulator = Simulator(self.variables, self.initialHybridState, self.BK)
        self.simulator.simulation(self.celerities)
        return f_objective(x, self.simulator, self.BK, criteria=self.score_criterium)[0]

    def __call__(self, x):
        # some sanity check of x
        assert len(x) == self.dims

        result = self.objective_function(x)
        self.tracker.track(result)
        return result


class cellCycleBehaegel:
    def __init__(self, complement='', score_criterium = 3):
        # tunable hyper-parameters in LA-MCTS
        self.Cp = 10
        self.leaf_size = 10
        self.kernel_type = "poly"
        self.ninits = 40
        self.gamma_type = "auto"
        self.complement = complement
        self.score_criterium = score_criterium

        # 1. Parse the SMB file that contains specifications about the biological interaction graph
        self.variables, _, self.initialHybridState, _, self.BK = utils.parse('cell_cycle_behaegel', False)

        # 2. Set up the simulator
        self.simulator = Simulator(self.variables, self.initialHybridState, self.BK)

        self.celerities = self.simulator.getAllCelerities()
        self.dims = len(self.celerities)  # problem dimensions
        self.lb = np.ones(self.dims) * -7  # lower bound for each dimensions
        self.ub = np.ones(self.dims) * 7  # upper bound for each dimensions
        self.tracker = tracker('cellCycleBehaegel' + str(self.complement))  # defined in functions.py

    def objective_function(self, x):
        for i in range(self.dims):
            self.celerities[i].setValue(x[i])

        self.simulator = Simulator(self.variables, self.initialHybridState, self.BK)
        self.simulator.simulation(self.celerities)
        return f_objective(x, self.simulator, self.BK, criteria=self.score_criterium)[0]

    def __call__(self, x):
        # some sanity check of x
        assert len(x) == self.dims

        result = self.objective_function(x)
        self.tracker.track(result)
        return result


class testHgrn:
    def __init__(self, complement='', score_criterium = 3):
        # tunable hyper-parameters in LA-MCTS
        self.Cp = 10
        self.leaf_size = 10
        self.kernel_type = "poly"
        self.ninits = 40
        self.gamma_type = "auto"
        self.complement = complement
        self.score_criterium = score_criterium

        # 1. Parse the SMB file that contains specifications about the biological interaction graph
        self.variables, _, self.initialHybridState, _, self.BK = utils.parse('test', False)

        # 2. Set up the simulator
        self.simulator = Simulator(self.variables, self.initialHybridState, self.BK)

        self.celerities = self.simulator.getAllCelerities()
        self.dims = len(self.celerities)  # problem dimensions
        self.lb = np.ones(self.dims) * -2  # lower bound for each dimensions
        self.ub = np.ones(self.dims) * 2  # upper bound for each dimensions
        self.tracker = tracker('testHgrn' + str(self.complement))  # defined in functions.py

    def objective_function(self, x):
        for i in range(self.dims):
            self.celerities[i].setValue(x[i])

        self.simulator = Simulator(self.variables, self.initialHybridState, self.BK)
        self.simulator.simulation(self.celerities)
        return f_objective(x, self.simulator, self.BK, criteria=self.score_criterium)[0]

    def __call__(self, x):
        # some sanity check of x
        assert len(x) == self.dims

        result = self.objective_function(x)
        self.tracker.track(result)
        return result


class Lunarlanding:
    def __init__(self):
        self.dims = 12
        self.lb = np.zeros(12)
        self.ub = 2 * np.ones(12)
        self.counter = 0
        self.env = gym.make('LunarLander-v2')

        # tunable hyper-parameters in LA-MCTS
        self.Cp = 50
        self.leaf_size = 10
        self.kernel_type = "poly"
        self.ninits = 40
        self.gamma_type = "scale"

        self.render = False

    def heuristic_Controller(self, s, w):
        angle_targ = s[0] * w[0] + s[2] * w[1]
        if angle_targ > w[2]:
            angle_targ = w[2]
        if angle_targ < -w[2]:
            angle_targ = -w[2]
        hover_targ = w[3] * np.abs(s[0])

        angle_todo = (angle_targ - s[4]) * w[4] - (s[5]) * w[5]
        hover_todo = (hover_targ - s[1]) * w[6] - (s[3]) * w[7]

        if s[6] or s[7]:
            angle_todo = w[8]
            hover_todo = -(s[3]) * w[9]

        a = 0
        if hover_todo > np.abs(angle_todo) and hover_todo > w[10]:
            a = 2
        elif angle_todo < -w[11]:
            a = 3
        elif angle_todo > +w[11]:
            a = 1
        return a

    def __call__(self, x):
        self.counter += 1
        assert len(x) == self.dims
        assert x.ndim == 1
        assert np.all(x <= self.ub) and np.all(x >= self.lb)

        total_rewards = []
        for i in range(0, 3):  # controls the number of episode/plays per trial
            state = self.env.reset()
            rewards_for_episode = []
            num_steps = 2000

            for step in range(num_steps):
                if self.render:
                    self.env.render()
                received_action = self.heuristic_Controller(state, x)
                next_state, reward, done, info = self.env.step(received_action)
                rewards_for_episode.append(reward)
                state = next_state
                if done:
                    break

            rewards_for_episode = np.array(rewards_for_episode)
            total_rewards.append(np.sum(rewards_for_episode))
        total_rewards = np.array(total_rewards)
        mean_rewards = np.mean(total_rewards)

        return mean_rewards * -1
