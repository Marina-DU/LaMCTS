# ------------------------------------------------------------------------------+
#
#   Nathan A. Rooy
#   A simple, bare bones, implementation of differential evolution with Python
#   August, 2017
#
# ------------------------------------------------------------------------------+
import sys

# --- IMPORT DEPENDENCIES ------------------------------------------------------+
import numpy as np
from random import random
from random import sample
from random import uniform


# --- FUNCTIONS ----------------------------------------------------------------+


def ensure_bounds(vec, lb, ub):
    vec_new = np.minimum(np.maximum(vec, lb), ub)
    return vec_new


# --- MAIN ---------------------------------------------------------------------+

def minimize(cost_func, lb, ub, population: np.array, mutation_factor=0.8, recombination_prob=0.9, generations=100):
    # --- INITIALIZE A POPULATION (step #1) ----------------+
    assert len(lb) == len(ub)

    popsize = population.shape[0]

    # --- SOLVE --------------------------------------------+

    # cycle through each generation (step #2)
    for i in range(generations):
        print("GENERATION:", i + 1)

        gen_scores = de_reproduction(population, cost_func, mutation_factor, recombination_prob, lb, ub)
        # select three random vector index positions [0, popsize), not including current vector (j)

        # --- SCORE KEEPING --------------------------------+
        gen_avg = sum(gen_scores) / popsize  # current generation avg. fitness
        gen_best = min(gen_scores)  # fitness of best individual
        gen_sol = population[np.argmin(gen_scores)]  # solution of best individual

        print('      > GENERATION AVERAGE:', gen_avg)
        print('      > GENERATION BEST:', gen_best)
        print('         > BEST SOLUTION:', gen_sol, '\n')

    pass


# --- CONSTANTS ----------------------------------------------------------------+


def de_reproduction_sampling(population, population_ev, cost_func, lb, ub, num_samples=10, mutation_factor=0.8,
                             recombination_prob=0.9):
    popsize = population.shape[0]

    target_index = 0
    trial_vectors = []
    trial_evals = []
    generations = 1
    max_gen = min(50 * 10 ** (0.006 * num_samples), 10000)

    while len(trial_vectors) < num_samples and generations <= max_gen:

        # --- MUTATION (step #3.A) ---------------------+
        candidates = list(range(popsize))
        candidates.remove(target_index)
        random_index = sample(candidates, 3)

        x_1 = population[random_index[0]]
        x_2 = population[random_index[1]]
        x_3 = population[random_index[2]]
        x_t = population[target_index]  # target individual

        # subtract x3 from x2, and create a new vector (x_diff)
        x_diff = x_2 - x_3
        # multiply x_diff by the mutation factor (F) and add to x_1
        v_donor = x_1 + mutation_factor * x_diff
        v_donor = ensure_bounds(v_donor, lb, ub)

        # --- RECOMBINATION (step #3.B) ----------------+

        v_trial = np.where(np.random.random(x_t.shape) <= recombination_prob, v_donor, x_t)

        # --- GREEDY SELECTION (step #3.C) -------------+

        score_trial = cost_func(v_trial)
        score_target = population_ev[target_index] if population_ev[target_index] is not None else cost_func(x_t)

        if score_trial < score_target:
            population[target_index] = v_trial
            population_ev[target_index] = score_trial
            print(f'better: trial {score_trial} target {score_target}')
            print(x_t)
            trial_vectors.append(v_trial)
            trial_evals.append(score_trial)
        else:
            print(f'worse: trial {score_trial} target {score_target}')
            print(x_t)

        target_index += 1
        if target_index >= popsize:
            print("generation ", generations)
            generations += 1
            target_index = 0

    return np.array(trial_vectors), np.array(trial_evals)


def de_best_reproduction_sampling(population, population_ev, cost_func, lb, ub, num_samples=10, mutation_factor=0.8,
                                  recombination_prob=0.9):
    popsize = population.shape[0]

    for idx in range(len(population_ev)):
        if population_ev[idx] is None:
            population_ev[idx] = cost_func(population[idx])

    target_index = 0
    trial_vectors = []
    trial_evals = []
    generations = 1
    max_gen = min(50 * 10 ** (0.006 * num_samples), 10000)

    while len(trial_vectors) < num_samples and generations <= max_gen:

        # --- MUTATION (step #3.A) ---------------------+
        candidates = list(range(popsize))
        candidates.remove(target_index)
        random_index = sample(candidates, 2)

        x_1 = population[min(enumerate(population_ev), key=lambda x: x[1])[0]]
        x_2 = population[random_index[0]]
        x_3 = population[random_index[1]]
        x_t = population[target_index]  # target individual

        # subtract x3 from x2, and create a new vector (x_diff)
        x_diff = x_2 - x_3
        # multiply x_diff by the mutation factor (F) and add to x_1
        v_donor = x_1 + mutation_factor * x_diff
        v_donor = ensure_bounds(v_donor, lb, ub)

        # --- RECOMBINATION (step #3.B) ----------------+

        v_trial = np.where(np.random.random(x_t.shape) <= recombination_prob, v_donor, x_t)

        # --- GREEDY SELECTION (step #3.C) -------------+

        score_trial = cost_func(v_trial)
        score_target = population_ev[target_index]

        if score_trial < score_target:
            population[target_index] = v_trial
            population_ev[target_index] = score_trial
            print(f'better: trial {score_trial} target {score_target}')
            print(x_t)
            trial_vectors.append(v_trial)
            trial_evals.append(score_trial)
        else:
            print(f'worse: trial {score_trial} target {score_target}')
            print(x_t)

        target_index += 1
        if target_index >= popsize:
            print("generation ", generations)
            generations += 1
            target_index = 0

    return np.array(trial_vectors), np.array(trial_evals)


def de_sampling(population: np.array, lb, ub, mutation_factor=0.8, recombination_prob=0.9):
    popsize = population.shape[0]
    trial_vectors = []

    for j in range(popsize):
        # --- MUTATION (step #3.A) ---------------------+
        candidates = list(range(popsize))
        candidates.remove(j)
        random_index = sample(candidates, 3)

        x_1 = population[random_index[0]]
        x_2 = population[random_index[1]]
        x_3 = population[random_index[2]]
        x_t = population[j]  # target individual

        # subtract x3 from x2, and create a new vector (x_diff)
        x_diff = x_2 - x_3
        # multiply x_diff by the mutation factor (F) and add to x_1
        v_donor = x_1 + mutation_factor * x_diff
        v_donor = ensure_bounds(v_donor, lb, ub)

        # --- RECOMBINATION (step #3.B) ----------------+

        v_trial = np.where(np.random.random(x_t.shape) <= recombination_prob, v_donor, x_t)

        trial_vectors.append(v_trial)

    return trial_vectors


def de_reproduction(population, cost_func, mutation_factor, recombination_prob, lb, ub):
    popsize = population.shape[0]
    gen_scores = []

    for j in range(popsize):

        # --- MUTATION (step #3.A) ---------------------+
        candidates = list(range(popsize))
        candidates.remove(j)
        random_index = sample(candidates, 3)

        x_1 = population[random_index[0]]
        x_2 = population[random_index[1]]
        x_3 = population[random_index[2]]
        x_t = population[j]  # target individual

        # subtract x3 from x2, and create a new vector (x_diff)
        x_diff = x_2 - x_3
        # multiply x_diff by the mutation factor (F) and add to x_1
        v_donor = x_1 + mutation_factor * x_diff
        v_donor = ensure_bounds(v_donor, lb, ub)

        # --- RECOMBINATION (step #3.B) ----------------+

        v_trial = np.where(np.random.random(x_t.shape) <= recombination_prob, v_donor, x_t)

        # --- GREEDY SELECTION (step #3.C) -------------+

        score_trial = cost_func(v_trial)
        score_target = cost_func(x_t)

        if score_trial < score_target:
            population[j] = v_trial
            gen_scores.append(score_trial)
            print('   >', score_trial, v_trial)
        else:
            print('   >', score_target, x_t)
            gen_scores.append(score_target)

    return gen_scores
