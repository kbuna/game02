import pygame
import os
import random





#線形補間 aからbまでの値をtの割合で補間する
def lerp(a, b, t):
    return a + t * (b - a)


#タイル--------------------------------------------
# 1マスのサイズ
TILESIZE = 64
# 右下に向かって何マス描くか
MAPWIDTH = 5
# 右上に向かって何マス描くか
MAPHEIGHT = 10

# タイルの辞書
colours = {
    'grass': (0, 255, 0),
    'dirt': (139, 69, 19)
}

# ランダムに"芝"か"ダート"を持つ、マス設定数の、多次元リストを作る
tilemap = [['grass' if random.randint(0, 1) else 'dirt' for _ in range(MAPWIDTH)] for _ in range(MAPHEIGHT)]

# いくつかの構文を利用した、省略した書き方。
# ⓵リスト内梱包表記
# result = [式 for 変数名 in イテラブルオブジェクト(ループ可能なもの)]
# →for in文の要領でループし、式にかけて処理した値を、ループ数だけリストに追加している

# ②三項演算子
# "grass" if 条件式 else "dirt" 
# 条件に応じて値を選択する。真ならば前者の値に化ける、偽ならば後者の値に化ける

# ➂Truesy(真)か Falsy(偽)か
# if random.randint(0,1)
# 0が出たら偽、1が出たら真ということ

# ④ダミー変数
# for _ in リスト :処理
# ループ内で使用されない場合に、"_"をダミー変数として使う書き方がある

# 上記を合わせて、
# 前者forは、MAPWIDTHの数(3ならば)だけ、
# [芝,ダート,芝]、と言う風に、ランダムに"ダート"か"芝"の文字列が入る、リストができあがる。
# そして、後者のfor文で、MAPHEIGHTの数(3ならば)だけ、
# [[芝,ダート,芝],[芝,芝,芝],[ダート,芝、ダート]]
# という多次元リストが生成される。





# NPCの位置と属性を設定します
npcs = [{'position': [random.randint(0, MAPWIDTH - 1), random.randint(0, MAPHEIGHT - 1)], 'type': 'npc_type_1', 'direction': 'down'} for _ in range(3)]  # 3つのNPCを作成

# "position":[x,y],"type":"npc_type_1","direction":"down"
#  {座標、NPCの属性、方向} を持つNPCを、3人分のリストを作成している。

# [{pos:[],type:"",di:""} for in range(3) ] リスト内梱包でリストを３つのディクショナリをもつリストを、リスト内梱包で作っている。
# npc[0]にキーpositonで、アクセスすると、座標がリストで返ってくる。



#--------------------------カメラ
# カメラの初期位置
camera_x, camera_y = 0, 0
# カメラの速度係数
camera_speed = 0.02



# Pygameを初期化
pygame.init()
#screen = pygame.display.set_mode((1280, 780))  # ウィンドウサイズを1280x780に変更



# 等角投影タイルを作成
isometric_size = int(TILESIZE * 1.5)
isometric_tiles = {}
# タイルのサーフィスを回転・スケーリングし、等角投影に変換しディクショナリに追加

for key, color in colours.items():
    tile_surf = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
    tile_surf.fill(color)
    tile_surf = pygame.transform.rotate(tile_surf, 45)
    tile_surf = pygame.transform.scale(tile_surf, (isometric_size, isometric_size // 2))
    isometric_tiles[key] = tile_surf
# colursは、草とダートの色の設定が入ったディクショナリ
# itmes()は、ディクショナリのキーと値のペアを取得するメソッド
# pygame.Surfaceクラスでオブジェクトを作成。TILESIZE=64x64のタイルを作る
# SRCALPHA、作るサーフィスに透明度を持たせることを示している。
# fill サーフィスオブジェクトに対して、指定した色で塗り粒す
# rotate タイルサーフィスを45度で回転させる 時計回りに回転する
# scale サーフィスを指定されたサイズに拡大または縮小する 
# 横幅はタイルサイズ、縦幅はタイルサイズの半分
# タイルサイズがそのままだと、横幅が縦幅より広く見えるため横方向に拡大して視覚的に調整する
# colorsの設定値が入った、斜めの、スケール調整した、タイルをディクショナリで作る


#アルファチャンネル(透明度)を持つサーフィスは、アルファブレンディングに対応している
#アルファブレンディングとは、描画されるピクセルの透明度に基づいて、既存のピクセルと新しいピクセルを混ぜ合わせるプロセス
#アルファチャンネルを持つサーフィスは、半透明の描画や透明領域を持つ画像を正確に扱うのに役立つ、キャラの影、ガラスの表現など透明度表現
#pygame.Surfaceクラスは、画像や描画対象となる画面の表面を表現するためのクラス。
#1 画像の読み込みと作成   
#   画像を読み込むためにも使用される
#2 画像とグラフィックス処理 
#   pygameの描画関数を使用して、画面上に図形や画像を描画するための対象となる 色の変更や回転拡大縮小などの処理も可能
#3 画像のピクセル操作 
#   ピクセル単位の操作もある。画像の特定のピクセルの色を取得したり設定したりできる
#4 アルファチャンネルと透明度 
#   pygame.SRCALPHAフラグを指定することで、透明度情報をもつサーフィスを作れる
#5 イベント処理
#   マウスクリックなどのイベント発生時に、特定の座標に対して操作を起こなうためのサーフィスを使用することがある


# NPCの画像をロードします
# それぞれ3毎の画像ロード情報が入ったリストを持つ、
# 上下左右のディクショナリを、さらに持つ
# tpc_type1 ディクショナリ
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
#timeモジュール
# time() 現在の時間を返す。unixエポック(1970,01,01,0:00)からの経過時間
# sleep(seconds) 指定した秒数だけプログラムの実行を一時停止,時間経過を待つために使う
# ctime(seconds) 指定した秒数デフォルトはtime()の戻り値を、人が読みやすい形式で表現した文字列を返す
# gmtime(seconds)time()で得られた秒数を"struct_time"オブジェクトとして返す、年月日時刻などの要素にアクセスできるタプル

#clockクラス コンストラクタを呼ぶと、クロックオブジェクトを作る
# tick(fps)で、指定したフレームレートでゲームが実行されるようにする。tick(60)なら1秒辺り60フレーム
# get_time() 最後のtick()を呼び出してから経過した時間をミリ秒単位で返す
# get_rawtime() 上と同じだが、ミリ秒ではなく、内部のタイマーの値を返す
#例えば、clock.tick(60) を呼び出すと、次の clock.tick(60) が呼ばれるまでの経過時間が計測され、それが1秒あたり60フレームになるように調整されます。この間、プログラムは一時的に停止し、次のフレームの描画やゲームロジックの処理が行われます。

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

    
    # 一定のフレーム数経過ごとにNPCを移動 -----------------------------まだ描画はしていない
    # 今回の場合npcsは、 {座標、NPCの属性(画像)、方向} を持つNPCを、3人分のリストを作成している。
    #フレームカウントが、ムーブフレームを超えたら実行
    if frame_count % move_frames == 0:
        for npc in npcs:
            #上下左右のどれかをランダムで決定
            direction = random.choice(['up', 'down', 'left', 'right'])
            #upかつ、npcのポジションキーの[y座標]の値を取る、これが0でなければ、描画の上限でなければ、
            #座標を1減らす(y座標は右下に向かい増えていくので)
            if direction == 'up' and npc['position'][1] > 0:
                npc['position'][1] -= 1
            elif direction == 'down' and npc['position'][1] < MAPHEIGHT - 1:
                npc['position'][1] += 1
            elif direction == 'left' and npc['position'][0] > 0:
                npc['position'][0] -= 1
            elif direction == 'right' and npc['position'][0] < MAPWIDTH - 1:
                npc['position'][0] += 1
            #npcの向きを格納する
            npc['direction'] = direction
            #アニメカウンターのリセット
            npc['animation_counter'] = 0  # アニメーションのカウンタをリセット

    # 画面をクリアして再描画 描画するまえに一旦、黒で塗りつぶす。
    screen.fill((0, 0, 0))  # 黒で塗りつぶす

    # タイルを描画します 
    # 縦方向のマスの数だけ繰り返す。
        for row in range(MAPHEIGHT):
            #isometタイルのキーが、
            tile_surf = isometric_tiles[tilemap[row][column]]
            #タイルのx座標の計算。列番号、マスの数-行番号、*  タイルサイズの1/2 -カメラのxを
            x = (column + (MAPHEIGHT - row)) * isometric_size // 2 - camera_x
            #20はオフセット値
            y = 20 + (column + row) * isometric_size // 4 - camera_y
            #tile画像を、x.yの位置に描画
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




pygame.quit()
