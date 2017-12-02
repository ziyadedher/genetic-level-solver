import random

# Directions that a creature can move
DIRECTIONS = ('U', 'R', 'D', 'L')

# Length of a creature's genes (directions)
GENE_LENGTH = 100

# Percentage of creatures to be used to create the next generation
TOP_CREATURES_PERCENTAGE = 0.20

# Threshold which determines if a random gene should be created for a child
MUTATION_THRESHOLD = 0.08

# Threshold which determines which parent a child should take a gene from
# (equal chance for both parents)
CROSSOVER_THRESHOLD = (1 + MUTATION_THRESHOLD) / 2


class Population:

    def __init__(self, num_creatures=1):
        """Creates a list of <num_creatures> creatures with randomly
        generated genes.
        """
        self.pop = []

        for i in range(num_creatures):
            self.pop.append(Creature())

    def create_new_generation(self):
        """ Creates a new generation based on favourable characteristics
            of creatures.
        """
        new_pop = []
        sorted_pop = sorted(self.pop, key=get_fitness)
        tournamet_pop = sorted_pop[0:len(sorted_pop) * TOP_CREATURES_PERCENTAGE]

        for i in range(len(self.pop)):
            parent1 = random.choice(tournamet_pop)
            parent2 = random.choice(tournamet_pop)
            new_child = crossover(parent1, parent2)
            new_pop.append(new_child)

        self.pop = new_pop

    def calculate_average_fitness(self):
        """Calculates the average fitness of a generation of creatures"""
        avg_fitness = 0
        for creature in self.pop:
            avg_fitness += creature.fitness

        return avg_fitness / len(self.pop)


class Creature:

    def __init__(self):
        """Create a creature with random genes."""
        self.fitness = 0
        self.genes = []

        for i in range(GENE_LENGTH):
            self.genes.append(random.choice(DIRECTIONS))


def get_fitness(creature):
    return creature.fitness

# def find_fittest(pop):
#     """Returns the fittest creature in a given population."""
#     fittest = pop[0]
#
#     for creature in pop:
#         if creature.fitness > fittest.fitness:
#             fittest = creature
#
#     return fittest


def crossover(parent1, parent2):
    """Returns a child created from two parents."""
    new_child = Creature()

    # Assigns parents' (or random) genes to the new child
    for i in range(len(parent1.genes)):
        random_num = random.random()
        if random_num <= MUTATION_THRESHOLD:
            new_child.genes[i] = random.choice(DIRECTIONS)
        elif random_num <= CROSSOVER_THRESHOLD:
            new_child.genes[i] = parent1.genes[i]
        else:
            new_child.genes[i] = parent2.genes[i]

    return new_child