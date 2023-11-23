import pygame
import random
import subprocess
import os

TILESIZE = 32
MAPWIDTH = 100
MAPHEIGHT = 100
DISPLAYMAP = pygame.display.set_mode((MAPWIDTH * TILESIZE, MAPHEIGHT * TILESIZE))

colours = {
    'road': (128, 128, 128),
    'dirt': (139, 69, 19)
}

map_data = [['road' for _ in range(MAPWIDTH)] for _ in range(MAPHEIGHT)]

isometric_size = int(TILESIZE * 1.5)
isometric_tiles = {}
for key, color in colours.items():
    tile_surf = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
    tile_surf.fill(color)
    tile_surf = pygame.transform.rotate(tile_surf, 45)
    tile_surf = pygame.transform.scale(tile_surf, (isometric_size, isometric_size // 2))
    isometric_tiles[key] = tile_surf

pygame.init()
clock = pygame.time.Clock()

def save_map():
    with open('map.txt', 'w') as file:
        for row in map_data:
            file.write(' '.join(row) + '\n')

def load_map():
    if os.path.exists('map.txt'):
        with open('map.txt', 'r') as file:
            return [line.strip().split() for line in file]
    else:
        return [['road' for _ in range(MAPWIDTH)] for _ in range(MAPHEIGHT)]

map_data = load_map()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                map_data[y // TILESIZE][x // TILESIZE] = 'road'
            elif event.button == 3:
                x, y = event.pos
                map_data[y // TILESIZE][x // TILESIZE] = 'dirt'
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                save_map()
                subprocess.run(["python", "tileTST.py"])

    DISPLAYMAP.fill((0, 0, 0))

    for column in range(MAPWIDTH):
        for row in range(MAPHEIGHT):
            tile_type = map_data[row][column]
            tile_surf = isometric_tiles[tile_type]
            x = (column + (MAPHEIGHT - row)) * isometric_size // 2
            y = 20 + (column + row) * isometric_size // 4
            DISPLAYMAP.blit(tile_surf, (x, y))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
