import pygame
import os

TILESIZE = 32
MAPWIDTH = 100
MAPHEIGHT = 100

# 初期のズームとカメラ位置
zoom = 1.0
camera_x, camera_y = 0, 0
dragging = False

DISPLAYMAP = pygame.display.set_mode((1280, 780))

# タイルの色を設定します
colours = {
    'road': (128, 128, 128),
    'dirt': (139, 69, 19),
    'selected': (255, 255, 255)  # 選択中のタイルの色
}

# テキストファイルからマップを読み込む
def load_map(filename):
    with open(filename, 'r') as file:
        return [line.strip().split() for line in file]

# マップデータの読み込み
filename = 'map.txt'
tilemap = load_map(filename)

# 選択中のタイル
selected_tile = 'road'

# 等角投影タイルを作成します
isometric_size = int(TILESIZE * 1.5)
isometric_tiles = {}
for key, color in colours.items():
    tile_surf = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
    tile_surf.fill(color)
    tile_surf = pygame.transform.rotate(tile_surf, 45)
    tile_surf = pygame.transform.scale(tile_surf, (isometric_size, isometric_size // 2))
    isometric_tiles[key] = tile_surf

# ゲームループのフレームレートを制御するためのClockオブジェクトを作成します
clock = pygame.time.Clock()

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左クリック
                dragging = True
                last_mouse_pos = pygame.mouse.get_pos()
            elif event.button == 3:  # 右クリック
                if not palette_window.get_rect().collidepoint(event.pos):
                    # エディットウィンドウがクリックされた場合、選択されたタイルを変更
                    column = int((event.pos[0] - camera_x) // (isometric_size * zoom))
                    row = int(((event.pos[1] - camera_y) - 20) // (isometric_size * zoom))
                    if 0 <= column < MAPWIDTH and 0 <= row < MAPHEIGHT:
                        tilemap[row][column] = selected_tile
            elif event.button == 4:  # ホイールアップ
                zoom *= 1.1
            elif event.button == 5:  # ホイールダウン
                zoom /= 1.1
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False

    if dragging:
        current_mouse_pos = pygame.mouse.get_pos()
        dx, dy = current_mouse_pos[0] - last_mouse_pos[0], current_mouse_pos[1] - last_mouse_pos[1]
        camera_x += dx
        camera_y += dy
        last_mouse_pos = current_mouse_pos

    keys = pygame.key.get_pressed()

    # キー操作によるズームイン・ズームアウト
    if keys[pygame.K_PLUS] or keys[pygame.K_KP_PLUS]:
        zoom += 0.02
    if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
        zoom -= 0.02
    zoom = max(0.1, min(zoom, 2.0))  # ズーム範囲を制限

    # 画面をクリアして再描画
    DISPLAYMAP.fill((0, 0, 0))  # 黒で塗りつぶす

    # タイルを描画します
    for column in range(MAPWIDTH):
        for row in range(MAPHEIGHT):
            tile_type = tilemap[row][column]
            tile_surf = isometric_tiles[tile_type]
            tile_size = int(TILESIZE * zoom)
            x = (column + (MAPHEIGHT - row)) * tile_size // 2 + camera_x
            y = 20 + (column + row) * tile_size // 4 + camera_y
            tile_surf = pygame.transform.scale(tile_surf, (tile_size, tile_size // 2))
            DISPLAYMAP.blit(tile_surf, (x, y))

    # 選択中のタイルをパレットウィンドウに表示
    palette_window = pygame.Surface((100, 50))
    palette_window.fill((0, 0, 0))
    selected_tile_surf = isometric_tiles[selected_tile]
    selected_tile_surf = pygame.transform.scale(selected_tile_surf, (50, 25))
    palette_window.blit(selected_tile_surf, (25, 12))
    DISPLAYMAP.blit(palette_window, (0, 0))

    pygame.display.update()

    # フレームレートを制御します
    clock.tick(60)

pygame.quit()
