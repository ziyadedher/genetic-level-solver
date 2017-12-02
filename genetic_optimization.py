import random

# Directions that a creature can move
DIRECTIONS = ('U', 'R', 'D', 'L')

# Length of a creature's genes (directions)
GENE_LENGTH = 100

# Number of creatures that compete to become the parent of a new child
NUM_TOURNAMENT_CREATURES = 5

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
        self.population = []

        for i in range(num_creatures):
            self.population.append(Creature())

    def create_new_generation(self):
        """ Creates a new generation based on favourable characteristics
            of creatures.
        """
        new_population = []

        for i in range(len(self.population)):
            parent1 = find_parent(self.population)
            parent2 = find_parent(self.population)
            new_child = crossover(parent1, parent2)
            new_population.append(new_child)

        self.population = new_population

    def calculate_average_fitness(self):
        """Calculates the average fitness of a generation of creatures"""
        avg_fitness = 0
        for creature in self.population:
            avg_fitness += creature.fitness

        return avg_fitness / len(self.population)


class Creature:

    def __init__(self):
        """Create a creature with random genes."""
        self.fitness = 0
        self.genes = []

        for i in range(GENE_LENGTH):
            self.genes.append(random.choice(DIRECTIONS))


def find_parent(population):
    """Returns a parent used for creating a child."""
    tournament_population = []

    for i in range(NUM_TOURNAMENT_CREATURES):
        tournament_population.append(random.choice(population))

    return find_fittest(tournament_population)


def find_fittest(population):
    """Returns the fittest creature in a given population."""
    fittest = population[0]

    for creature in population:
        if creature.fitness > fittest.fitness:
            fittest = creature

    return fittest


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