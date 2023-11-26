import pygame
import sys
import os
import random


#title------------------------------------------------------------------

# 初期設定
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
tmr = 0
# ゲームの状態クラス
# メニュー状態、スタート状態、コンティニュー状態を持つ
class GameStateSet:
    MENU = "menu"
    START = "start"
    CONTINUE = "continue"

# ファイルパスを引数に、ロードしたものを返す
# 画像情報はblitで使う
def load_image(file_path):
    if os.path.exists(file_path):
        return pygame.image.load(file_path)
    else:
        raise FileNotFoundError(f"File not found: {file_path}")

# pygame.mixer.sound.playで音を再生する
def load_sound(file_path):
    if os.path.exists(file_path):
        return pygame.mixer.Sound(file_path)
    else:
        raise FileNotFoundError(f"File not found: {file_path}")

# play(-1)は、ループ再生の回数。-1は無限ループ。
def load_music(file_path):
    if os.path.exists(file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(-1)
    else:
        raise FileNotFoundError(f"File not found: {file_path}")




# ゲームデータの生成
# tilemap = generate_tilemap(20, 20)
# npcs = generate_npcs(20, 20, 3)

#title------------------------------------------------------------------


def lerp(a, b, t):
    return a + t * (b - a)

# 1マスのサイズ
TILESIZE = 64
# 右下に向かって何マス描くか
MAPWIDTH = 5
# 右上に向かって何マス描くか
MAPHEIGHT = 10
# ランダムに"芝"か"ダート"を持つ、マス設定数の、多次元リストを作る
tilemap = [['grass' if random.randint(0, 1) else 'dirt' for _ in range(MAPWIDTH)] for _ in range(MAPHEIGHT)]


# タイルの辞書
colours = {
    'grass': (0, 255, 0),
    'dirt': (139, 69, 19)
}

# NPCの位置と属性を設定します
npcs = [{'position': [random.randint(0, MAPWIDTH - 1), random.randint(0, MAPHEIGHT - 1)], 'type': 'npc_type_1', 'direction': 'down'} for _ in range(3)]  # 3つのNPCを作成

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




def main():

    #pygameを初期化
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("経営型ゲーム")
    font = pygame.font.Font(None, 36)
    pygame.mixer.init()

    global tmr

    # テキストを描画する関数
    def draw_text(text, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)


    # ボタンのクラス
    class Button:
        #ボタンは、矩形属性(x,y,w,h)、テキスト、ホバーしているか、ホバー前からの真偽値を持つ
        def __init__(self, text, x, y, width, height):
            self._rect = pygame.Rect(x, y, width, height)
            self._text = text
            self._hovered = False
            self._prev_hovered = False
        #ボタンは上記の要素に加えて、色と、ホバー時のサウンドを使って描画される   
        def draw(self, color, hover_sound=None):
            #テキストを描画する、色と、縦横の中心の位置を使って
            draw_text(self._text, color, self._rect.centerx, self._rect.centery)
            #ボタンがサウンドを持っていて、ホバーしていて、ホバー前でないならば音を鳴らす
            if hover_sound is not None and self._hovered and not self._prev_hovered:
                hover_sound.play()
        #プロパティ。ホバー以前にホバー状態の値を入れてから、ホバー状態かどうかを新たにセットする。
        def set_hovered(self, value):
            self._prev_hovered = self._hovered
            self._hovered = value
        #プロパティ。矩形情報をセットする
        #none からtrueが入ったらロジックエラーにならない？
        @property
        def rect(self):
            return self._rect
        #プロパティ。ホバー
        @property
        def hovered(self):
            return self._hovered




    # スタートとコンティニューのボタンの位置を設定
    # 描画する文字、描画し始めるxの座標、yの座標、横幅、縦幅、
    #  0,0→   x+
    # ↓
    #  y+
    start_button = Button("START", SCREEN_WIDTH // 6, SCREEN_HEIGHT // 4 + 30, 200, 50)
    continue_button = Button("CONTINUE", SCREEN_WIDTH // 6, SCREEN_HEIGHT // 4 + 60, 200, 50)
    # タイトル画像とホバー効果音を設定
    img_title = [load_image("image/o1.webp"), load_image("image/logo.png")]
    hover_sound = load_sound("sound/hover.mp3")
    # タイトルBGMを読み込み・再生
    load_music("sound/title.mp3")




    # NPCが移動するフレーム数を設定します
    move_frames = 30
    frame_count = 0

    # NPCの歩行アニメーションに関する設定
    animation_frames = 10  # 1歩のアニメーションを10フレームかけて描画
    animation_counter = 0

    # ゲームループのフレームレートを制御するためのClockオブジェクトを作成します
    clock = pygame.time.Clock()




    # カメラの初期位置
    camera_x, camera_y = 0, 0
    # カメラの速度係数
    camera_speed = 0.02




    # 等角投影タイルを作成....
    isometric_size = int(TILESIZE * 1.5)
    isometric_tiles = {}

    for key, color in colours.items():
        tile_surf = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        tile_surf.fill(color)
        tile_surf = pygame.transform.rotate(tile_surf, 45)
        tile_surf = pygame.transform.scale(tile_surf, (isometric_size, isometric_size // 2))
        isometric_tiles[key] = tile_surf
        
    def draw_isometric_tile(surface, key, column, row):
        x = (column + (MAPHEIGHT - row)) * isometric_size // 2 - camera_x
        y = 20 + (column + row) * isometric_size // 4 - camera_y
        surface.blit(isometric_tiles[key], (x, y))



    # 現在のゲーム状態を、メニュー状態にする
    current_game_state = GameStateSet.MENU
















    # ゲームループ
    running = True
    while running:

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
                #クリックイベントであるなら、現在のゲーム状態をチェックする、
                #クリックイベントのポジション属性の座標が、スタートボタンの矩形範囲内にあるかどうか
                #collidepointは,単純にこう比較している 
                # rectの左端 <= pos.x <=rectの右端  and  rectの上端 <= pos.y <= rectの下端
                # pygameは 左端はx,y=0,0から  右端に向かって値が増えていくので、xが高いほど右側で、yが高いほど下側になる

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
            elif current_game_state == "start":
                # 一定のフレーム数ごとにNPCを移動
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
                    screen.fill((0, 0, 0))  # 黒で塗りつぶす

                # タイルを描画します
                for column in range(MAPWIDTH):
                    for row in range(MAPHEIGHT):
                        tile_surf = isometric_tiles[tilemap[row][column]]
                        x = (column + (MAPHEIGHT - row)) * isometric_size // 2 - camera_x
                        y = 20 + (column + row) * isometric_size // 4 - camera_y
                        screen.blit(tile_surf, (x, y))
                # NPCを描画します
                for npc in npcs:
                    x = (npc['position'][0] + (MAPHEIGHT - npc['position'][1])) * isometric_size // 2 - camera_x
                    y = 20 + (npc['position'][0] + npc['position'][1]) * isometric_size // 4 - camera_y

                    # 歩行アニメーションのための画像を選択
                    animation_list = npc_images[npc['type']][npc['direction']]
                    animation_counter = npc['animation_counter'] // (animation_frames // len(animation_list))
                    npc_image = animation_list[animation_counter % len(animation_list)]

                    screen.blit(npc_image, (x, y))

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






            #A3 ゲームコンティニューしたいならこうする
            elif current_game_state == "countinue":
                # CONTINUEの処理をここに書く         
                # 無限ループしているBGMの停止
                pygame.mixer.music.stop()
                # pygameライブラリを終了する
                pygame.quit()
                # pythonのプログラム自体を終了する
                sys.exit()

        #スクリーンを白で塗りつぶす
        #screen.fill(pygame.Color("white"))




        #イベントハンドラの説明
        #pygame.eventモジュール。ユーザ操作やゲーム内イベント(キーの押下、マウス移動、ウィンドウを閉じる)を取得するためにある。
        #.get()は発生したすべてのイベントを取得するメソッド。
        # 通常は明示的にイベントを生成する必要はなく、ユーザの入力やシステム状態変更によってイベントが発生する。

        # Eventクラスで、イベントを生成する
        #例 close_event = pygame.event.Event(pygame.QUIT)
        #仕様 event = pygame.event.Event(event_type, key=value, other_key=other_value)#イベントの種類、どのキーがおされたかなど

        # 生成したイベントをイベントキューに追加
        # 引数には、Eventクラスのインスタンスが入り、イベントキューに投稿する。カスタムイベントを作るのに使う。
        # pygame.event.post(close_event)

        #イベントキューは、イベントが一時的に保管されるデータ構造、先入れ先出しの順序でイベントを取り出す。
        #ユーザー入力やシステムイベントを保持して、プログラムがこれらのイベントに対応できるようにする。
        # eventモジュールのget()メソッドは,イベントキューからすべてのイベントを取得して、リストとして返す。

        #そのほかのイベントキュー操作のメソッド
        # get()イベントキュー内のイベントをリストで取得 post()イベントキューにイベントを追加
        # event.pump() キュー内のイベントを処理して、内部的に保持している状態を更新する。
        # event.clear() キュー内のイベントを削除する ウィンドウの再描画やゲームの状態が大きく変わるとき
        
        #イベントキュー内から特定のイベントのみを処理する方法
        #get()で取得したイベントリストをフィルタリングする。
        # if event.type == pygame.QUIT という書き方で、forループからイベントを一つづつ取り出して、該当イベントかをチェックできる。

        #イベントタイプ
        #pygame. 
        # QUIT ウィンドウを閉じるボタンが押されたときのイベント
        # KEYDOWN / KEYUP   キーが押されたか離されたときのイベント  event.keyでどのキーが押されたかを取得できる
        # MOUSEMOTION      マウスが移動したとき event.posで現在のマウス座標が取得できる
        # MOUSEBUTTONDOWN  マウスが押されたか離された event.buttonでどのボタンが押されたかを取得
        # MOUSEBUTTONUP 
        # MOUSEWHEEL マウスホイールが操作されたとき event.yでホイールの垂直方向の移動量が取得できる
        # ACTIVEEVENT ウィンドウがアクティブが非アクティブ event.gainで 1ならアクティブ 2なら非アクティブ
        # USEREVENT ユーザーが定義したイベントタイプ eventオブジェクトの属性にカスタム情報を格納できる

        #詳説
        # イベントキューのfor文内では、イベントキューに積まれた最古のイベントを１つづつevent内に格納していく。
        #  ここに格納される基本的なイベントは、いくつかのtypeのテンプレートがある。
        #  typeを見ればイベントの種類がわかり、例えばACTIVEEVENTであるものは、同時にgainの値には1か2が入っている。
        # ちなみにpythonでは、フィールドや値に当たるものは、属性と呼ぶ。

        #カスタムイベントの扱い方
        # ⓵ 新たにイベントタイプを作る
        # CUSTOM_EVENT_TYPE = pygame.USEREVENT + 1
        # ② Eventクラスに、イベントタイプを使って、カスタムイベントを生成 
        # custom_event = pygame.event.Event(CUSTOM_EVENT_TYPE, message="Hello, Custom Event!")
        # ➂ カスタムイベントをイベントキューに追加
        # pygame.event.post(custom_event)
        # ④ イベントハンドラ内で、イベントキューからカスタムイベントが来るかをチェックする
        # for event in pygame.event.get() if event.type == CUSTOM_EVENT_TYPE: print(event.message)



        ##②
        ##使い方としてはイベントタイプが==ならば、任意の属性はどんな値か？というふうに使える。
        ##このときEVENTクラスは引数に、指定した属性と値を持ったクラスを、好きに作ることができる。
        ##この仕様は、特殊？ クラスの属性(フィールド)はあらかじめ定義が必要では？
        ##謎回答⓵ 動的に属性を追加すること自体は、objectクラスを継承することで可能。（しかしpygameはこの仕様で作っていない）
        ##謎回答② Pygameライブラリは、C言語で書かれており、内部的にはC言語の"構造体"を、によって作られている。
        ##謎回答②-2 C構造体をPythonのクラスでラップすることで、Pythonで操作できている
        ##Pygameユーザーは、C言語における処理を、Pythonで扱うためのインターフェースとして、EVENTクラスなどを扱っている。
        ##わからんこと⓵、C言語は静的型付けなので値には型が必要。pygameのEventクラスは、好きな引数を持つイベントを生成できる。
        ##むしろ動的型付けができるpython向きなのでは？


        #⓵
        # +1は、そもそもイベントタイプは整数型の定数だから可能。
        # pygameライブラリの内部で、そのようにpythonコードで定義されている。
        # 例えば、enum[ USEREVENT =24]というように定義されている。
        # 下記は、具体的な内部的なイベントの定義
        """
        QUIT              = 0x100
        ACTIVEEVENT       = 0x101
        KEYDOWN           = 0x102
        KEYUP             = 0x103
        MOUSEMOTION       = 0x104
        MOUSEBUTTONDOWN   = 0x105
        MOUSEBUTTONUP     = 0x106
        JOYAXISMOTION     = 0x107
        JOYBALLMOTION     = 0x108
        JOYHATMOTION      = 0x109
        JOYBUTTONDOWN     = 0x10A
        JOYBUTTONUP       = 0x10B
        VIDEORESIZE       = 0x10C
        VIDEOEXPOSE       = 0x10D
        USEREVENT         = 0x8000
        """



        pygame.display.flip()
        #ウィンドウの表示を更新するメソッド
        #説明
        #ループ内でオブジェクトが変更されたとき、バックバッファに一時的に格納される
        #flip()は、このバックバッファをフロントバッファ(ユーザが見る画面が最新の状態)の内容に入れ替える。
        #これらの仕様をダブルバッファリングといい、画面のちらつきを軽減する
        #詳説
        #バッファとは、データを一時的に格納したり処理するためのメモリ領域。画像や描画データを一時保存する、
        #Back Bufferは、描画された変更や新しい画像が最初に保持されるメモリ領域。表示される前にここで変更が行われる。
        #Front Bufferは、バックバッファの変更が完了した後に、これらのバッファを入れ替えて、画面に新しく描画が表示される








if __name__=="__main__":
  main()



