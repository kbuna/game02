import pygame
import sys
import os
import random
import title_scene as ts
import play_scene  as ps

from PIL import Image, ImageEnhance,ImageFilter
#title------------------------------------------------------------------

# 初期設定
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
tmr = 0

# フォントの初期化
pygame.font.init()

# フォントの設定
# font_path = os.path.join(os.path.dirname(__file__), 'font/NotoSansJP-Regular.ttf')
# # font_path = os.path.abspath("font/NotoSansJP-Regular.ttf")
# font = pygame.font.Font(font_path, 36)

# font = pygame.font.Font(os.path.abspath("font/NotoSansJP-Regular.ttf"), 36)

font = pygame.font.Font("font/NotoSansJP-Regular.ttf", 36)

#ビガ
# def apply_white_filter(surface):
#     # サーフェスデータをNumPy配列に変換
#     pixels = pygame.surfarray.pixels3d(surface)

#     # RGB成分を調整して白っぽくする
#     pixels[:, :, 0] = pixels[:, :, 0] + 50  # R成分を増やす
#     pixels[:, :, 1] = pixels[:, :, 1] + 50  # G成分を増やす
#     pixels[:, :, 2] = pixels[:, :, 2] + 50  # B成分を増やす

def apply_white_filter(surface):
    # サーフェスデータをNumPy配列に変換
    pixels = pygame.surfarray.pixels3d(surface)

    # 各成分を均等に増やすのではなく、明るさを抑える
    brightness_factor = 0.8  # 明るさを調整する係数
    pixels[:, :, 0] = pixels[:, :, 0] * brightness_factor  # R成分を調整
    pixels[:, :, 1] = pixels[:, :, 1] * brightness_factor  # G成分を調整
    pixels[:, :, 2] = pixels[:, :, 2] * brightness_factor  # B成分を調整

def desaturate(image_path, output_path, brightness_factor=1.5, saturation_factor=0.5):
    image = Image.open(image_path)

    # 彩度を変更
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(saturation_factor)

    # 明るさを変更
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness_factor)

    # 保存
    image.save(output_path)
#play-------------------------------------------------------------------


def main():

    #pygameを初期化
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("経営型ゲーム")
    pygame.mixer.init()

    global tmr
    global font
    # ゲームループのフレームレートを制御するためのClockオブジェクトを作成します
    clock = pygame.time.Clock()
    # カメラの初期位置
    #camera_x, camera_y = 0, 0
    # カメラの速度係数
    #camera_speed = 0.02
    frame_count=0




    # スタートとコンティニューのボタンの位置を設定
    # 描画する文字、描画し始めるxの座標、yの座標、横幅、縦幅、
    #  0,0→   x+
    # ↓
    #  y+
    start_button = ts.Button(screen,"START",font, SCREEN_WIDTH // 8, SCREEN_HEIGHT // 4-40 , 200, 50)
    continue_button = ts.Button(screen,"CONTINUE",font, SCREEN_WIDTH // 8, SCREEN_HEIGHT // 4 + 70, 200, 50)

    # タイトル画像とホバー効果音を設定
    #img_title = [ts.load_image("image/o1.webp"), ts.load_image("image/logo.png")]
    img_title = [
    pygame.image.load("froze1_desaturated2.png").convert_alpha(),
    pygame.image.load("logo1.png").convert_alpha()
    ]
    img_title[0] = pygame.transform.scale(img_title[0], (SCREEN_WIDTH, SCREEN_HEIGHT))
    #apply_white_filter(img_title[0])  # タイトル画像にフィルタ処理をかける
    #画像生成
    #desaturate("froze1.png", "froze1_desaturated2.png", brightness_factor=1.2, saturation_factor=0.7)


    hover_sound = ts.load_sound("sound/hover.mp3")
    # タイトルBGMを読み込み・再生
    ts.load_music("sound/title.mp3")


        


    # 現在のゲーム状態を、メニュー状態にする
    current_game_state = ts.GameStateSet.MENU



    # ゲームループ
    running = True
    while running:
        
        #print(frame_count)

        # 各ボタンがホバー状態にあるかどうか？
        start_button.set_hovered(start_button.rect.collidepoint(pygame.mouse.get_pos()))
        continue_button.set_hovered(continue_button.rect.collidepoint(pygame.mouse.get_pos()))
        #pygame.mouse.get_pos で現在のマウスの座標を取得する
        #ボタン内に、クリック位置があれば,ホバー状態はTrue
        
        for event in pygame.event.get():


            #Q1 ゲームを閉じるか否か？
            if event.type == pygame.QUIT:
                running = False
            #Q1-2 クリックを検出したか？
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Q1-2-X ゲームは、どんな状態？
                if current_game_state == "menu":
                    if start_button.rect.collidepoint(event.pos):
                        current_game_state = "start"
                    elif continue_button.rect.collidepoint(event.pos):
                        current_game_state = "countinue"

        #A1 メニュー画面ならこうする
        if current_game_state == "menu":
            # タイトルロゴ表示       
            # ビガビガ 
            #apply_white_filter(img_title[0])  # タイトル画像にのみフィルターをかける
            screen.blit(img_title[0], [0, 0])
            screen.blit(img_title[1], [340, 80])
            #hoberedの値を見て、三項演算子で、青か黒か。
            start_color = pygame.Color("blue") if start_button.hovered else pygame.Color("black")
            start_button.draw(start_color,hover_sound=hover_sound,rect_color=(255, 255, 255))

            continue_color = pygame.Color("blue") if continue_button.hovered else pygame.Color("black")
            continue_button.draw(continue_color, hover_sound=hover_sound,rect_color=(255, 255, 255))

        #A2 ゲームスタート後ならこうする
        elif current_game_state == "start": # フレームカウントを更新します
                ps.update_scene(screen, font,frame_count)        
                #print(frame_count)

                #ps.update_scene(screen, frame_count,move_frames,animation_frames,animation_counter, camera_x, camera_y,camera_speed)

        elif current_game_state == "countinue":     
            #exit処理
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(60)#フレームレート
        frame_count += 1





if __name__=="__main__":
  main()



