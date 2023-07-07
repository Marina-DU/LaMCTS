import numpy as np


class Particle:
    def __init__(self, func, position: np.array = None, current_fitness=None):
        if position is None:
            self.position = np.random.uniform(func.lb, func.ub, func.dims)
        else:
            self.position = position
        self.current_fitness = current_fitness
        self.velocity = np.random.uniform(-1, 1, func.dims)
        self.best_position = self.position.copy()
        self.best_fitness = float('inf') if current_fitness is None else current_fitness
        self.func = func

    def update_velocity(self, global_best_position, inertia_weight, cognitive_weight, social_weight):
        for i in range(len(self.velocity)):
            r1 = np.random.random(self.velocity.shape)
            r2 = np.random.random(self.velocity.shape)
            cognitive_component = cognitive_weight * r1 * (self.best_position - self.position)
            social_component = social_weight * r2 * (global_best_position - self.position)
            self.velocity = inertia_weight * self.velocity + cognitive_component + social_component

    def update_position(self):
        self.position = self.position + self.velocity
        self.position = np.clip(self.position, self.func.lb, self.func.ub)

    def evaluate_fitness(self):
        fitness = self.func(self.position)
        self.current_fitness = fitness
        if fitness < self.best_fitness:
            self.best_fitness = fitness
            self.best_position = self.position.copy()
        return fitness


def particle_swarm_optimization(func, num_iterations, num_particles=30, inertia_weight=0.5, cognitive_weight=0.5,
                                social_weight=0.5):
    particles = [Particle(func) for _ in range(num_particles)]
    global_best_fitness = float('inf')
    global_best_position = None

    for _ in range(num_iterations):
        for particle in particles:
            particle.evaluate_fitness()
            if particle.best_fitness < global_best_fitness:
                global_best_fitness = particle.best_fitness
                global_best_position = particle.best_position.copy()
                print("best fitness: ", global_best_fitness)

        for particle in particles:
            particle.update_velocity(global_best_position, inertia_weight, cognitive_weight, social_weight)
            particle.update_position()

    return global_best_position, global_best_fitness


def pso_sampling(population, population_ev, cost_func, num_samples=10, inertia=0.5, cognitive=2.0, social=2.0):

    swarm = []
    initial_population = population.copy()
    for idx in range(len(population_ev)):
        if population_ev[idx] is None:
            swarm.append(Particle(cost_func, population[idx], cost_func(population[idx])))
        else:
            swarm.append(Particle(cost_func, population[idx], population_ev[idx]))

    global_best_fitness = float('inf')
    global_best_position = None
    samples = []
    sample_evals = []
    num_iterations = 0
    max_iterations = min(50 * 10 ** (0.006 * num_samples), 10000)

    while len(sample_evals) < num_samples and num_iterations < max_iterations:
        num_iterations += 1
        for particle in swarm:
            # we already have the fitness on the first iteration
            if num_iterations != 1:
                particle.evaluate_fitness()


            if particle.best_fitness < global_best_fitness:
                if particle.best_position not in initial_population:
                    sample_evals.append(particle.current_fitness)
                    samples.append(particle.position)

                print("NEW BEST FITNESS: ", particle.best_fitness)
                print("OLD BEST FITNESS: ", global_best_fitness)
                global_best_fitness = particle.best_fitness
                global_best_position = particle.best_position.copy()
                assert particle.current_fitness == particle.best_fitness

            else:
                print("WROSE PSO")
                print("particle.best_fitness: ", particle.best_fitness)
                print("global_best_fitness: ", global_best_fitness)


        for particle in swarm:
            particle.update_velocity(global_best_position, inertia, cognitive, social)
            particle.update_position()

    return np.array(samples), np.array(sample_evals)
