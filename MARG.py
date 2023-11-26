import pygame
import os
import random

# 線形補間 aからbまでの値をtの割合で補間する
def lerp(a, b, t):
    return a + t * (b - a)

# タイルの定義
TILESIZE = 64
MAPWIDTH = 5
MAPHEIGHT = 10
colours = {'grass': (0, 255, 0), 'dirt': (139, 69, 19)}
tilemap = [['grass' if random.randint(0, 1) else 'dirt' for _ in range(MAPWIDTH)] for _ in range(MAPHEIGHT)]

# NPCの初期位置と属性を設定
npcs = [{'position': [random.randint(0, MAPWIDTH - 1), random.randint(0, MAPHEIGHT - 1)], 'type': 'npc_type_1', 'direction': 'down'} for _ in range(3)]

# カメラの初期位置と速度
camera_x, camera_y = 0, 0
camera_speed = 0.02

# Pygameを初期化
pygame.init()
screen = pygame.display.set_mode((800, 600))  # ウィンドウサイズを800x600に変更
pygame.display.set_caption("Isometric Game")

# 等角投影タイルの生成
isometric_size = int(TILESIZE * 1.5)
isometric_tiles = {}
for key, color in colours.items():
    tile_surf = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
    tile_surf.fill(color)
    tile_surf = pygame.transform.rotate(tile_surf, 45)
    tile_surf = pygame.transform.scale(tile_surf, (isometric_size, isometric_size // 2))
    isometric_tiles[key] = tile_surf

# NPC画像のロード
npc_images = {
    'npc_type_1': {
        'up': [pygame.image.load('npc_up_0.png'), pygame.image.load('npc_up_1.png'), pygame.image.load('npc_up_2.png')],
        'down': [pygame.image.load('npc_down_0.png'), pygame.image.load('npc_down_1.png'), pygame.image.load('npc_down_2.png')],
        'left': [pygame.image.load('npc_left_0.png'), pygame.image.load('npc_left_1.png'), pygame.image.load('npc_left_2.png')],
        'right': [pygame.image.load('npc_right_0.png'), pygame.image.load('npc_right_1.png'), pygame.image.load('npc_right_2.png')]
    },
}

# ゲームループのフレームレートを制御するClockオブジェクト
clock = pygame.time.Clock()

# NPCが移動するフレーム数とアニメーションに関する設定
move_frames = 30
frame_count = 0
animation_frames = 10
animation_counter = 0

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if frame_count % move_frames == 0:
        for npc in npcs:
            direction = random.choice(['up', 'down', 'left', 'right'])
            if direction == 'up' and npc['position'][1] > 0:
                npc['position'][1] -= 1
            elif direction == 'down' and npc['position'][1] < MAPHEIGHT - 1:
                npc['position'][1] += 1
            elif direction == 'left' and npc['position'][0] > 0:
                npc['position'][0] -= 1
            elif direction == 'right' and npc['position'][0] < MAPWIDTH - 1:
                npc['position'][0] += 1
            npc['direction'] = direction
            npc['animation_counter'] = 0

    screen.fill((0, 0, 0))  # 黒で画面をクリア

    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            tile_surf = isometric_tiles[tilemap[row][column]]
            x = (column + (MAPHEIGHT - row)) * isometric_size // 2 - camera_x
            y = 20 + (column + row) * isometric_size // 4 - camera_y
            screen.blit(tile_surf, (x, y))

    for npc in npcs:
        x = (npc['position'][0] + (MAPHEIGHT - npc['position'][1])) * isometric_size // 2 - camera_x
        y = 20 + (npc['position'][0] + npc['position'][1]) * isometric_size // 4 - camera_y

        animation_list = npc_images[npc['type']][npc['direction']]
        animation_counter = npc['animation_counter'] // (animation_frames // len(animation_list))
        npc_image = animation_list[animation_counter % len(animation_list)]

        screen.blit(npc_image, (x, y))
        npc['animation_counter'] = (npc['animation_counter'] + 1) % animation_frames

    pygame.display.update()
    clock.tick(60)
    frame_count += 1
    mouse_x, mouse_y = pygame.mouse.get_pos()
    camera_x = lerp(camera_x, mouse_x, camera_speed)
    camera_y = lerp(camera_y, mouse_y, camera_speed)

pygame.quit()