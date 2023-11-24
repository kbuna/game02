import pygame
import sys
import random


pygame.init()


#土地クラス
#Land文字列、ランダムな整数、所有者はなし
class Land:
    def __init__(self):
        self.status = 'Land'
        self.price = random.randint(1000, 5000)  # ランダムな価格
        self.owner = None




# GameState
# 画面情報、タイル情報、グリッドの個数
class GameState:
    #スクリーンサイズを設定
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    #ステータスの縦幅を設定
    STATUS_HEIGHT = 100
    #タイルのサイズを設定
    TILE_SIZE = 50
    #グリッドの横の個数は、スクリーンの横幅をタイルサイズで割ったもの
    GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
    #グリッドの縦の個数は、スクリーンの縦幅からステータスの縦幅を引いて、タイルサイズで割ったもの
    GRID_HEIGHT = (SCREEN_HEIGHT - STATUS_HEIGHT) // TILE_SIZE

    #GameStateが呼び出されたとき、初期化
    #グリッド、所有土地数、所有店の数をセット、所持金、土地のカウント、店のカウント、
    #選択したタイル、クリックされたコマンド
    def __init__(self):
        self.grid = [[Land() for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        self.owned_land = set()
        self.owned_shops = set()
        self.money = 10000
        self.land_count = 0
        self.shop_count = 0
        self.selected_tile = None
        self.clicked_command = None



# GameLayer
class GameLayer:
    #初期化、描画するスクリーンとフォントを持つ
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw(self, game_state):
        pass

    def handle_event(self, event, game_state):
        pass

    def execute_command(self, command, game_state):
        pass



# StatusLayer ステータス画面の表示
class StatusLayer(GameLayer):
    #ゲームレイヤーを受け取る（スクリーンとフォント）
    #矩形を描画する、(スクリーンに、色指定、)
    def draw(self, game_state):
        pygame.draw.rect(self.screen, (100, 100, 100), (0, 0, game_state.SCREEN_WIDTH, game_state.STATUS_HEIGHT))
        status_text = f"Money: {game_state.money} | Owned Lands: {game_state.land_count} | Owned Shops: {game_state.shop_count}"
        status_surface = self.font.render(status_text, True, (255, 255, 255))
        self.screen.blit(status_surface, (10, 10))

 #矩形を描画するウィンドウの Surface オブジェクトを指定しています。
 # self がクラスのインスタンスであり、
 # screen がそのインスタンスの画面を表すメンバ変数であると仮定します。

#(100, 100, 100): 描画する矩形の色を RGB 形式で指定しています。
# ここでは (100, 100, 100) は灰色を表しています。

#(0, 0, game_state.SCREEN_WIDTH, game_state.STATUS_HEIGHT): 
# 矩形の座標とサイズを指定しています。
# 具体的には、左上隅の x 座標が 0、y 座標が 0 で、
# 横幅が game_state.SCREEN_WIDTH、 =完全な横幅
# 高さが game_state.STATUS_HEIGHT です。 =ステータスの縦幅




# MapLayer クラス内の変数名の変更
class MapLayer(GameLayer):
    #ゲームステートを引数に
    #グリッドの縦の個数回ループ
    #グリッドの横の個数回ループ
    #矩形を描画する、xはタイルサイズ、yは
    def draw(self, game_state):
        for y in range(game_state.GRID_HEIGHT):
            for x in range(game_state.GRID_WIDTH):
                rect = pygame.Rect(x * game_state.TILE_SIZE, game_state.STATUS_HEIGHT + y * game_state.TILE_SIZE, game_state.TILE_SIZE, game_state.TILE_SIZE)
                #現在のタイルは、グリッド
                #二次元配列を作り、各要素にLandクラスのインスタンスを生成している
                #grid = [[Land() for _ in range(グリッドの横)] for _ in range(グリッドの縦)]
                #self.gridは2次元のリストとなり、各セルにはLandクラスの新しいインスタンスが生成されています。
                # これにより、初期状態ではゲームのマップが生成され、各セルはランダムに生成された価格と所有者なしの土地を表します。
                current_tile = game_state.grid[y][x]
                #もしもタイルの所有者がプレイヤーだったら
                if current_tile.owner == 'Player':
                    #かつ、もし、タイルの属性が土地だったら色を指定
                    if current_tile.status == 'Land':
                        pygame.draw.rect(self.screen, (0, 255, 0), rect)
                    #土地ではなくお店だったら色をしてい
                    elif current_tile.status == 'Shop':
                        pygame.draw.rect(self.screen, (255, 0, 0), rect)
                #タイルの所有者がプレイヤーではなく、
                elif game_state.selected_tile == (x, y):
                    pygame.draw.rect(self.screen, (169, 169, 169), rect)
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)

    #イベントハンドラは、ゲームステートと、検出したイベントが送られる

    def handle_event(self, event, game_state):
        #その、イベントタイプが、マウスボタンが押されたら
        if event.type == pygame.MOUSEBUTTONDOWN:
            #かつ、そのイベントが左クリックだったら
            if event.button == 1:  # 左クリック
                #マウスポジションを取得
                mouse_pos = pygame.mouse.get_pos()
                #xとyのタプルを作る
                #  マウスのx座標をgame_state.TILE_SIZEで割った整数部分を取得します。これにより、マウスのx座標がタイルの何番目に相当するか。
                #  マウスのy座標をgame_state.TILE_SIZEで割った整数部分を取得します。これにより、マウスのy座標がタイルの何番目に相当するか。
                tile_x, tile_y = mouse_pos[0] // game_state.TILE_SIZE, (mouse_pos[1] - game_state.STATUS_HEIGHT) // game_state.TILE_SIZE
                #タプルを参照して、xが0以上、グリッドの横の数の上限未満、かつ、yが0以上で、縦の数未満
                if 0 <= tile_x < game_state.GRID_WIDTH and 0 <= tile_y < game_state.GRID_HEIGHT:
                    game_state.selected_tile = (tile_x, tile_y) #選択タイルに、x,yを代入する



# CommandLayer 
# スクリーンとフォントを持つ、
# ドラッグしているかどうか
# ドラッグの座標？
class CommandLayer(GameLayer):
    def __init__(self, screen, font):
        super().__init__(screen, font)
        self.dragging = False
        self.drag_offset = (0, 0)


    #ゲームステートを受け取り描画
    def draw(self, game_state):
        #ゲームステートのタイルが存在したら
        if game_state.selected_tile:
            #コマンドボックスを生成する
            pygame.draw.rect(self.screen, (50, 50, 50), pygame.Rect(10, 120, 180, 150))
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(170, 10, 20, 20))
            #x,yの選択タイル座標を格納
            tile_x, tile_y = game_state.selected_tile
            #グリッドのx,yを格納
            current_tile = game_state.grid[tile_y][tile_x]
            #コマンドの配列を宣言
            commands = []

            #もし、現在のタイルステータスが、土地であり、かつ、所有者がいなければ、
            # Buy Landを追加　その他もリストに追加
            if current_tile.status == 'Land' and current_tile.owner is None:
                commands.append('Buy Land')
            elif current_tile.status == 'Land' and current_tile.owner == 'Player':
                commands.append('Sell Land')
            elif current_tile.status == 'Shop' and current_tile.owner == 'Player':
                commands.append('Sell Shop')

            #列挙型で、コマンドを引き取る
            #enumerate()関数を使うと、forループの中でリストやタプルなどのイテラブルオブジェクトの要素と同時にインデックス番号（カウント、順番）を取得できる。
            for i, command in enumerate(commands):
                #フォントを使ってレンダリング、コマンドを、
                text_surface = self.font.render(command, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(100, 160 + i * 40))
                self.screen.blit(text_surface, text_rect)

    def handle_event(self, event, game_state):
        #もしマウスクリックされたら
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # かつ左クリックなら
                #マウスポジションを取得
                mouse_pos = pygame.mouse.get_pos()
                #
                close_button_clicked = pygame.Rect(170, 10, 20, 20).collidepoint(mouse_pos)
                if close_button_clicked:
                    game_state.selected_tile = None
                else:
                    tile_x, tile_y = game_state.selected_tile
                    current_tile = game_state.grid[tile_y][tile_x]

                    if current_tile.status == 'Land' and current_tile.owner is None:
                        game_state.clicked_command = 'Buy Land'
                    elif current_tile.status == 'Land' and current_tile.owner == 'Player':
                        game_state.clicked_command = 'Sell Land'
                    elif current_tile.status == 'Shop' and current_tile.owner == 'Player':
                        game_state.clicked_command = 'Sell Shop'

                    # execute_command メソッドを呼ぶ
                    self.execute_command(game_state.clicked_command, game_state)

            elif event.button == 3 and game_state.selected_tile:
                # 右クリックでドラッグ可能にする
                self.dragging = True
                mouse_pos = pygame.mouse.get_pos()
                self.drag_offset = (mouse_pos[0] - 10, mouse_pos[1] - 120)

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # ドラッグ中の処理
            mouse_pos = pygame.mouse.get_pos()
            game_state.selected_tile = (
                (mouse_pos[0] - self.drag_offset[0]) // game_state.TILE_SIZE,
                (mouse_pos[1] - self.drag_offset[1] - game_state.STATUS_HEIGHT) // game_state.TILE_SIZE
            )

        elif event.type == pygame.MOUSEBUTTONUP and self.dragging:
            # ドラッグ終了
            self.dragging = False




# ゲームの初期
# スクリーンを、ゲームステートのサイズで描画
screen = pygame.display.set_mode((GameState.SCREEN_WIDTH, GameState.SCREEN_HEIGHT))
#キャプションを設定
pygame.display.set_caption("シミュレーションゲーム")
#クロックを格納
clock = pygame.time.Clock()
#フォント設定
font = pygame.font.Font(None, 36)
#ゲームステートクラスを格納
game_state = GameState()
#各種レイヤークラスを格納 引数はフォントと描画画面
status_layer = StatusLayer(screen, font)
map_layer = MapLayer(screen, font)
command_layer = CommandLayer(screen, font)



# ゲームループ
while True:
    #発生した全てのイベントを処理。
    for event in pygame.event.get():
        #イベントタイプが終了なら、終了
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #それ以外なら、各種レイヤーの、イベントハンドラに、ゲームステートとイベントを送り実行
        else:
            status_layer.handle_event(event, game_state)
            map_layer.handle_event(event, game_state)
            command_layer.handle_event(event, game_state)

    #画面を黒色で塗りつぶします。これは、前のフレームの描画をクリアして新しいフレームを描画するためのものです。
    screen.fill((0, 0, 0))
    #ステータスレイヤーを描画
    status_layer.draw(game_state)
    #マップレイヤーを描画
    map_layer.draw(game_state)
    #コマンドレイヤーを描画
    command_layer.draw(game_state)
    # 画面を更新します。これにより、前述の描画操作が実際に画面に反映されます。
    pygame.display.flip()
    #ゲームのフレームレートを制御します。この場合、1秒あたり30フレームに制限されています。
    clock.tick(30)