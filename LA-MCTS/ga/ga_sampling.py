import sys
from random import sample
import numpy as np


def ensure_bounds(vec, lb, ub):
    vec_new = np.minimum(np.maximum(vec, lb), ub)
    return vec_new


def ga_reproduction_sampling(population, population_ev, cost_func, lb, ub, num_samples=10, mutation_prob=0.2,
                             crossover_prob=0.7, tournament_size=3):

    popsize = population.shape[0]



    generations = 1
    max_gen = num_samples*10

    trial_vectors = []
    trial_evals = []
    worst_vectors = []
    worst_evals = []

    while len(trial_vectors) < num_samples and generations <= max_gen:
        print(population)

        # --- SELECTION (step #1) ---------------------+
        selected_indices = np.random.choice(np.arange(popsize), size=tournament_size, replace=False)
        tournament_individuals = population_ev[selected_indices]
        best_index = selected_indices[np.argmin(tournament_individuals)]
        print("best_index",best_index)
        parent_1 = population[best_index]

        selected_indices = np.random.choice(np.arange(popsize), size=tournament_size, replace=False)
        tournament_individuals = population_ev[selected_indices]
        best_index = selected_indices[np.argmin(tournament_individuals)]
        print("best_index",best_index)
        parent_2 = population[best_index]


        # --- CROSSOVER (step #2) ---------------------+
        if np.random.random() < crossover_prob:
            crossover_point = np.random.randint(0, len(parent_1))
            child = np.concatenate([parent_1[:crossover_point], parent_2[crossover_point:]])
        else:
            child = parent_1.copy()  # if no crossover, child is identical to parent

        # --- MUTATION (step #3) ---------------------+
        for i in range(len(child)):
            if np.random.random() < mutation_prob:
                child[i] = 1 - child[i]  # flip bit

        print(parent_1)
        print(parent_2)
        print(child)

        print("b4",child)
        child = ensure_bounds(child, lb, ub)
        print("after",child)

        # --- REPLACEMENT (step #4) ---------------------+
        score_child = cost_func(child)

        # replace if child is better
        worst_index = np.argmax(population_ev)
        if score_child < population_ev[worst_index]:
            population[worst_index] = child
            population_ev[worst_index] = score_child
            trial_vectors.append(child)
            trial_evals.append(score_child)
            print("BETTER:", score_child)
        else:
            worst_vectors.append(population[worst_index])
            worst_evals.append(population_ev[worst_index])
            # print("worse:", score_child)

        generations += 1
    if len(trial_vectors) <= num_samples/10:
        print("BAD NODE")
        indices = np.argsort(worst_evals)[::-1]

        # Sort worst_evals and worst_vectors according to the indices
        n_to_add = round(num_samples/10)

        trial_vectors.append(worst_evals[indices][:n_to_add])
        trial_evals.append(worst_vectors[indices][:n_to_add])



    return np.array(trial_vectors), np.array(trial_evals)
