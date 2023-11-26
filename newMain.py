import pygame
import sys
import os
import random
import title_scene as ts
import play_scene  as ps

#title------------------------------------------------------------------

# 初期設定
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
tmr = 0

#play-------------------------------------------------------------------


def main():

    #pygameを初期化
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("経営型ゲーム")
    font = pygame.font.Font(None, 36)
    pygame.mixer.init()

    global tmr

    # ゲームループのフレームレートを制御するためのClockオブジェクトを作成します
    clock = pygame.time.Clock()
    # カメラの初期位置
    #camera_x, camera_y = 0, 0
    # カメラの速度係数
    #camera_speed = 0.02
    frame_count=0
    # NPCが移動するフレーム数を設定します
    move_frames = 60

    # NPCの歩行アニメーションに関する設定
    animation_frames = 10  # 1歩のアニメーションを10フレームかけて描画
    animation_counter = 0




    # スタートとコンティニューのボタンの位置を設定
    # 描画する文字、描画し始めるxの座標、yの座標、横幅、縦幅、
    #  0,0→   x+
    # ↓
    #  y+
    start_button = ts.Button(screen,"START",font, SCREEN_WIDTH // 6, SCREEN_HEIGHT // 4 + 30, 200, 50)
    continue_button = ts.Button(screen,"CONTINUE",font, SCREEN_WIDTH // 6, SCREEN_HEIGHT // 4 + 60, 200, 50)

    # タイトル画像とホバー効果音を設定
    img_title = [ts.load_image("image/o1.webp"), ts.load_image("image/logo.png")]
    hover_sound = ts.load_sound("sound/hover.mp3")
    # タイトルBGMを読み込み・再生
    ts.load_music("sound/title.mp3")


        


    # 現在のゲーム状態を、メニュー状態にする
    current_game_state = ts.GameStateSet.MENU



    # ゲームループ
    running = True
    while running:
        
        print(frame_count)

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
            screen.blit(img_title[0], [0, 0])
            screen.blit(img_title[1], [340, 80])

            start_color = pygame.Color("blue") if start_button.hovered else pygame.Color("black")
            start_button.draw(start_color, hover_sound=hover_sound)

            continue_color = pygame.Color("blue") if continue_button.hovered else pygame.Color("black")
            continue_button.draw(continue_color, hover_sound=hover_sound)

        #A2 ゲームスタート後ならこうする
        elif current_game_state == "start": # フレームカウントを更新します
                ps.update_scene(screen, frame_count,move_frames,animation_frames,animation_counter)        
                print(frame_count)

                #ps.update_scene(screen, frame_count,move_frames,animation_frames,animation_counter, camera_x, camera_y,camera_speed)
        #A3 ゲームコンティニューしたいならこうする
        elif current_game_state == "countinue":
            # CONTINUEの処理をここに書く         
            # 無限ループしているBGMの停止
            pygame.mixer.music.stop()
            # pygameライブラリを終了する
            pygame.quit()
            # pythonのプログラム自体を終了する
            sys.exit()

        pygame.display.flip()
        # フレームレートを制御します
        clock.tick(60)
        frame_count += 1
        



if __name__=="__main__":
  main()



