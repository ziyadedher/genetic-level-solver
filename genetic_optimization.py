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


class Population:

    def __init__(self, gene_length, num_creatures):
        """Creates a list of <num_creatures> creatures with randomly
        generated genes.
        """
        self.pop = []
        self.gene_length = gene_length

        for i in range(num_creatures):
            self.pop.append(Creature(self.gene_length))

    def create_new_generation(self):
        """ Creates a new generation based on favourable characteristics
            of creatures.
        """
        new_pop = []
        sorted_pop = sorted(self.pop, key=get_fitness, reverse=True)
        tournament_pop = sorted_pop[:int(len(sorted_pop) * TOP_CREATURES_PERCENTAGE)]

        for i in range(len(self.pop)):
            parent1 = random.choice(tournament_pop)
            parent2 = random.choice(tournament_pop)
            new_child = crossover(parent1, parent2)
            new_pop.append(new_child)

        self.pop = new_pop

    def calculate_average_fitness(self):
        """Calculates the average fitness of a generation of creatures.
        """
        avg_fitness = 0
        for creature in self.pop:
            avg_fitness += creature.fitness

        return avg_fitness / len(self.pop)


class Creature:

    def __init__(self, gene_length):
        """Create a creature with random genes.
        """
        self.fitness = 0
        self.genes = []

        for i in range(gene_length):
            self.genes.append(random.choice(DIRECTIONS))


def get_fitness(creature):
    return creature.fitness


def crossover(parent1, parent2):
    """Returns a child created from two parents.
    """
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