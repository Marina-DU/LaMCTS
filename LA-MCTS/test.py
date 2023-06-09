from pso import particle
from functions.functions import *


dimensions = 2
# lower_bound = -10
# upper_bound = 10
num_particles = 30
num_iterations = 640

f = Rosenbrock(dims=dimensions)

best_position, best_fitness = particle.particle_swarm_optimization(f, num_iterations, num_particles)


print("Best position:", best_position)
print("Best fitness:", best_fitness)


