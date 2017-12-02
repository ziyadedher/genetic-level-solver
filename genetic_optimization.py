import random

MAX_NODES = 5
GENE_LENGTH = 64

class Population:

    def __init__(self, num_individuals):
        individuals = []

        for i in range(num_individuals):
             individuals[i] = Individual()




class Individual:

    def __init__(self):
        """Create a creature with random values"""
        fitness = 0
        genes = []

        for i in range(GENE_LENGTH):
            genes[i] = random.randint(0,1)

    def calculate_fitness(self):
        """create fitness function"""


def create_new_generation():
    """ Creates a new generation based on favourable characteristics of individuals"""


