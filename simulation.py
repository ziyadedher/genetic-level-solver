"""General simulation control.
"""

import os
import time
import random
import pickle

from typing import List, Tuple, BinaryIO

import pygame
import pygame.gfxdraw

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

# Drawing constants
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
    step_num:
        current step number in the simulation
    """
    display: pygame.Surface
    level: 'Level'
    step_num: int

    # === Private Attributes ===
    # _draw_step:
    #   draws the generation's progress every this many generations
    # _interval:
    #   waits this long after each drawing in milliseconds
    _draw_step: int
    _interval: int

    def __init__(self) -> None:
        """Initalizes this simulation along with physics and display.
        """
        # Ask for a level and if to generate random points
        level = ask_level()
        chance = ask_points()

        # Initializes basic variables
        self.step_num = 0
        self._draw_step = 0
        self._interval = 0

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
        pygame.display.update()

    def settings(self, draw_step: int = 1, interval: int = 0) -> None:
        """Update drawing settings.

        Draws the generation every <draw_step> generations.
        Waits <interval> milliseconds after every draw.
        """
        self._draw_step = draw_step
        self._interval = interval

    def start(self, generations: int, num_creatures: int,
              movements: int) -> None:
        """Starts the simulation and
        runs for <generations> number of generations with
        <num_creatures> number of creatures
        that move <movements> times before dying.
        """
        # Stores fitness levels for statistics
        fitness_levels = []

        # Generates a population holder
        populations = genetics.PopulationController(movements, num_creatures)

        # Runs through the amount of generations needed to simulate
        for i in range(generations):
            # Resets step number to zero at the start
            self.step_num = 0

            # Sets the draw to True only on every <draw_step> generation
            if self._draw_step != 0:
                draw = (i % self._draw_step) == 0
            else:
                draw = False

            # Gets the current population and creates creatures for each item
            pop = populations.pop
            creatures = [Creature(self.level) for _ in range(len(pop))]

            # Runs through each movement required
            while self.step_num < movements:
                # Tries to step, ends if a EndSimulation exception was raised
                try:
                    self.step(creatures, pop)
                except EndSimulation:
                    pygame.quit()
                    draw_graph(fitness_levels)
                    return

                # Draws everything if draw is set to true
                if draw:
                    self.draw(creatures, self._interval)

            # Updates each individual's fitness based off the number of points
            # they gathered in that generation
            for j, ind in enumerate(pop):
                ind.fitness = creatures[j].points

            # Appends the fitness statistics to the fitness level tracker
            fitness_levels.append(populations.calculate_fitness_statistics())
            # Creates a new generation
            populations.create_new_generation()

        # Draws statistics
        draw_graph(fitness_levels)

    def step(self, creatures: List['Creature'],
             pop: List[genetics.Individual]) -> None:
        """Runs a step in the simulation.

        Updates each creature in <creatures>.
        """
        # Runs through each creature and moves accordingly
        for i, creature in enumerate(creatures):
            creature.move(pop[i].genes[self.step_num])

        # Close event handler, raises an EndSimulation exception
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise EndSimulation

        # Increments step
        self.step_num += 1

    def draw(self, creatures: List['Creature'], interval: int = 0) -> None:
        """Draws the level and all the passed in creatures,
        then waits <interval> milliseconds.
        """
        # Draws the level
        self.level.draw(self.display)

        # Draws the creatures
        for creature in creatures:
            creature.draw(self.display)

        # Updates the display and waits
        pygame.display.update()
        time.sleep(interval / 1000)


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
    _grid: List[List[int]]

    def __init__(self, blueprint: List[List[int]] = None,
                 chance: float = 0.025) -> None:
        """Initializes this level with the given blueprint in the form of
        a list of columns where each column is a list of integers. Adds the
        points randomly depending on <chance>.

        - 0 represents a empty block
        - 1 represents a wall
        - 2 represents a point
        """
        # Generates the grid depending on the given blueprint
        if blueprint is None:
            self._grid = _generate_empty_grid()
        else:
            self._grid = blueprint

        # Adds points if required
        self.add_points(chance)

    def add_points(self, chance: float) -> None:
        """Randomly scatters points across the empty tiles of the level
        at the rate of <chance>.
        """
        # Runs through each tile
        for i in range(len(self._grid)):
            for j in range(len(self._grid[i])):
                # Makes sure it is empty
                if self._grid[i][j] == 0:
                    # Randomly chooses whether to make it a point
                    if random.random() < chance:
                        self._grid[i][j] = 2

    def draw(self, display: pygame.Surface) -> None:
        """Draws this level to the given PyGame display.
        """
        # Sets the background
        display.fill(COLORS[0])

        # Draws each tile in the grid
        for i in range(len(self._grid)):
            for j in range(len(self._grid[i])):
                # Calculates the left and top
                left = i * TILE_SIZE
                top = j * TILE_SIZE
                # Gets the tile index
                index = self._grid[i][j]

                # Draws the tile if it is not empty
                if index == 1 or index == 2:
                    # Creates the rectangle and draws it
                    tile_rect = pygame.Rect(left, top, TILE_SIZE, TILE_SIZE)
                    pygame.gfxdraw.box(display, tile_rect, COLORS[index])

    def get_tile_at(self, position: Tuple[int, int]) -> int:
        """Gets the tile at the given position.

        Returns the integer representation.
        """
        return self._grid[position[0]][position[1]]

    def set_tile_at(self, position: Tuple[int, int], tile: int) -> None:
        """Sets the tile at the given position to the integer representation.
        """
        self._grid[position[0]][position[1]] = tile

    def dump_grid(self, save: BinaryIO) -> None:
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
    level: 'Level'
    points: int

    # === Private Attributes ===
    # _x_coord:
    #   x-coordinate of the creature
    # _y_coord:
    #   y-coordinate of the creature
    # _visited:
    #   list of tuples of visited points
    _x_coord: int
    _y_coord: int
    _visited: List[Tuple[int, int]]

    def __init__(self, level: 'Level') -> None:
        """Initializes the creature in the given level.
        """
        # Initializes the level and the number of points
        self.level = level
        self.points = 0

        # Sets the position to the middle and sets that to be a visited place
        self._x_coord = NUM_COLUMNS // 2
        self._y_coord = NUM_ROWS // 2
        self._visited = [(self._x_coord, self._y_coord)]

    def _try_move(self, displacement: Tuple[int, int]) -> None:
        """Try to move a certain displacement, update accordingly.
        """
        # Gets the move to position and loops the board if the end is hit
        move_x = (self._x_coord + displacement[0]) % NUM_COLUMNS
        move_y = (self._y_coord + displacement[1]) % NUM_ROWS

        # Gets the tile at the position to move to
        status = self.level.get_tile_at((move_x, move_y))

        # Moves there if it is not a wall
        if status != 1:
            self._x_coord = move_x
            self._y_coord = move_y

        # Collects the point if it is a point
        if status == 2:
            pos = (self._x_coord, self._y_coord)
            # Updates if this point has not been collected by this creature
            if pos not in self._visited:
                self._visited.append(pos)
                self.points += 1

    def move(self, direction: str) -> None:
        """Moves the creature in the given direction.
        """
        if direction == 'U':
            self._try_move((0, -1))
        elif direction == 'R':
            self._try_move((1, 0))
        elif direction == 'D':
            self._try_move((0, 1))
        elif direction == 'L':
            self._try_move((-1, 0))
        elif direction == 'UR':
            self._try_move((-1, 1))
        elif direction == 'UL':
            self._try_move((-1, -1))
        elif direction == 'DR':
            self._try_move((1, 1))
        elif direction == 'DL':
            self._try_move((1, -1))

    def draw(self, display: pygame.Surface) -> None:
        """Draws this creature to the given PyGame display.
        """
        # Calculates the left and top
        left = self._x_coord * TILE_SIZE
        top = self._y_coord * TILE_SIZE

        # Creates the rectangle and chooses the color
        tile_rect = pygame.Rect(left, top, TILE_SIZE, TILE_SIZE)
        color = RED

        # Draws the rectangle
        pygame.draw.rect(display, color, tile_rect)


def _generate_empty_grid() -> List[List[int]]:
    """Generates an empty grid.
    """
    # Generates the grid and returns it
    grid = []
    for _ in range(NUM_COLUMNS):
        column = [0] * NUM_ROWS
        grid.append(column)
    return grid


def _generate_boxed_grid() -> List[List[int]]:
    """Generates a grid with walls only at the sides.
    """
    # Generates the grid and returns it
    grid = []
    for i in range(NUM_COLUMNS):
        if i == 0 or i == NUM_COLUMNS - 1:
            column = [1] * NUM_ROWS
        else:
            column = [1] + [0] * (NUM_ROWS - 2) + [1]
        grid.append(column)
    return grid


def ask_level() -> List:
    """Asks for the level to load.

    Returns an empty array if the level is randomly generated,
    returns an 2-d array if with the level if it is chosen.
    """
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


def ask_points() -> float:
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


def draw_graph(fitness_levels: List[Tuple[float, float, float]]) -> None:
    """Draws the graph of fitness versus generation.
    """
    # Separates the statistics
    maximum_fitnesses = [stat[0] for stat in fitness_levels]
    minimum_fitnesses = [stat[1] for stat in fitness_levels]
    average_fitnesses = [stat[2] for stat in fitness_levels]

    # Plots average fitness versus generation
    plt.plot(average_fitnesses, 'b',
             maximum_fitnesses, 'g-',
             minimum_fitnesses, 'r-')

    # Sets display labels
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Fitness Statistics")
    plt.grid()

    # Shows the plot
    plt.show()
