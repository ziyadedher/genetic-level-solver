"""General simulation control.
"""

import time

import pygame


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
        self.level = Level()
        self.level.draw(self.display)


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

    def __init__(self, blueprint=None):
        """Initializes this level with the given blueprint in the form of
        a list of columns where each column is a list of integers.

        - 0 represents a empty block
        - 1 represents a wall
        - 2 represents a point
        """
        # Generates the grid
        if blueprint is None:
            self._grid = self._generate_boxed_grid()
        else:
            self._grid = blueprint

    def _generate_boxed_grid(self):
        """Generates a grid with walls only at the sides.
        """
        # Generates the grid and returns it
        grid = []
        for x in range(NUM_COLUMNS):
            if x == 0 or x == NUM_COLUMNS - 1:
                column = [1] * rows
            else:
                column = [1] + [0] * (rows - 2) + [1]
            grid.append(column)
        return grid

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

        Returns a -1 if the tile is a wall,
        0 if the tile is an empty space,
        1 if the tile is a point.
        """
        return self._grid[position[0]][position[1]] - 1


class Creature:
    """Creature in the simulation.

    === Public Attributes ===
    points:
        number of points this creature has collected
    """
    # === Private Attributes ===
    # _x:
    #   x-coordinate of the creature
    # _y:
    #   y-coordinate of the creature

    def __init__(self, level):
        """Initializes the creature in the given level.
        """
        self.points = 0
        self._x = NUM_COLUMNS // 2
        self._y = NUM_ROWS // 2

    def _try_move(self, displacement):
        """Try to move a certain displacement, update accordingly.
        """
        move_to = (self._x + displacement[0], self._y + displacement[1])
        status = level.get_tile_at(move_to)

        if status != -1:
            self._x = move_to[0]
            self._y = move_to[1]
            self.points += status

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


def run(genomes):
    level = Level()
    creature = Creature(level)
    for instruction in genome:
        creature.move(instruction)
    return creature.points


if __name__ == '__main__':
    sim = Simulation()
    while True:
        pygame.display.update()
