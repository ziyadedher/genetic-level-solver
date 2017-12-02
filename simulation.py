"""General simulation control.
"""

import time

import pygame


# Screen constants
SCREEN_SIZE = (1000, 500)
SCREEN_TITLE = "Genetic Level Solver"

# Level constants
TILE_SIZE = 10

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

    def __init__(self):
        """Initializes this level.
        """
        # Generates the grid
        self._grid = self._generate_boxed_grid()

    def _generate_boxed_grid(self):
        """Generates a grid with walls only at the sides.
        """
        # Calculates how many rows and columns of tiles there will be
        columns = SCREEN_SIZE[0] // TILE_SIZE
        rows = SCREEN_SIZE[1] // TILE_SIZE

        # Generates the grid and returns it
        grid = []
        for x in range(columns):
            if x == 0 or x == columns - 1:
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


if __name__ == '__main__':
    sim = Simulation()
    while True:
        pygame.display.update()
