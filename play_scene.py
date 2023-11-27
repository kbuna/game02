
import random
import pygame
import datetime
import os
from title_scene import Button,load_sound
import sys
import math
import numpy as np

#------------------------------------------初期化

WIDTH = 1280
HEIGHT = 720
UI_AREA_HEIGHT = 100


# 背景
BACKGROUND_COLOR = (25, 25, 112)
AURORA_COLOR1 = (240, 240, 240, 140)  # オーロラの色1
AURORA_COLOR2 = (173, 216, 230, 50)   # オーロラの色2
def draw_aurora(background, frame_count):
    for x in range(WIDTH):
        x_offset = frame_count / 2.7 + random.uniform(0, 2)
        amplitude = HEIGHT / 2 * math.sin(frame_count / 100)
        y = int(HEIGHT / 1.3 - amplitude * math.sin((x + x_offset) / WIDTH /4 * math.pi-1.3))
        # 周期の変数を大きな値にしてゆっくり目にする
        color_value = random.randint(225, 255)
        color = (color_value, color_value, color_value)
        pygame.draw.line(background, color, (x, HEIGHT), (x, y), 1)

        #ノイズ
        #amplitude = HEIGHT / 4 * math.sin(frame_count / random.uniform(0,10000))

        #極彩色
        # # color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))


def apply_dynamic_dark_filter(surface, frame_count):
    # サーフェスデータをNumPy配列に変換
    pixels = pygame.surfarray.pixels3d(surface)

   # サイン波の周期を調整
    sine_period = 500
    # 時間の経過によって変化する係数を計算
    time_factor = (math.sin(frame_count / sine_period) + 1) / 2  

    # 色が乗る効果を加える
    color_change_rate = 0.145  # 色がどれだけ乗るかを制御
    pixels[:, :, 0] = np.clip(pixels[:, :, 0] + 255 * color_change_rate * time_factor, 0, 255).astype(np.uint8)
    pixels[:, :, 1] = np.clip(pixels[:, :, 1] + 255 * color_change_rate * time_factor, 0, 255).astype(np.uint8)
    pixels[:, :, 2] = np.clip(pixels[:, :, 2] + 255 * color_change_rate * time_factor, 0, 255).astype(np.uint8)

    # 明るさを調整する係数を設定
    brightness_change_rate = 0.315  # 明るさがどれだけ変わるかを制御
    # 明るさを変更
    brightness = 1 - brightness_change_rate * time_factor
    pixels[:, :, 0] = np.clip(pixels[:, :, 0] * brightness, 0, 255).astype(np.uint8)
    pixels[:, :, 1] = np.clip(pixels[:, :, 1] * brightness, 0, 255).astype(np.uint8)
    pixels[:, :, 2] = np.clip(pixels[:, :, 2] * brightness, 0, 255).astype(np.uint8)

#タイルマップ関連-----------------------------------------------------------------------------------------------------
#タイル素材--------------------
# 1マスの定義
TILESIZE = 64

# タイル属性
tile_type = {
    'grass': (0, 255, 0),
    'dirt': (139, 69, 19),
    'ice1': (173, 216, 230),  # 氷の色1
    'ice2': (135, 206, 250),  # 氷の色2
    'water': (30, 144, 255)  # 水の色
}

# 等角投影タイルの定義
isometric_Width = int(TILESIZE * 1.5)
isometric_Height = isometric_Width // 2

# 使用するタイル辞書
use_tiles = {}

# タイルを具体化する
for key, type_color in tile_type.items():
    # 背景が透明化された、タイルSurfaceを作る
    tile = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
    # 色を塗る
    tile.fill(type_color)
    # 反時計回りで45度回転させる
    tile = pygame.transform.rotate(tile, 45)
    # (幅,高さ)で指定したサイズの新規Surfaceを作る
    tile = pygame.transform.scale(tile, (isometric_Width, isometric_Height))
    # タイル属性の数だけuseタイルを格納
    use_tiles[key] = tile

# マップを作る-----------------------------------

# 左上から右に向かって何マスか
MAPWIDTH = 10
# 左上から下に向かって何マスか
MAPHEIGHT = 10

# タイルでマップを制作する
tilemap = [['water' if random.randint(0, 5) == 0 else random.choice(['ice1', 'ice2']) for _ in range(MAPWIDTH)] for _ in range(MAPHEIGHT)]

def draw_tiles(screen, isometric_Width):
    for column in range(MAPWIDTH):
        for row in range(MAPHEIGHT):
            tile = use_tiles[tilemap[row][column]]
            x = (column + (MAPHEIGHT - row)) * isometric_Width // 2 + 130
            y = 20 + (column + row) * isometric_Width // 4 + 130
            screen.blit(tile, (x - TILESIZE // 2, y - TILESIZE // 2))




#----------------------------------------------------------NPC


#NPCが取り得る見た目の画像セット
npc_images = {
    'npc_type_1': {
        'up': [
            pygame.image.load('image/npc_up_0.png'),
            pygame.image.load('image/npc_up_1.png'),
            pygame.image.load('image/npc_up_2.png')
        ],
        'down': [
            pygame.image.load('image/npc_down_0.png'),
            pygame.image.load('image/npc_down_1.png'),
            pygame.image.load('image/npc_down_2.png')
        ],
        'left': [
            pygame.image.load('image/npc_left_0.png'),
            pygame.image.load('image/npc_left_1.png'),
            pygame.image.load('image/npc_left_2.png')
        ],
        'right': [
            pygame.image.load('image/npc_right_0.png'),
            pygame.image.load('image/npc_right_1.png'),
            pygame.image.load('image/npc_right_2.png')
        ]
    },
    # 他のNPCタイプも追加
        'npc_type_2': {
        'up': [
            pygame.image.load('image/red_up_0.png'),
            pygame.image.load('image/red_up_1.png'),
            pygame.image.load('image/red_up_2.png')
        ],
        'down': [
            pygame.image.load('image/red_down_0.png'),
            pygame.image.load('image/red_down_1.png'),
            pygame.image.load('image/red_down_2.png')
        ],
        'left': [
            pygame.image.load('image/red_left_0.png'),
            pygame.image.load('image/red_left_1.png'),
            pygame.image.load('image/red_left_2.png')
        ],
        'right': [
            pygame.image.load('image/red_right_0.png'),
            pygame.image.load('image/red_right_1.png'),
            pygame.image.load('image/red_right_2.png')
        ]
    }
}




#５体のNPCが生成される
npcs = [
    {
        #マス数未満の正数をランダムに
        'position': [random.randint(0, MAPWIDTH - 1), random.randint(0, MAPHEIGHT - 1)], 
        'type': random.choice(['npc_type_1', 'npc_type_2']),
        'direction': 'down',
        'animation_counter': 0  
        }for _ in range(5)
        ]  #5体生成

# すべてのnpcの行動を更新する
def update_npcs(npcs):

    for npc in npcs:    
        # 一定の確率で向きをランダムに変更
        if random.random() < 0.2:  # ここで確率を調整 (例: 0.2は20%の確率)
            npc['direction'] = random.choice(['up', 'down', 'left', 'right'])

        # 移動前の座標を保存
        original_position = npc['position'][:]
        
        # 現在の向きに基づいて移動
        new_position = npc['position'][:]
        if npc['direction'] == 'up':
            new_position[1] -= 1
        elif npc['direction'] == 'down':
            new_position[1] += 1
        elif npc['direction'] == 'left':
            new_position[0] -= 1
        elif npc['direction'] == 'right':
            new_position[0] += 1

        # 移動先の座標が有効な範囲内であれば更新
        if 0 <= new_position[0] < MAPWIDTH and 0 <= new_position[1] < MAPHEIGHT:
            # 移動先に他のNPCがいなければ更新
            if all(npc['position'] != other_npc['position'] for other_npc in npcs if other_npc != npc):
                npc['position'] = new_position
            else:
                # 移動先に他のNPCがいる場合、違う方向を選ぶ
                valid_directions = ['up', 'down', 'left', 'right']
                valid_directions.remove(npc['direction'])  # 現在の向きを除外

                # 新しい方向を選ぶ
                new_direction = random.choice(valid_directions)
                new_position = npc['position'][:]
                if new_direction == 'up':
                    new_position[1] -= 1
                elif new_direction == 'down':
                    new_position[1] += 1
                elif new_direction == 'left':
                    new_position[0] -= 1
                elif new_direction == 'right':
                    new_position[0] += 1

                # 新しい方向でもすべての方向がブロックされている場合、足踏み
                if all(
                    (
                        (new_direction == 'up' and original_position[1] == npc['position'][1] - 1) or
                        (new_direction == 'down' and original_position[1] == npc['position'][1] + 1) or
                        (new_direction == 'left' and original_position[0] == npc['position'][0] - 1) or
                        (new_direction == 'right' and original_position[0] == npc['position'][0] + 1)
                    ) for other_npc in npcs if other_npc != npc
                ):
                    npc['position'] = original_position
                else:
                    npc['position'] = new_position
        else:
            # 移動先が無効な範囲の場合、向きを再抽選して進める方向を探す
            valid_directions = ['up', 'down', 'left', 'right']
            valid_directions.remove(npc['direction'])  # 現在の向きを除外

            # 新しい方向を選ぶ
            new_direction = random.choice(valid_directions)
            new_position = npc['position'][:]
            if new_direction == 'up':
                new_position[1] -= 1
            elif new_direction == 'down':
                new_position[1] += 1
            elif new_direction == 'left':
                new_position[0] -= 1
            elif new_direction == 'right':
                new_position[0] += 1

            # 新しい方向でもすべての方向がブロックされている場合、足踏み
            if all(
                (
                    (new_direction == 'up' and original_position[1] == npc['position'][1] - 1) or
                    (new_direction == 'down' and original_position[1] == npc['position'][1] + 1) or
                    (new_direction == 'left' and original_position[0] == npc['position'][0] - 1) or
                    (new_direction == 'right' and original_position[0] == npc['position'][0] + 1)
                ) for other_npc in npcs if other_npc != npc
            ):
                npc['position'] = original_position
            else:
                npc['position'] = new_position

            # 新しい座標がマップの範囲外になっている場合、座標を修正
            npc['position'][0] = max(0, min(MAPWIDTH - 1, npc['position'][0]))
            npc['position'][1] = max(0, min(MAPHEIGHT - 1, npc['position'][1]))

        # すべてのnpcカウンターを0を代入
        npc['animation_counter'] = 0


# # 壁との衝突をチェックする関数
# def is_wall_collision(position):
#     # 仮の壁の位置や条件に合わせて調整する必要があります
#     return position in [(wall_x, wall_y) for wall_x in range(WALLWIDTH) for wall_y in range(WALLHEIGHT)]



#すべてのnpcを描画する
def draw_npcs(screen, npcs, npc_images, isometric_Width, animation_reduser):

    for npc in npcs:
        #移動先の座標を画定
        x = (npc['position'][0] + (MAPHEIGHT - npc['position'][1])) * isometric_Width // 2  +100
        y = (npc['position'][0] + npc['position'][1]) * isometric_Width // 4  +100


        #()
            

        #imageを取り出す
        animation_list = npc_images[npc['type']][npc['direction']]

        #失速カウンター
        stall_counter = npc['animation_counter'] // (animation_reduser // len(animation_list))
          
            #npcが"持っている"カウントを取り出す。
            #そのカウントを、整数除算した数で整数除算して、低減カウントとして変換する。
            #大雑把に、
            #animation_counter  アニメーションの進行具合
            #animation_reduser アニメーションの進行を遅滞させる
            #len(animation_list) 画像の枚数が大きいほどアニメのコマ切り替えを早める

        #コマ連番画像のループ取得
        npc_image = animation_list[stall_counter % len(animation_list)] 

        # x,yに画像を描画
        screen.blit(npc_image, (x, y))
        # アニメーションカウントを加算する。初期値は１０のタイミングで０に戻る。
        npc['animation_counter'] = (npc['animation_counter'] + 1) % animation_reduser

 


#----------------------------------------デバックモード
# def get_valid_moves(npc):
#     valid_moves = []
#     for direction in ['up', 'down', 'left', 'right']:
#         new_position = npc['position'].copy()
#         if direction == 'up' and new_position[1] > 0:
#             new_position[1] -= 1
#         elif direction == 'down' and new_position[1] < MAPHEIGHT - 1:
#             new_position[1] += 1
#         elif direction == 'left' and new_position[0] > 0:
#             new_position[0] -= 1
#         elif direction == 'right' and new_position[0] < MAPWIDTH - 1:
#             new_position[0] += 1
#         valid_moves.append(new_position)
#     return valid_moves

# def draw_valid_moves(screen, npc, isometric_Width):
#     valid_moves = get_valid_moves(npc)
#     for position in valid_moves:
#         x = (position[0] + (MAPHEIGHT - position[1])) * isometric_Width // 2 + 130
#         y = 20 + (position[0] + position[1]) * isometric_Width // 4 + 130
#         pygame.draw.circle(screen, (0, 255, 0), (x, y), TILESIZE // 2, 3)










# 初期の時間を設定
current_time = datetime.datetime(2023, 11, 11, 2, 32)

# ゲーム内時間を測るカウント
sec_count = 0
minit = 60
#
npc_update_counter=1



#--------------------------------------------------------UI


def draw_ui(screen, ui_area_height):
    # 画面上部にUIを描画する処理
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, WIDTH, ui_area_height))  # 例: 白い矩形をUIエリアとして描画
    # ここにUIコンポーネントの描画処理を追加

#--------------------------------------------------------Timer






# 1秒ごとに実行される関数
def update_timer():
    global current_time
    # 1分進める
    current_time += datetime.timedelta(minutes=1)



# UIエリアにタイマーを表示する関数
def draw_timer(screen, ui_area_height):
    font = pygame.font.Font(None, 36)
    timer_text = current_time.strftime("%Y/%m/%d (%a)\n%I:%M %p")
    text_surface = font.render(timer_text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, ui_area_height // 2))
    screen.blit(text_surface, text_rect)


#---------------------------------------倍速ボタン

#倍速ボタン
double_speed_button = None
half_speed_button = None


current_speed_state="1"

# NPCが移動するタイミング
move_timing = 60

# NPCの次のコマが描かれるまでを遅滞させる
animation_reduser = 10 


def on_click(text):
    print(f"{text} button clicked!")
    global minit
    # ここに倍速時の処理を追加
    if text == "1":
        minit = 30
    elif text == "2":
        minit = 180





#カメラ 距離
def lerp(a, b, t):
    return a + t * (b - a)

    
#SEファイルパスを読み込む
def load_sound(file_path):
    if os.path.exists(file_path):
        return pygame.mixer.Sound(file_path)
    else:
        raise FileNotFoundError(f"File not found: {file_path}")
    
pygame.mixer.init()

hover_sound = load_sound("sound/hover.mp3")









def update_scene(screen, frame_count):
    #引数は、画面自体、アニメ描画実行されるまでのフレームカウントムーブカウント、アニメ連番、カメラ座標、制御クロック



    global double_speed_button,half_speed_button
    global sec_count
    global move_timing #60count
    global animation_reduser #10count
    global npc_update_counter

    aurora_background = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    # 背景をクリア
    aurora_background.fill((0, 0, 0, 0))

    # タイマー倍速ボタンの作成
    if double_speed_button is None and half_speed_button is None:
        font = pygame.font.Font(None, 36)
        double_speed_button = Button(screen, "2x Speed", font, 100, 20, 50, 50)
        half_speed_button = Button(screen, "0.5x Speed", font, 100, 50, 50, 50)

    #シーン遷移があるため、まず塗りつぶす
    screen.fill(BACKGROUND_COLOR)  


    # オーロラを描画
    draw_aurora(aurora_background,frame_count)
        
    # 背景描画前に変化するフィルターをかける
    apply_dynamic_dark_filter(aurora_background, frame_count)

    # 画面に描画
    screen.blit(aurora_background, (0, 0))


    # タイルを描画する
    draw_tiles(screen,isometric_Width)

    #ゲーム時間を進める
    if sec_count % minit ==0:
        update_timer()



    #タイマー倍率が1ならば
    if npc_update_counter == 1:
        #npc移動タイミング
        if frame_count % move_timing == 0:
            #部分的変更のあるrectを検出
            update_npcs(npcs)
            #npc移動エリアデバックチェック
            # for npc in npcs:
            #     draw_valid_moves(screen, npc, isometric_Width)


        #npcアニメタイミングは10
        draw_npcs(screen, npcs, npc_images, isometric_Width, animation_reduser)



    # 画面上部にUIを描画
    draw_ui(screen, UI_AREA_HEIGHT)
    draw_timer(screen, UI_AREA_HEIGHT)
    double_speed_button.draw("Black", hover_sound=hover_sound,rect_color=(255, 0, 0))
    half_speed_button.draw("Black", hover_sound=hover_sound,rect_color=(255, 0, 0))


    # イベント処理
    for event in pygame.event.get():
        print("1")
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("clicked!!!!!")
            # ボタンのクリック状態を更新
            double_speed_button.draw("Black", hover_sound=hover_sound,rect_color=(255, 0, 0))
            half_speed_button.draw("Black", hover_sound=hover_sound,rect_color=(255, 0, 0))
            if double_speed_button.rect.collidepoint(event.pos):
                current_speed_state="1"
                on_click(current_speed_state)
            if half_speed_button.rect.collidepoint(event.pos):
                current_speed_state="2"
                on_click(current_speed_state)



    #バックバッファを画面に反映
    #pygame.display.update()

    #1/60秒をカウントする
    sec_count +=1





