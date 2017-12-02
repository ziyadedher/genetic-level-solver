import random
import simulation

GENE_LENGTH = 25                  # Length of an individual's genes (directions)
DIRECTIONS = ('U', 'R', 'D', 'L') # Directions that an individual can move
CROSSOVER_THRESHOLD = 0.5         # Threshold which determines which parent to
                                  # take a gene from
MUTATION_THRESHOLD = 0.08         # Threshold which determines if a random gene
                                  # should be created for a child


class Population:

    def __init__(self, num_individuals=1):
        """Creates  a list of individuals with randomly generated genes."""
        self.population = []

        for i in range(num_individuals):
             self.population.append(Individual())

    def create_new_generation(self):
        """ Creates a new generation based on favourable characteristics
            of individuals.
        """
        new_population = []

        for i in range(len(self.population)):
            parent1 = find_parent(self.population)
            parent2 = find_parent(self.population)
            new_child = crossover(parent1, parent2)
            new_population.append(new_child)

        self.population = new_population


class Individual:

    def __init__(self):
        """Create an individual with random genes."""
        self.fitness = 0
        self.genes = []

        for i in range(GENE_LENGTH):
            self.genes.append(random.choice(DIRECTIONS))


def find_parent(population):
    """Returns a parent used for creating a child."""
    tournament_population = []

    for i in range(5):
        tournament_population[i] = random.choice(population)

    return find_fittest(tournament_population)


def find_fittest(population):
    """Returns the fittest individual in a given population."""
    fittest = population[0]

    for individual in population:
        if individual.fitness > fittest.fitness:
            fittest = individual

    return fittest


def crossover(parent1, parent2):
    """Returns a child created from two parents."""
    new_child = Individual()

    # Assigns parents' (or random) genes to the new child
    for i in range(len(parent1.genes)):
        random_num = random.random()
        if random_num <= MUTATION_THRESHOLD:
            new_child.genes[i] = random.choice(DIRECTIONS)
        elif random.random <= CROSSOVER_THRESHOLD:
            new_child.genes[i] = parent1.genes[i]
        else:
            new_child.genes[i] = parent2.genes[i]

    return new_child