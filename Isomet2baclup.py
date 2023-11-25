import pygame
import os
import random

def lerp(a, b, t):
    return a + t * (b - a)

# タイルのサイズとマップの大きさを設定します
TILESIZE = 64
MAPWIDTH = 20
MAPHEIGHT = 20

# タイルの色を設定します
colours = {
    'grass': (0, 255, 0),
    'dirt': (139, 69, 19)
}

# タイルマップをランダムに生成します
tilemap = [['grass' if random.randint(0, 1) else 'dirt' for _ in range(MAPWIDTH)] for _ in range(MAPHEIGHT)]

# NPCの位置と属性を設定します
npcs = [{'position': [random.randint(0, MAPWIDTH - 1), random.randint(0, MAPHEIGHT - 1)], 'type': 'npc_type_1', 'direction': 'down'} for _ in range(3)]  # 3つのNPCを作成

# カメラの初期位置
camera_x, camera_y = 0, 0

# カメラの速度係数
camera_speed = 0.02

# Pygameを初期化します
pygame.init()
DISPLAYMAP = pygame.display.set_mode((1280, 780))  # ウィンドウサイズを1280x780に変更

# 等角投影タイルを作成します
isometric_size = int(TILESIZE * 1.5)
isometric_tiles = {}
for key, color in colours.items():
    tile_surf = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
    tile_surf.fill(color)
    tile_surf = pygame.transform.rotate(tile_surf, 45)
    tile_surf = pygame.transform.scale(tile_surf, (isometric_size, isometric_size // 2))
    isometric_tiles[key] = tile_surf

# NPCの画像をロードします
npc_images = {
    'npc_type_1': {
        'up': [
            pygame.image.load('npc_up_0.png'),
            pygame.image.load('npc_up_1.png'),
            pygame.image.load('npc_up_2.png')
        ],
        'down': [
            pygame.image.load('npc_down_0.png'),
            pygame.image.load('npc_down_1.png'),
            pygame.image.load('npc_down_2.png')
        ],
        'left': [
            pygame.image.load('npc_left_0.png'),
            pygame.image.load('npc_left_1.png'),
            pygame.image.load('npc_left_2.png')
        ],
        'right': [
            pygame.image.load('npc_right_0.png'),
            pygame.image.load('npc_right_1.png'),
            pygame.image.load('npc_right_2.png')
        ]
    },
    # 他のNPCタイプも追加
}

# ゲームループのフレームレートを制御するためのClockオブジェクトを作成します
clock = pygame.time.Clock()
# NPCが移動するフレーム数を設定します
move_frames = 30
frame_count = 0

# NPCの歩行アニメーションに関する設定
animation_frames = 10  # 1歩のアニメーションを10フレームかけて描画
animation_counter = 0

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 一定のフレーム数ごとにNPCを移動させます
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
            npc['animation_counter'] = 0  # アニメーションのカウンタをリセット

    # 画面をクリアして再描画
    DISPLAYMAP.fill((0, 0, 0))  # 黒で塗りつぶす

    # タイルを描画します
    for column in range(MAPWIDTH):
        for row in range(MAPHEIGHT):
            tile_surf = isometric_tiles[tilemap[row][column]]
            x = (column + (MAPHEIGHT - row)) * isometric_size // 2 - camera_x
            y = 20 + (column + row) * isometric_size // 4 - camera_y
            DISPLAYMAP.blit(tile_surf, (x, y))

    # NPCを描画します
    for npc in npcs:
        x = (npc['position'][0] + (MAPHEIGHT - npc['position'][1])) * isometric_size // 2 - camera_x
        y = 20 + (npc['position'][0] + npc['position'][1]) * isometric_size // 4 - camera_y

        # 歩行アニメーションのための画像を選択
        animation_list = npc_images[npc['type']][npc['direction']]
        animation_counter = npc['animation_counter'] // (animation_frames // len(animation_list))
        npc_image = animation_list[animation_counter % len(animation_list)]

        DISPLAYMAP.blit(npc_image, (x, y))

        # 移動判定ごとにアニメーションカウンタを増加
        npc['animation_counter'] = (npc['animation_counter'] + 1) % animation_frames

    pygame.display.update()

    # フレームレートを制御します
    clock.tick(60)

    # フレームカウントを更新します
    frame_count += 1

    # カメラの位置をマウスの位置にゆっくり追従
    mouse_x, mouse_y = pygame.mouse.get_pos()
    camera_x = lerp(camera_x, mouse_x, camera_speed)
    camera_y = lerp(camera_y, mouse_y, camera_speed)

pygame.quit()
