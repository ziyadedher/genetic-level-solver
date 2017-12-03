"""Brains of the operation, controls all genetic algorithm stuff.
This is what makes things happen.
"""


import random


# Directions that a creature can move
DIRECTIONS = ('U', 'R', 'D', 'L')

# Percentage of creatures to be used to create the next generation
TOP_CREATURES_PERCENTAGE = 0.20

# Threshold which determines if a random gene should be created for a child
MUTATION_THRESHOLD = 0.02

# Threshold which determines which parent a child should take a gene from
# (equal chance for both parents)
CROSSOVER_THRESHOLD = (1 + MUTATION_THRESHOLD) / 2


class PopulationController:
    """Controls the populations that go through the genetic algorithm.

    === Public Attributes ===
    pop:
        current population, which is a list of individuals
    gene_length:
        length of the genes, which is the amount of moves
    """
    def __init__(self, gene_length, num_individuals):
        """Creates a list of <num_individuals> creatures with randomly
        generated genes of length <gene_length>.
        """
        self.pop = []
        self.gene_length = gene_length

        # Creates individuals based off how many creatures are required
        for _ in range(num_individuals):
            self.pop.append(Individual(self.gene_length))

    def create_new_generation(self):
        """ Creates a new generation based on favourable characteristics
        of creatures.
        """
        # Sorts the current population and gets a top percentage to compete
        sorted_pop = sorted(self.pop, key=lambda x: x.fitness, reverse=True)
        tournament = sorted_pop[:int(len(self.pop) * TOP_CREATURES_PERCENTAGE)]

        # Empties the population to create a new set
        self.pop = []

        # Creates a new set of individuals by randomly choosing
        # two parents from the tournament set and crossing them
        for _ in range(len(sorted_pop)):
            child = crossover(random.choice(tournament),
                              random.choice(tournament),
                              self.gene_length)
            self.pop.append(child)

    def calculate_fitness_statistics(self):
        """Calculates fitness statistics of the current population.

        Returns a tuple of the maximum, minimum, and average fitness of the
        current population.
        """
        # Sets up for statistic calculation
        max_fit = self.pop[0].fitness
        min_fit = self.pop[0].fitness
        tot_fit = 0

        for ind in self.pop:
            # Sums up for average
            tot_fit += ind.fitness

            # Gets minimums and maximums
            fit = ind.fitness
            if fit > max_fit:
                max_fit = fit
            if fit < min_fit:
                min_fit = fit

        # Returns the tuple as stated
        return (max_fit, min_fit, tot_fit / len(self.pop))


class Individual:
    """Single individual in a population.

    === Public Attributes ===
    fitness:
        measure of how well this individual has done
    genes:
        this individual's genes, which are the moves it will take
    """
    def __init__(self, gene_length):
        """Initializes a creature with random genes.
        """
        self.fitness = 0
        self.genes = []

        # Runs through the number of movements and assigns a random one
        for _ in range(gene_length):
            self.genes.append(random.choice(DIRECTIONS))


def crossover(parent1, parent2, gene_length):
    """Returns a child created from two parents by crossing over their genes.
    """
    child = Individual(gene_length)

    # Assigns parents' (or random) genes to the new child
    for i in range(len(parent1.genes)):
        rand = random.random()
        if rand <= MUTATION_THRESHOLD:
            child.genes[i] = random.choice(DIRECTIONS)
        elif rand <= CROSSOVER_THRESHOLD:
            child.genes[i] = parent1.genes[i]
        else:
            child.genes[i] = parent2.genes[i]

    return child
