# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
# 
from .Classifier import Classifier
import json
import numpy as np
import math
import operator
import copy
from random import sample as random_sample
from diffevo import de_simple
from pso import particle as pso


class Node:
    obj_counter = 0

    # If a leave holds >= SPLIT_THRESH, we split into two new nodes.

    def __init__(self, parent=None, dims=0, reset_id=False, kernel_type="rbf", gamma_type="auto"):
        # Note: every node is initialized as a leaf,
        # only internal nodes equip with classifiers to make decisions
        # if not is_root:
        #     assert type( parent ) == type( self )
        self.dims = dims
        self.x_bar = float('inf')
        self.n = 0
        self.uct = 0
        self.classifier = Classifier([], self.dims, kernel_type, gamma_type)

        # insert curt into the kids of parent
        self.parent = parent
        self.kids = []  # 0:good, 1:bad

        self.bag = []

        # for DE
        self.population = np.array([])
        self.population_ev = np.array([])
        self.target_index = 0
        self.generation = 1
        self.best_in_gen_idx = None

        # # for PSO
        # self.particles = []
        # self.global_best_fitness = float('inf')
        # self.global_best_position = None

        self.is_svm_splittable = False

        if reset_id:
            Node.obj_counter = 0

        self.id = Node.obj_counter

        # data for good and bad kids, respectively
        Node.obj_counter += 1

    def update_kids(self, good_kid, bad_kid):
        assert len(self.kids) == 0
        self.kids.append(good_kid)
        self.kids.append(bad_kid)
        assert self.kids[0].classifier.get_mean() > self.kids[1].classifier.get_mean()

    def is_good_kid(self):
        if self.parent is not None:
            if self.parent.kids[0] == self:
                return True
            else:
                return False
        else:
            return False

    def is_leaf(self):
        if len(self.kids) == 0:
            return True
        else:
            return False

    def visit(self):
        self.n += 1

    def print_bag(self):
        sorted_bag = sorted(self.bag.items(), key=operator.itemgetter(1))
        print("BAG" + "#" * 10)
        for item in sorted_bag:
            print(item[0], "==>", item[1])
        print("BAG" + "#" * 10)
        print('\n')

    def get_best_idx(self):
        return min(range(len(self.bag)), key=lambda i: self.bag[i][1])

    def get_best_from_current_population(self):
        return self.population[min(enumerate(self.population_ev), key=lambda x: x[1])[0]]

    def update_bag(self, samples):
        assert len(samples) > 0

        self.bag.clear()
        self.bag.extend(samples)
        self.classifier.update_samples(self.bag)
        if len(self.bag) <= 2:
            self.is_svm_splittable = False
        else:
            self.is_svm_splittable = self.classifier.is_splittable_svm()
        self.x_bar = self.classifier.get_mean()
        self.n = len(self.bag)

    def clear_data(self):
        self.bag.clear()

    def get_name(self):
        # state is a list of jsons
        return "node" + str(self.id)

    def pad_str_to_8chars(self, ins, total):
        if len(ins) <= total:
            ins += ' ' * (total - len(ins))
            return ins
        else:
            return ins[0:total]

    def get_rand_sample_from_bag(self):
        if len(self.bag) > 0:
            upeer_boundary = len(list(self.bag))
            rand_idx = np.random.randint(0, upeer_boundary)
            return self.bag[rand_idx][0]
        else:
            return None

    def check_target_index(self, de_type='rand'):
        if self.target_index >= len(self.population):
            print(f'node{self.id} finished generation {self.generation}')
            self.target_index = 0
            self.generation = self.generation + 1
            if de_type == 'best':
                self.best_in_gen_idx = self.get_best_idx()

    def get_parent_str(self):
        return self.parent.get_name()

    def propose_samples_bo(self, num_samples, path, lb, ub, samples):
        proposed_X = self.classifier.propose_samples_bo(num_samples, path, lb, ub, samples)
        return proposed_X

    def propose_sample_de(self, path, func, num_samples=10, de_type='rand', n_init=10):
        assert de_type in ['rand', 'best'], "de_type can only be 'rand' or 'best'"

        samples = copy.deepcopy(self.bag)

        if len(self.population) == 0:
            self.population = np.array([sample[0] for sample in samples])
            self.population_ev = np.array([sample[1] for sample in samples])

        while len(self.population) < n_init:
            sample = self.classifier.propose_rand_samples_sobol(1, path, func.lb, func.ub)[0]
            self.population = np.concatenate((self.population, [sample]))
            self.population_ev = np.concatenate((self.population_ev, [None]))

        if len(self.population) < n_init:
            sorted_idx = np.argsort(self.population_ev)
            self.population = self.population[sorted_idx]
            self.population_ev = self.population_ev[sorted_idx]
            self.population = self.population[:n_init]
            self.population_ev = self.population_ev[:n_init]

        # self.update_bag(samples)

        if de_type == 'rand':
            # proposed_X, fX = self.de_reproduction_sampling(func, num_samples=num_samples)
            proposed_X, fX = self.classifier.propose_sample_de(func, path, num_samples, self.population, self.population_ev)
        else:
            # proposed_X, fX = self.de_reproduction_sampling_best(func, num_samples=num_samples)
            proposed_X, fX = self.classifier.propose_sample_de_best(func, path, num_samples, self.population, self.population_ev)
        fX = fX * -1
        return proposed_X, fX

    def propose_samples_turbo(self, num_samples, path, func):
        proposed_X, fX = self.classifier.propose_samples_turbo(num_samples, path, func)
        return proposed_X, fX

    def propose_samples_pso(self, num_samples, path, func):
        proposed_x, fx = self.classifier.propose_samples_pso(num_samples, path, func)
        # proposed_x, fx = self.pso_sampling(func, path)
        # fx = fx * -1
        return proposed_x, fx

    def propose_samples_rand(self, num_samples):
        assert num_samples > 0
        samples = self.classifier.propose_samples_rand(num_samples)
        return samples

    def __str__(self):
        name = self.get_name()
        name = self.pad_str_to_8chars(name, 7)
        name += (self.pad_str_to_8chars('is good:' + str(self.is_good_kid()), 15))
        name += (self.pad_str_to_8chars('is leaf:' + str(self.is_leaf()), 15))

        val = 0
        name += (self.pad_str_to_8chars(' val:{0:.4f}   '.format(round(self.get_xbar(), 3)), 20))
        name += (self.pad_str_to_8chars(' uct:{0:.4f}   '.format(round(self.get_uct(), 3)), 20))

        name += self.pad_str_to_8chars('sp/n:' + str(len(self.bag)) + "/" + str(self.n), 15)
        upper_bound = np.around(np.max(self.classifier.X, axis=0), decimals=2)
        lower_bound = np.around(np.min(self.classifier.X, axis=0), decimals=2)
        boundary = ''
        for idx in range(0, self.dims):
            boundary += str(lower_bound[idx]) + '>' + str(upper_bound[idx]) + ' '

        # name  += ( self.pad_str_to_8chars( 'bound:' + boundary, 60 ) )

        parent = '----'
        if self.parent is not None:
            parent = self.parent.get_name()
        parent = self.pad_str_to_8chars(parent, 10)

        name += (' parent:' + parent)

        kids = ''
        kid = ''
        for k in self.kids:
            kid = self.pad_str_to_8chars(k.get_name(), 10)
            kids += kid
        name += (' kids:' + kids)

        return name

    def get_uct(self, Cp=10):
        if self.parent == None:
            return float('inf')
        if self.n == 0:
            return float('inf')
        return self.x_bar + 2 * Cp * math.sqrt(2 * np.power(self.parent.n, 0.5) / self.n)

    def get_xbar(self):
        return self.x_bar

    def get_n(self):
        return self.n

    def train_and_split(self):
        assert len(self.bag) >= 2
        self.classifier.update_samples(self.bag)
        good_kid_data, bad_kid_data = self.classifier.split_data()
        assert len(good_kid_data) + len(bad_kid_data) == len(self.bag)
        return good_kid_data, bad_kid_data

    def plot_samples_and_boundary(self, func):
        name = self.get_name() + ".pdf"
        self.classifier.plot_samples_and_boundary(func, name)

    def sample_arch(self):
        if len(self.bag) == 0:
            return None
        net_str = np.random.choice(list(self.bag.keys()))
        del self.bag[net_str]
        return json.loads(net_str)

    # def de_reproduction_sampling(self, func, num_samples=1, mutation_factor=0.8, recombination_prob=0.9):
    #     popsize = self.population.shape[0]
    #
    #     assert self.target_index in list(range(popsize))
    #
    #     trial_vectors = []
    #     trial_evals = []
    #
    #     for i in range(num_samples):
    #
    #         # --- MUTATION (step #3.A) ---------------------+
    #         candidates = list(range(popsize))
    #         candidates.remove(self.target_index)
    #         random_index = random_sample(candidates, 3)
    #
    #         x_1 = self.population[random_index[0]]
    #         x_2 = self.population[random_index[1]]
    #         x_3 = self.population[random_index[2]]
    #         x_t = self.population[self.target_index]  # target individual
    #
    #         # subtract x3 from x2, and create a new vector (x_diff)
    #         x_diff = x_2 - x_3
    #         # multiply x_diff by the mutation factor (F) and add to x_1
    #         v_donor = x_1 + mutation_factor * x_diff
    #         v_donor = de_simple.ensure_bounds(v_donor, func.lb, func.ub)
    #
    #         # --- RECOMBINATION (step #3.B) ----------------+
    #
    #         v_trial = np.where(np.random.random(x_t.shape) <= recombination_prob, v_donor, x_t)
    #
    #         # --- GREEDY SELECTION (step #3.C) -------------+
    #
    #         score_trial = func(v_trial)
    #         score_target = self.population_ev[self.target_index]
    #
    #         if score_trial < score_target:
    #             self.population[self.target_index] = v_trial
    #             print('   >', score_trial, v_trial)
    #         else:
    #             print('   >', score_target, x_t)
    #
    #         trial_vectors.append(v_trial)
    #         trial_evals.append(score_trial)
    #
    #         self.target_index = self.target_index + 1
    #         self.check_target_index()
    #
    #     return np.array(trial_vectors), np.array(trial_evals)

    def de_reproduction_sampling_best(self, func, num_samples=1, mutation_factor=0.8, recombination_prob=0.9):
        popsize = self.population.shape[0]

        assert self.target_index in list(range(popsize))

        trial_vectors = []
        trial_evals = []

        for i in range(num_samples):

            # --- MUTATION (step #3.A) ---------------------+
            candidates = list(range(popsize))
            candidates.remove(self.target_index)
            random_index = random_sample(candidates, 2)

            x_1 = self.get_best_from_current_population()
            x_2 = self.population[random_index[0]]
            x_3 = self.population[random_index[1]]
            x_t = self.population[self.target_index]  # target individual

            # subtract x3 from x2, and create a new vector (x_diff)
            x_diff = x_2 - x_3
            # multiply x_diff by the mutation factor (F) and add to x_1
            v_donor = x_1 + mutation_factor * x_diff
            v_donor = de_simple.ensure_bounds(v_donor, func.lb, func.ub)

            # --- RECOMBINATION (step #3.B) ----------------+

            v_trial = np.where(np.random.random(x_t.shape) <= recombination_prob, v_donor, x_t)

            # --- GREEDY SELECTION (step #3.C) -------------+

            score_trial = func(v_trial)
            score_target = self.population_ev[self.target_index]

            if score_trial < score_target:
                self.population[self.target_index] = v_trial
                self.population[self.target_index] = score_trial
                print('   >', score_trial, v_trial)
            else:
                print('   >', score_target, x_t)

            trial_vectors.append(v_trial)
            trial_evals.append(score_trial)

            self.target_index = self.target_index + 1
            self.check_target_index()

        return trial_vectors, trial_evals

    # def pso_sampling(self, func, path, num_iterations=10, inertia_weight=0.5, cognitive_weight=0.5,
    #                  social_weight=0.5):
    #
    #     n_init = 30
    #
    #     if len(self.particles) == 0:
    #         print("POPULATING PARTICLES")
    #         samples = copy.deepcopy(self.bag)
    #         n_bag = len(samples)
    #         if n_bag > n_init:
    #             samples = sorted(samples, key=lambda x: x[1])[:n_init]
    #         elif n_bag < n_init:
    #             n_add = n_init - n_bag
    #             x_add = self.classifier.propose_rand_samples_sobol(n_add, path, func.lb, func.ub)
    #             x_fx_add = [(x, func(x)*-1) for x in x_add]
    #             samples = samples + x_fx_add
    #
    #         print('len(self.bag)', len(self.bag))
    #         for sample in samples:
    #             self.particles.append(pso.Particle(func, sample[0], sample[1] * -1))
    #             if sample[1] * -1 < self.global_best_fitness:
    #                 self.global_best_fitness = sample[1] * -1
    #                 self.global_best_position = sample[0]
    #
    #     samples = []
    #     sample_evals = []
    #
    #     for _ in range(num_iterations):
    #         print("self.global_best_fitness", self.global_best_fitness)
    #
    #         for particle in self.particles:
    #             particle.update_velocity(self.global_best_position, inertia_weight, cognitive_weight, social_weight)
    #             particle.update_position()
    #
    #         for particle in self.particles:
    #             particle.evaluate_fitness()
    #             if particle.best_fitness < self.global_best_fitness:
    #                 self.global_best_fitness = particle.best_fitness
    #                 self.global_best_position = particle.best_position.copy()
    #                 print("best fitness: ", self.global_best_fitness)
    #                 samples.append(particle.position)
    #                 sample_evals.append(particle.current_fitness)
    #
    #     return np.array(samples), np.array(sample_evals)
# print(root)
#
# with open('features.json', 'r') as infile:
#     data=json.loads( infile.read() )
# samples = {}
# for d in data:
#     samples[ json.dumps(d['feature']) ] = d['acc']
# n1 = Node(samples, root)
# print(n1)
#
# n1 =
