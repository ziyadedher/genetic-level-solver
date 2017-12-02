import pygame
import simulation

def updated_level(grid):
    return simulation.Level(grid)


pwidth, pheight = simulation.SCREEN_SIZE
bwidth, bheight = pwidth // simulation.TILE_SIZE, pheight // simulation.TILE_SIZE
print(bwidth, bheight)
grid = [[0] * bheight for x in range(bwidth)]
level = updated_level(grid)
pygame.init()

screen = pygame.display.set_mode(simulation.SCREEN_SIZE)
going = True
old_position = ()

while going:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            going = False
    position = pygame.mouse.get_pos()
    grid_pos = position[0] // simulation.TILE_SIZE, position[1] // \
        simulation.TILE_SIZE
    if pygame.mouse.getpressed() and grid_pos != old_position:
        grid[grid_pos[0]][grid_pos[1]] += 1
        grid[grid_pos[0]][grid_pos[1]] %= 3
        level = updated_level(grid)
    old_position = grid_pos
    level.draw(screen)
        pygame.display.update()
