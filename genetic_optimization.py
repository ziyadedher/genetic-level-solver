import random

GENE_LENGTH = 25
DIRECTIONS = ('U', 'R', 'D', 'L')

class Population:

    def __init__(self, num_individuals):

        self.population = []

        for i in range(num_individuals):
             self.population[i] = Individual()


class Individual:

    def __init__(self):
        """Create a creature with random values"""
        self.fitness = 0
        self.genes = []

        for i in range(GENE_LENGTH):
            self.genes[i] = random.choice(DIRECTIONS)

    def get_fitness(self):
        return self.fitness

    def calculate_fitness(self):
        """Calculates fitness during run on the grid"""


def create_new_generation(population):
    """ Creates a new generation based on favourable characteristics of individuals"""

    new_population = []

    for i in range(population.len):
        parent1 = find_parent(population)
        parent2 = find_parent(population)
        child = crossover(parent1, parent2)
        new_population[i] = child

    return new_population

def find_fittest(population):

    fittest = population[0]

    for individual in population:
        if individual.fitness > fittest.fitness:
            fittest = individual

    return fittest

def find_parent(population):

    tournament_population = []

    for i in range(5):
        tournament_population


