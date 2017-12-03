"""General simulation control.
"""

import os
import sys
import time
import random
import pickle
import pygame

import matplotlib.pyplot as plt

import genetics


# Screen constants
SCREEN_SIZE = (900, 500)
SCREEN_TITLE = "Genetic Level Solver"

# Level constants
TILE_SIZE = 10
LEVEL_PATH = "levels/"

# Calculates how many rows and columns of tiles there will be
NUM_COLUMNS = SCREEN_SIZE[0] // TILE_SIZE
NUM_ROWS = SCREEN_SIZE[1] // TILE_SIZE

# Color constants
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
COLORS = [BLACK, WHITE, GREEN]


class EndSimulation(Exception):
    """Raised when the simulation is ended prematurely.
    """
    pass


class Simulation:
    """Controls the simulation's execution and physics.

    === Public Attributes ===
    display:
        PyGame display
    level:
        current Level
    """

    def __init__(self):
        """Initalizes this simulation along with physics and display.
        """
        # Ask for a level and if to generate random points
        level = self.ask_level()
        chance = self.ask_points()

        # Initializes pygame display with size and title
        pygame.init()
        self.display = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(SCREEN_TITLE)

        # Initializes the level and draws it
        if level == []:
            self.level = Level(chance=chance)
        else:
            self.level = Level(blueprint=level, chance=chance)
        self.level.draw(self.display)

    def ask_level(self):
        """Asks for the level to load.

        Returns an empty array if the level is randomly generated,
        returns an 2-d array if with the level if it is chosen.
        """
        # Stores the level
        level = []

        # Asks the user if they want to load a level
        ans = input("Load a preexisting level? [y/n] ")
        if ans.lower() == 'n':
            return []

        # Makes sure the levels path exists
        if os.path.exists(LEVEL_PATH):
            # Lists the maps in the path
            for item in os.listdir(LEVEL_PATH):
                print(item)

            # Asks for the name
            level = input("Enter a file name of the above, " +
                          "or hit enter to continue: ")

            # If no name was given or the level does not exist, returns
            if level == "":
                return []
            if not os.path.exists(LEVEL_PATH + level):
                input("That is not a level. Press enter to continue. ")
                return []

            # Loads and returns the level if all is well
            return pickle.load(open(LEVEL_PATH + level, "rb"))

        # If the path does not exist, then return
        input("No levels found. Press enter to continue. ")
        return []

    def ask_points(self):
        """Asks if points should be randomly placed and the frequency if yes.

        Returns the frequency float.
        """
        # Asks whether to randomly generate
        ans = input("Randomly generate points? [y/n] ")
        if ans.lower() == "n":
            return 0

        # Asks until a valid input is given.
        prompt = "Frequency (default: 0.025): "
        while True:
            freq = input(prompt)
            # Returns default if no answer was given
            if freq == "":
                return 0.025
            try:
                freq = float(freq)
                if freq < 0.0 or freq > 1.0:
                    raise ValueError
            except ValueError:
                print("Please input a number between 0.0 and 1.0.")
                continue
            else:
                return freq

    def start(self, generations, num_creatures, movements, draw_step=1):
        """Starts the simulation and
        runs for <generations> number of generations with
        <num_creatures> number of creatures
        that move <movements> times before dying.
        Draws the generation every <draw_step>.
        """
        # Stores fitness levels for statistics
        fitness_levels = []

        # Generates a population holder
        populations = genetics.Population(movements, num_creatures)

        # Runs through the amount of generations needed to simulate
        for i in range(generations):
            # Sets the draw to True only on every <draw_step> generation
            draw = (i % draw_step) == 0

            # Gets the current population and creates creatures for each item
            pop = populations.pop
            creatures = [Creature(self.level) for _ in range(len(pop))]

            # Runs through each movement required
            for step_i in range(movements):
                # Tries to step, ends if a EndSimulation exception was raised
                try:
                    self.step(creatures, pop, step_i, draw)
                except EndSimulation:
                    pygame.quit()
                    self.draw_graph(fitness_levels)
                    return

            # Updates each individual's fitness based off the number of points
            # they gathered in that generation
            for j in range(len(creatures)):
                pop[j].fitness = creatures[j].points

            # Appends the average fitness to the fitness level tracker
            fitness_levels.append(populations.calculate_average_fitness())
            # Creates a new generation
            populations.create_new_generation()

        # Draws statistics
        self.draw_graph(fitness_levels)

    def step(self, creatures, pop, step_number, draw):
        """Runs a step in the simulation.

        Updates each creature in <creatures> and only draws if <draw> is True.
        """
        # Draws the level if required
        if draw:
            self.level.draw(self.display)

        # Runs through each creature and moves accordingly
        for i in range(len(creatures)):
            creatures[i].move(pop[i].genes[step_number])
            # Draws the creature if required
            if draw:
                creatures[i].draw(self.display)

        # Close event handler, raises an EndSimulation exception
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise EndSimulation

        # Updates the display to show changes if required
        if draw:
            pygame.display.update()

    def draw_graph(self, fitness_levels):
        """Draws the graph of fitness versus generation.
        """
        # Plots fitness level versus generation
        plt.plot(range(len(fitness_levels)), fitness_levels, 'ro')

        # Sets display labels
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.title("Average Fitness over Generations")
        plt.grid()

        # Shows the plot
        plt.show()


class Level:
    """Level in this simulation.

    Consists of a grid which either contains an empty space, wall, or point.
    """
    # === Private Attributes ===
    # _grid:
    #   2-D array of level tiles
    #   a tile is a number between 0 and 2 inclusive where
    #       0: empty
    #       1: wall
    #       2: point

    def __init__(self, blueprint=None, chance=0.025):
        """Initializes this level with the given blueprint in the form of
        a list of columns where each column is a list of integers. Adds the
        points randomly depending on <chance>.

        - 0 represents a empty block
        - 1 represents a wall
        - 2 represents a point
        """
        # Generates the grid depending on the given blueprint
        if blueprint is None:
            self._grid = self._generate_empty_grid()
        else:
            self._grid = blueprint

        # Adds points if required
        self.add_points(chance)

    def _generate_empty_grid(self):
        """Generates an empty grid.
        """
        # Generates the grid and returns it
        grid = []
        for x in range(NUM_COLUMNS):
            column = [0] * NUM_ROWS
            grid.append(column)
        return grid

    def _generate_boxed_grid(self):
        """Generates a grid with walls only at the sides.
        """
        # Generates the grid and returns it
        grid = []
        for x in range(NUM_COLUMNS):
            if x == 0 or x == NUM_COLUMNS - 1:
                column = [1] * NUM_ROWS
            else:
                column = [1] + [0] * (NUM_ROWS - 2) + [1]
            grid.append(column)
        return grid

    def add_points(self, chance):
        """Randomly scatters points across the empty tiles of the level
        at the rate of <chance>.
        """
        # Runs through each tile
        for x in range(len(self._grid)):
            for y in range(len(self._grid[x])):
                # Makes sure it is empty
                if self._grid[x][y] == 0:
                    # Randomly chooses whether to make it a point
                    if random.random() < chance:
                        self._grid[x][y] = 2

    def draw(self, display):
        """Draws this level to the given PyGame display.
        """
        # Draws each tile in the grid
        for x in range(len(self._grid)):
            for y in range(len(self._grid[x])):
                # Calculates the left and top
                left = x * TILE_SIZE
                top = y * TILE_SIZE

                # Creates the rectangle and chooses the color
                tile_rect = pygame.Rect(left, top, TILE_SIZE, TILE_SIZE)
                color = COLORS[self._grid[x][y]]

                # Draws the rectangle
                pygame.draw.rect(display, color, tile_rect)

    def get_tile_at(self, position):
        """Gets the tile at the given position.

        Returns the integer representation.
        """
        return self._grid[position[0]][position[1]]

    def set_tile_at(self, position, tile):
        """Sets the tile at the given position to the integer representation.
        """
        self._grid[position[0]][position[1]] = tile

    def dump_grid(self, save):
        """Dumps the grid into a save file using Pickle.
        """
        pickle.dump(self._grid, save)


class Creature:
    """Creature in the simulation.

    === Public Attributes ===
    level:
        Level this creature is in
    points:
        number of points this creature has collected
    """
    # === Private Attributes ===
    # _x:
    #   x-coordinate of the creature
    # _y:
    #   y-coordinate of the creature
    # _visited:
    #   list of tuples of visited points

    def __init__(self, level):
        """Initializes the creature in the given level.
        """
        # Initializes the level and the number of points
        self.level = level
        self.points = 0

        # Sets the position to the middle and sets that to be a visited place
        self._x = NUM_COLUMNS // 2
        self._y = NUM_ROWS // 2
        self._visited = [(self._x, self._y)]

    def _try_move(self, displacement):
        """Try to move a certain displacement, update accordingly.
        """
        # Gets the move to position and loops the board if the end is hit
        move_x = (self._x + displacement[0]) % NUM_COLUMNS
        move_y = (self._y + displacement[1]) % NUM_ROWS

        # Gets the tile at the position to move to
        status = self.level.get_tile_at((move_x, move_y))

        # Moves there if it is not a wall
        if status != 1:
            self._x = move_x
            self._y = move_y

        # Collects the point if it is a point
        if status == 2:
            pos = (self._x, self._y)
            # Updates if this point has not been collected by this creature
            if pos not in self._visited:
                self._visited.append(pos)
                self.points += 1

    def move(self, direction):
        """Moves the creature in the given direction (U, R, D, or L).
        """
        if direction == 'U':
            self._try_move((0, -1))
        elif direction == 'R':
            self._try_move((1, 0))
        elif direction == 'D':
            self._try_move((0, 1))
        elif direction == 'L':
            self._try_move((-1, 0))

    def draw(self, display):
        """Draws this creature to the given PyGame display.
        """
        # Calculates the left and top
        left = self._x * TILE_SIZE
        top = self._y * TILE_SIZE

        # Creates the rectangle and chooses the color
        tile_rect = pygame.Rect(left, top, TILE_SIZE, TILE_SIZE)
        color = RED

        # Draws the rectangle
        pygame.draw.rect(display, color, tile_rect)
