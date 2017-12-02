"""General simulation control.
"""

import time

import pygame
import pymunk


# Screen constants
SCREEN_SIZE = (960, 540)
SCREEN_TITLE = "Genetic Level Solver"

# Level constants
TILE_SIZE = 96

# Color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


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
        self.level = Level((10, 5))
        self.level.draw(self.display)


class Level:
    """Level in this simulation.

    === Public Attributes ===
    length:
        horizontal length of this level in tiles
    height:
        vertical height of this level in tiles
    """
    # === Private Attributes ===
    # _grid:
    #   2-D array of level tiles
    #   a tile is a 0 or 1 where 0 is empty and 1 is wall

    def __init__(self, dimensions):
        """Initializes this level with the given dimensions in the form
        (<length>, <height>) in tiles.
        """

        # Initializes dimensions
        self.length = dimensions[0]
        self.height = dimensions[1]

        # Generates the grid
        self._grid = self._generate_ground_grid()

    def _generate_ground_grid(self):
        """Create the tile grid to be an empty level with a ground.

        Returns a 2-D array of tiles (0s or 1s).
        """
        return [([1] + [0 for y in range(self.height - 1)])
                for x in range(self.length)]

    def draw(self, display):
        """Draws this level to the given PyGame display.
        """
        print(self._grid)
        for x in range(len(self._grid)):
            for y in range(len(self._grid[x])):
                left = x * TILE_SIZE
                top = SCREEN_SIZE[1] - ((y + 1) * TILE_SIZE)
                tile_rect = pygame.Rect(left, top, TILE_SIZE, TILE_SIZE)
                color = WHITE if self._grid[x][y] else BLACK

                pygame.draw.rect(display, color, tile_rect)


if __name__ == '__main__':
    sim = Simulation()
    while True:
        pygame.display.update()
