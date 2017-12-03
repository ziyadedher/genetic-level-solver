import pygame
import simulation
import pickle
import sys
import os
if len(sys.argv) != 2:
    print("You fool! You must invoke this command as such:")
    print("python level_creator.py FILE")
    sys.exit()

def updated_level(grid):
    return simulation.Level(grid, points=False)


pwidth, pheight = simulation.SCREEN_SIZE
bwidth, bheight = pwidth // simulation.TILE_SIZE, pheight // simulation.TILE_SIZE
grid = [[0] * bheight for x in range(bwidth)]
level = updated_level(grid)
pygame.init()

screen = pygame.display.set_mode(simulation.SCREEN_SIZE)
going = True
old_position = ()
adding = 1

while going:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            going = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                adding = 2
            if event.key == pygame.K_RIGHT:
                adding = 1

    position = pygame.mouse.get_pos()
    grid_pos = position[0] // simulation.TILE_SIZE, position[1] // \
        simulation.TILE_SIZE
    if pygame.mouse.get_pressed()[0]:
        grid[grid_pos[0]][grid_pos[1]] = adding
    if pygame.mouse.get_pressed()[2]:
        grid[grid_pos[0]][grid_pos[1]] = 0
        level = updated_level(grid)
        old_position = grid_pos
    level.draw(screen)
    pygame.display.update()


directory = "levels"
file_name = sys.argv[1]
file_path = directory + "/" + file_name
if not os.path.exists(directory):
    os.mkdir(directory)
file = open(file_path, "wb+")
pickle.dump(grid, file)
file.close()
