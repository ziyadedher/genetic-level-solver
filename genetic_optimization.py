import random

GENE_LENGTH = 25
DIRECTIONS = ('U', 'R', 'D', 'L')

class Population:

    def __init__(self, num_individuals):
        """Creates  a list of individuals with randomly generated genes"""

        self.population = []

        for i in range(num_individuals):
             self.population[i] = Individual()

    def create_new_generation(self):
        """ Creates a new generation based on favourable characteristics of individuals"""

        new_population = []

        for i in range(len(self.population)):
            parent1 = find_parent(self.population)
            parent2 = find_parent(self.population)
            child = crossover(parent1, parent2)
            new_population[i] = child

        self.population = new_population


class Individual:

    def __init__(self):
        """Create a creature with random values"""
        self.fitness = 0
        self.genes = []

        for i in range(GENE_LENGTH):
            self.genes[i] = random.choice(DIRECTIONS)

    # Getter
    def get_fitness(self):
        return self.fitness

    def calculate_fitness(self):
        """Calculates fitness during run on the grid"""

def crossover(parent1, parent2):


def find_fittest(population):
    """Returns the fittest individual in a population"""
    fittest = population[0]

    for individual in population:
        if individual.fitness > fittest.fitness:
            fittest = individual

    return fittest

def find_parent(population):
    """Returns a parent used for creating a child"""

    tournament_population = []

    for i in range(5):
        tournament_population[i] = random.choice(population)

    return find_fittest(tournament_population)



