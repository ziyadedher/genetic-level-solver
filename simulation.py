"""General simulation control.
"""

import os
import time
import random
import pickle
import pygame

import matplotlib.pyplot as plt

import genetic_optimization as genetics


# Screen constants
SCREEN_SIZE = (900, 500)
SCREEN_TITLE = "Genetic Level Solver"

# Level constants
TILE_SIZE = 10

# Calculates how many rows and columns of tiles there will be
NUM_COLUMNS = SCREEN_SIZE[0] // TILE_SIZE
NUM_ROWS = SCREEN_SIZE[1] // TILE_SIZE

# Color constants
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
COLORS = [BLACK, WHITE, GREEN]


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
        # Initializes pygame display
        pygame.init()
        self.display = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(SCREEN_TITLE)

        # Initializes the level
        level = self.ask_level()
        if level == []:
            self.level = Level()
        else:
            self.level = Level(level)
        self.level.draw(self.display)

    def ask_level(self):
        """Asks for the level to load.
        """
        path = "levels/"
        level = []

        if os.path.exists(path):
            os.listdir(path)
            level = input("Enter a file name of the above, or hit enter to generate.")
        else:
            input("No levels found. Press enter to generate.")
            return []

        if not os.path.exists(path + level):
            input("That is not a level. Press enter to generate.")
            return []

        return pickle.load(open(path + level, "rb"))

    def start(self, generations, num_creatures, movements, draw_step=1):
        """Starts the simulation and
        runs for <generations> number of generations with
        <num_creatures> number of creatures.
        Draws the generation every <draw_step>.
        """
        fitness_levels = []
        populations = genetics.Population(movements, num_creatures)

        for i in range(generations):
            draw = (i % draw_step) == 0
            pop = populations.pop
            creatures = [Creature(self.level) for _ in range(len(pop))]

            for step_i in range(movements):
                self.step(creatures, pop, step_i, draw)
            for j in range(len(creatures)):
                pop[j].fitness = creatures[j].points

            fitness_levels.append(populations.calculate_average_fitness())
            populations.create_new_generation()

        self.draw_graph(fitness_levels)

    def step(self, creatures, pop, step_number, draw):
        """Runs a step in the simulation.
        """
        if draw:
            self.level.draw(self.display)
        for i in range(len(creatures)):
            creatures[i].move(pop[i].genes[step_number])
            if draw:
                creatures[i].draw(self.display)
        pygame.display.update()

    def draw_graph(self, fitness_levels):
        """Draws the graph of fitness versus generation.
        """
        plt.plot(range(len(fitness_levels)), fitness_levels, 'ro')
        plt.show()


class Level:
    """Level in this simulation.
    """
    # === Private Attributes ===
    # _grid:
    #   2-D array of level tiles
    #   a tile is a number between 0 and 2 inclusive where
    #       0: empty
    #       1: wall
    #       2: point

    def __init__(self, blueprint=None, points=True):
        """Initializes this level with the given blueprint in the form of
        a list of columns where each column is a list of integers. Adds
        points randomly if points is set to True.

        - 0 represents a empty block
        - 1 represents a wall
        - 2 represents a point
        """
        # Generates the grid
        if blueprint is None:
            self._grid = self._generate_boxed_grid()
        else:
            self._grid = blueprint

        if points:
            self.add_points()

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

    def add_points(self):
        """Randomly scatters points across the empty tiles of the level.
        """
        chance = 0.03

        for x in range(len(self._grid)):
            for y in range(len(self._grid[x])):
                if self._grid[x][y] == 0:
                    rand = random.random()
                    if rand < chance:
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
        self.level = level
        self.points = 0

        self._x = NUM_COLUMNS // 2
        self._y = NUM_ROWS // 2
        self._visited = [(self._x, self._y)]

    def _try_move(self, displacement):
        """Try to move a certain displacement, update accordingly.
        """
        move_x = (self._x + displacement[0]) % NUM_COLUMNS
        move_y = (self._y + displacement[1]) % NUM_ROWS
        status = self.level.get_tile_at((move_x, move_y))

        if status != 1:
            self._x = move_x
            self._y = move_y
        if status == 2:
            pos = (self._x, self._y)
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


if __name__ == '__main__':
    sim = Simulation()
    sim.start(250, 100, 200, draw_step=10)
