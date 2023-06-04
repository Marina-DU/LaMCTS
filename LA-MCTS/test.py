import random
import numpy as np


def differential_evolution(objective_func, bounds, population_size=50, max_generations=100, mutation_factor=0.8,
                           crossover_probability=0.9):
    num_dimensions = len(bounds)
    population = np.zeros((population_size, num_dimensions))

    # Initialize the population within the specified bounds
    for i in range(population_size):
        for j in range(num_dimensions):
            population[i, j] = random.uniform(bounds[j][0], bounds[j][1])

    # Evaluate the objective function for each individual in the population
    fitness = np.array([objective_func(individual) for individual in population])

    # Main loop
    for generation in range(max_generations):
        for i in range(population_size):
            target = population[i]

            # Select three distinct individuals from the population
            indices = [index for index in range(population_size) if index != i]
            random.shuffle(indices)
            a, b, c = population[indices[0]], population[indices[1]], population[indices[2]]

            # Mutation: Generate a mutant individual
            mutant = a + mutation_factor * (b - c)

            # Crossover: Perform crossover between the target and the mutant
            trial = np.copy(target)
            j_rand = random.randint(0, num_dimensions - 1)  # Random index for crossover
            for j in range(num_dimensions):
                if j == j_rand or random.random() < crossover_probability:
                    trial[j] = mutant[j]

            # Ensure trial is within the specified bounds
            trial = np.clip(trial, bounds[:, 0], bounds[:, 1])

            # Selection: Replace the target with the trial if it has better fitness
            trial_fitness = objective_func(trial)
            if trial_fitness < fitness[i]:
                population[i] = trial
                fitness[i] = trial_fitness

        # Print the best fitness in the current generation
        best_fitness = np.min(fitness)
        print(f"Generation {generation + 1}: Best Fitness = {best_fitness}")

    # Return the best individual and its fitness
    best_index = np.argmin(fitness)
    best_individual = population[best_index]
    best_fitness = fitness[best_index]

    return best_individual, best_fitness
