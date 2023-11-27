
import random
import pygame
import datetime
import os
from title_scene import Button,load_sound
import sys

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
UI_AREA_HEIGHT = 100
# 初期の時間を設定
current_time = datetime.datetime(2023, 11, 11, 2, 32)

# ゲーム内の1分を1秒にするために60fpsの60カウント
frames_per_second = 60
game_count =0

double_speed_button = None
half_speed_button = None

dirty_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

current_speed_state="1"




def get_valid_moves(npc):
    valid_moves = []
    for direction in ['up', 'down', 'left', 'right']:
        new_position = npc['position'].copy()
        if direction == 'up' and new_position[1] > 0:
            new_position[1] -= 1
        elif direction == 'down' and new_position[1] < MAPHEIGHT - 1:
            new_position[1] += 1
        elif direction == 'left' and new_position[0] > 0:
            new_position[0] -= 1
        elif direction == 'right' and new_position[0] < MAPWIDTH - 1:
            new_position[0] += 1
        valid_moves.append(new_position)
    return valid_moves

def draw_valid_moves(screen, npc, isometric_size):
    valid_moves = get_valid_moves(npc)
    for position in valid_moves:
        x = (position[0] + (MAPHEIGHT - position[1])) * isometric_size // 2 + 130
        y = 20 + (position[0] + position[1]) * isometric_size // 4 + 130
        pygame.draw.circle(screen, (0, 255, 0), (x, y), TILESIZE // 2, 3)







def draw_ui(screen, ui_area_height):
    # 画面上部にUIを描画する処理
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, SCREEN_WIDTH, ui_area_height))  # 例: 白い矩形をUIエリアとして描画
    # ここにUIコンポーネントの描画処理を追加


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
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, ui_area_height // 2))
    screen.blit(text_surface, text_rect)







#モデル タイル設定
# 1マスのサイズ
TILESIZE = 64
# 右下に向かって何マス描くか
MAPWIDTH = 10
# 右上に向かって何マス描くか
MAPHEIGHT = 10

# ランダムに属性を持つ、マス数分の多次元リスト
tilemap = [['grass' if random.randint(0, 1) else 'dirt' for _ in range(MAPWIDTH)] for _ in range(MAPHEIGHT)]

# 色の辞書
colours = {
    'grass': (0, 255, 0),
    'dirt': (139, 69, 19)
}



#モデル NPC設定
# NPCの位置と属性を設定します
npcs = [
    {
        'position': [random.randint(0, MAPWIDTH - 1), random.randint(0, MAPHEIGHT - 1)], 
        'type': random.choice(['npc_type_1', 'npc_type_2']),
        'direction': 'down',
        'animation_counter': 0  
        }for _ in range(5)
        ]  #5体生成



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
        'npc_type_2': {
        'up': [
            pygame.image.load('red_up_0.png'),
            pygame.image.load('red_up_1.png'),
            pygame.image.load('red_up_2.png')
        ],
        'down': [
            pygame.image.load('red_down_0.png'),
            pygame.image.load('red_down_1.png'),
            pygame.image.load('red_down_2.png')
        ],
        'left': [
            pygame.image.load('red_left_0.png'),
            pygame.image.load('red_left_1.png'),
            pygame.image.load('red_left_2.png')
        ],
        'right': [
            pygame.image.load('red_right_0.png'),
            pygame.image.load('red_right_1.png'),
            pygame.image.load('red_right_2.png')
        ]
    }
}



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





# npcsリスト内の各npcに対してランダムな方向に移動させ、その後の描画に備えて、位置情報を更新している。
# def update_npcs(npcs,isometric_size,camera_x,camera_y,animation_frames):
def update_npcs(npcs,isometric_size,animation_frames):

    #npc
    for npc in npcs:
        #そのnpcが動く方向を決める
        direction = random.choice(['up', 'down', 'left', 'right'])
        #方向に合わせて座標を動かす
        if direction == 'up' and npc['position'][1] > 0:
            npc['position'][1] -= 1
        elif direction == 'down' and npc['position'][1] < MAPHEIGHT - 1:
            npc['position'][1] += 1
        elif direction == 'left' and npc['position'][0] > 0:
            npc['position'][0] -= 1
        elif direction == 'right' and npc['position'][0] < MAPWIDTH - 1:
            npc['position'][0] += 1
        #npcはどの方向を向いているのか
        npc['direction'] = direction
        #npcのアニメーションフレーム番号
        npc['animation_counter'] = 0  # アニメーションのカウンタをリセット

        # 等角投影を考慮した座標に変換
        x = (npc['position'][0] + (MAPHEIGHT - npc['position'][1])) * isometric_size // 2+130
        y = 20 + (npc['position'][0] + npc['position'][1]) * isometric_size // 4+130
        
        # x = (npc['position'][0] + (MAPHEIGHT - npc['position'][1])) * isometric_size // 2 - camera_x
        # y = 20 + (npc['position'][0] + npc['position'][1]) * isometric_size // 4 - camera_y
        #npcの方向に応じた画像取得
        animation_list = npc_images[npc['type']][npc['direction']]
        #アニメーションの進行具合を取得する
        animation_counter = npc['animation_counter'] // (animation_frames // len(animation_list))
        #現在のアニメ画像の取得
        npc_image = animation_list[animation_counter % len(animation_list)]
        #変更があったrectの更新
        dirty_rect.union_ip(pygame.Rect(x, y, npc_image.get_width(), npc_image.get_height()))
    return dirty_rect


def draw_npcs(screen, npcs, npc_images, isometric_size, animation_frames):
    for npc in npcs:
    #     x = (npc['position'][0] + (MAPHEIGHT - npc['position'][1])) * isometric_size // 2 - camera_x
    #     y = 20 + (npc['position'][0] + npc['position'][1]) * isometric_size // 4 - camera_y
        x = (npc['position'][0] + (MAPHEIGHT - npc['position'][1])) * isometric_size // 2  +130
        y = 20 + (npc['position'][0] + npc['position'][1]) * isometric_size // 4  +130
        # 歩行アニメーションのための画像を選択
        animation_list = npc_images[npc['type']][npc['direction']]
        animation_counter = npc['animation_counter'] // (animation_frames // len(animation_list))
        npc_image = animation_list[animation_counter % len(animation_list)]

        screen.blit(npc_image, (x, y))

        # 移動判定ごとにアニメーションカウンタを増加
        npc['animation_counter'] = (npc['animation_counter'] + 1) % animation_frames



def draw_tiles(screen,isometric_size):
    for column in range(MAPWIDTH):
        for row in range(MAPHEIGHT):
            tile_surf = isometric_tiles[tilemap[row][column]]
            x = (column + (MAPHEIGHT - row)) * isometric_size // 2 +130
            y = 20 + (column + row) * isometric_size // 4 +130
            
            # x = (column + (MAPHEIGHT - row)) * isometric_size // 2 - camera_x
            # y = 20 + (column + row) * isometric_size // 4 - camera_y
            #screen.blit(tile_surf, (x, y))
            screen.blit(tile_surf, (x - TILESIZE // 2, y - TILESIZE // 2))



# 等角投影タイルを作成....
isometric_size = int(TILESIZE * 1.5)
isometric_tiles = {}

for key, color in colours.items():
    tile_surf = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
    tile_surf.fill(color)
    tile_surf = pygame.transform.rotate(tile_surf, 45)
    tile_surf = pygame.transform.scale(tile_surf, (isometric_size, isometric_size // 2))
    isometric_tiles[key] = tile_surf


def on_click(text):
    print(f"{text} button clicked!")
    # ここに倍速時の処理を追加
    global frames_per_second
    if text == "1":
        frames_per_second *= 2
    elif text == "2":
        frames_per_second /= 2


# def update_scene(screen, frame_count, move_frames,animation_frames,animation_counter,camera_x, camera_y,camera_speed):
def update_scene(pygame,screen, frame_count, move_frames,animation_frames,animation_counter):
    #引数は、画面自体、アニメ描画実行されるまでのフレームカウントムーブカウント、アニメ連番、カメラ座標、制御クロック
    

    global double_speed_button
    global half_speed_button

    if double_speed_button is None and half_speed_button is None:
        font = pygame.font.Font(None, 36)
        # タイマー倍速ボタンの作成
        double_speed_button = Button(screen, "2x Speed", font, 100, 20, 50, 50)
        half_speed_button = Button(screen, "0.5x Speed", font, 100, 50, 50, 50)

    global dirty_rect
    global game_count
    # テスト時間計測開始
    start_time = pygame.time.get_ticks()
    print(f"Before: frame_count = {frame_count}")


    #シーン遷移があるため、まず塗りつぶす
    screen.fill((0, 0, 0))  

    # タイルを描画する
    draw_tiles(screen,isometric_size)

    #ゲーム時間を進める
    if game_count % frames_per_second ==0:
        update_timer()

    #npcの移動タイミングならば移動する
    if frame_count % move_frames == 0:
        dirty_rect = update_npcs(npcs,isometric_size,animation_frames)
        # dirty_rect = update_npcs(npcs,isometric_size,camera_x,camera_y,animation_frames)

        #移動可能な範囲をデバックチェック
        for npc in npcs:
            draw_valid_moves(screen, npc, isometric_size)


    #npcを描画する
    draw_npcs(screen, npcs, npc_images, isometric_size, animation_frames)

    # 画面上部にUIを描画
    draw_ui(screen, UI_AREA_HEIGHT)
    draw_timer(screen, UI_AREA_HEIGHT)
    double_speed_button.draw("Black", hover_sound=hover_sound)
    half_speed_button.draw("Black", hover_sound=hover_sound)
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            # ボタンのクリック状態を更新
            double_speed_button.draw("Black", hover_sound=hover_sound)
            half_speed_button.draw("Black", hover_sound=hover_sound)
            if double_speed_button.rect.collidepoint(event.pos):
                current_speed_state="1"
                on_click(current_speed_state)
            if half_speed_button.rect.collidepoint(event.pos):
                current_speed_state="2"
                on_click(current_speed_state)



    #変更があった部分のrectのみdisplayに統合
    pygame.display.update(dirty_rect)

    #1/60秒をカウントする
    game_count +=1


    # カメラの位置をマウスの位置にゆっくり追従
    # mouse_x, mouse_y = pygame.mouse.get_pos()
    # camera_x = lerp(camera_x, mouse_x, camera_speed)
    # camera_y = lerp(camera_y, mouse_y, camera_speed)

    # テスト時間計測終了
    end_time = pygame.time.get_ticks()
    # 経過時間を出力
    elapsed_time = end_time - start_time
    print(f"scene_start の実行時間: {elapsed_time} ミリ秒")




