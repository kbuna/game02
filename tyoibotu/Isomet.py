import pygame
import os

# タイルのサイズとマップの大きさを設定します
TILESIZE = 64
MAPWIDTH = 10
MAPHEIGHT = 10

# タイルの色を設定します
colours = {
    'grass': (0, 255, 0),
    'dirt': (139, 69, 19)
}

# タイルマップを作成します
tilemap = [
    ['grass' for _ in range(MAPWIDTH)] for _ in range(MAPHEIGHT)
]

# NPCの位置を設定します
npc_position = [5, 5]

# Pygameを初期化します
pygame.init()
DISPLAYMAP = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))

# 等角投影タイルを作成します
isometric_tiles = {}
for key, color in colours.items():
    tile_surf = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
    tile_surf.fill(color)
    tile_surf = pygame.transform.rotate(tile_surf, 45)
    isometric_size = tile_surf.get_width()
    tile_surf = pygame.transform.scale(tile_surf, (isometric_size, isometric_size//2))
    isometric_tiles[key] = tile_surf

# NPCのSurfaceを作成します
npc_surf = pygame.image.load('npc.png')

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                npc_position[1] -= 1
            elif event.key == pygame.K_DOWN:
                npc_position[1] += 1
            elif event.key == pygame.K_LEFT:
                npc_position[0] -= 1
            elif event.key == pygame.K_RIGHT:
                npc_position[0] += 1

    # タイルを描画します
    for column in range(MAPWIDTH):
        for row in range(MAPHEIGHT):
            tile_surf = isometric_tiles[tilemap[row][column]]
            x = (column + (MAPHEIGHT - row)) * isometric_size // 2
            y = 20 + (column + row) * isometric_size // 4
            DISPLAYMAP.blit(tile_surf, (x, y))

    # NPCを描画します
    x = (npc_position[0] + (MAPHEIGHT - npc_position[1])) * isometric_size // 2
    y = 20 + (npc_position[0] + npc_position[1]) * isometric_size // 4
    DISPLAYMAP.blit(npc_surf, (x, y))

    pygame.display.update()

pygame.quit()

