"""Level creator utility for the simulator.
"""

import os
import pygame

import simulation


# Display constants
SCREEN_TITLE = "Level Creator"


def main():
    """Runs the level creator.
    """
    # Displays instructions
    print("")
    print("Left click on the screen to draw and right click to erase.")
    print("Left arrow key will make you draw points (green), " +
          "and right will make you draw walls (white).")
    print("Close the window to save your level.")
    input("Press enter to continue. \n")

    # Creates the stock empty level with no points and initializes PyGame
    level = simulation.Level(blueprint=None, chance=0)
    pygame.init()
    display = pygame.display.set_mode(simulation.SCREEN_SIZE)
    pygame.display.set_caption(SCREEN_TITLE)

    # Keeps track if the editor is closed and which tile is being added
    editing = True
    adding = 1

    # Runs until editing is finished
    while editing:
        # Event handler
        for event in pygame.event.get():
            # Ends the editor on quit
            if event.type == pygame.QUIT:
                editing = False

            # Sets the tile to add
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    adding = 2
                if event.key == pygame.K_RIGHT:
                    adding = 1

        # Gets mouse position and its respective position on the grid
        mouse_pos = pygame.mouse.get_pos()
        grid_pos = (mouse_pos[0] // simulation.TILE_SIZE,
                    mouse_pos[1] // simulation.TILE_SIZE)

        # Adds if left mouse was pressed and removes if right mouse
        if pygame.mouse.get_pressed()[0]:
            level.set_tile_at(grid_pos, adding)
        elif pygame.mouse.get_pressed()[2]:
            level.set_tile_at(grid_pos, 0)

        # Draws the level and updates the display
        level.draw(display)
        pygame.display.update()

    # Quits PyGame window
    pygame.quit()

    # Creates the levels directory if it did not exist
    if not os.path.exists(simulation.LEVEL_PATH):
        os.mkdir(simulation.LEVEL_PATH)

    # Asks for a name
    prompt = "What would you like to call this level?\n> "
    name = input(prompt)
    # Makes sure the name is valid
    while name == "" or any(c in name for c in './'):
        print("That is not a valid name.")
        name = input(prompt)
    # Saves
    with open(simulation.LEVEL_PATH + name, "wb+") as save:
        level.dump_grid(save)
