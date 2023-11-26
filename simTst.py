import pygame
import sys
import random

pygame.init()

# 画面のサイズ
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# ステータス領域の高さ
STATUS_HEIGHT = 100


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("シミュレーションゲーム")
clock = pygame.time.Clock()


# グリッドのパラメータ
TILE_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = (SCREEN_HEIGHT - STATUS_HEIGHT) // TILE_SIZE

# 土地クラス
class Land:
    def __init__(self):
        self.status = 'Land'
        self.price = random.randint(1000, 5000)  # 土地はランダムな価格になる
        self.owner = None

# グリッドの初期化
grid = [[Land() for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
owned_land = set()
owned_shops = set()

# フォントの設定
font = pygame.font.Font(None, 36)

# ポップアップテキストの位置調整
popup_text_pos = (0, 0)

# 所持金
money = 10000

# カウンターの初期化
owned_land_count = 0
owned_shops_count = 0

# 選択されたタイルの座標を保持する変数
selected_tile = None

# コマンドボタンのリスト
command_buttons = [
    {'rect': pygame.Rect(10, 150, 150, 30), 'command': 'buy_land', 'text': 'Buy Land', 'clicked': False},
    {'rect': pygame.Rect(10, 190, 150, 30), 'command': 'sell_land', 'text': 'Sell Land', 'clicked': False},
    {'rect': pygame.Rect(10, 230, 150, 30), 'command': 'buy_shop', 'text': 'Buy Shop', 'clicked': False},
    {'rect': pygame.Rect(10, 270, 150, 30), 'command': 'sell_shop', 'text': 'Sell Shop', 'clicked': False},
]

# コマンドボックスの位置
command_box_rect = pygame.Rect(10, 120, 180, 150)

# 閉じるボタン
close_button = pygame.Rect(170, 10, 20, 20)

# 購入した土地の処理
def buy_land(tile_x, tile_y):
    global money, owned_land_count
    money -= grid[tile_y][tile_x].price
    grid[tile_y][tile_x].owner = 'Player'
    owned_land.add((tile_x, tile_y))
    owned_land_count += 1

# 売却した土地の処理
def sell_land(tile_x, tile_y):
    global money, owned_land_count
    money += grid[tile_y][tile_x].price // 2
    grid[tile_y][tile_x].owner = None
    owned_land.remove((tile_x, tile_y))
    owned_land_count -= 1

# 購入したお店の処理
def buy_shop(tile_x, tile_y):
    global money, owned_shops_count
    money -= 2000  # 仮の店舗購入価格
    grid[tile_y][tile_x].owner = 'Player'
    owned_shops.add((tile_x, tile_y))
    owned_shops_count += 1

# 売却したお店の処理
def sell_shop(tile_x, tile_y):
    global money, owned_shops_count
    money += 1000  # 仮の店舗売却価格
    grid[tile_y][tile_x].owner = None
    owned_shops.remove((tile_x, tile_y))
    owned_shops_count -= 1

# グリッドの描画
def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * TILE_SIZE, STATUS_HEIGHT + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            current_tile = grid[y][x]

            if current_tile.owner == 'Player':
                if current_tile.status == 'Land':
                    pygame.draw.rect(screen, (0, 255, 0), rect)
                elif current_tile.status == 'Shop':
                    pygame.draw.rect(screen, (255, 0, 0), rect)
            elif selected_tile == (x, y):
                pygame.draw.rect(screen, (169, 169, 169), rect)
            else:
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)

# カーソルがあるタイルの描画
def draw_hover_tile(hover_tile_x, hover_tile_y):
    if 0 <= hover_tile_x < GRID_WIDTH and 0 <= hover_tile_y < GRID_HEIGHT:
        rect = pygame.Rect(hover_tile_x * TILE_SIZE, STATUS_HEIGHT + hover_tile_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)

# コマンドボックス内のコマンドボタンを描画
def draw_command_buttons():
    for button in command_buttons:
        pygame.draw.rect(screen, (100, 100, 100), button['rect'])
        text_surface = font.render(button['text'], True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=button['rect'].center)
        screen.blit(text_surface, text_rect)

# ポップアップテキストを描画
def draw_popup_text(text):
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=popup_text_pos)
    screen.blit(text_surface, text_rect)

# ゲームループ
while True:

    clicked_command = None  # クリックされたコマンドを保持する変数
    #イベントキューをチェックする
    for event in pygame.event.get():
        #QUITならば
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左クリック
                mouse_pos = pygame.mouse.get_pos()
                tile_x, tile_y = mouse_pos[0] // TILE_SIZE, (mouse_pos[1] - STATUS_HEIGHT) // TILE_SIZE

                # タイルの範囲内でクリックされた場合
                if 0 <= tile_x < GRID_WIDTH and 0 <= tile_y < GRID_HEIGHT:
                    selected_tile = (tile_x, tile_y)  # タイルが選択されたら座標を保持

                    # コマンドボタンのクリックフラグを初期化
                    for button in command_buttons:
                        button['clicked'] = False

                    close_button_clicked = close_button.collidepoint(mouse_pos)

                    # タイルが土地である場合
                    if grid[tile_y][tile_x].status == 'Land':
                        # タイルがプレイヤーの所有地である場合
                        if (tile_x, tile_y) in owned_land:
                            command_buttons[1]['clicked'] = True  # Sell Land
                        else:
                            command_buttons[0]['clicked'] = True  # Buy Land

                    # タイルがプレイヤーの所有店舗である場合
                    elif (tile_x, tile_y) in owned_shops:
                        command_buttons[3]['clicked'] = True  # Sell Shop

                    # タイルが店舗である場合
                    elif grid[tile_y][tile_x].status == 'Shop':
                        command_buttons[2]['clicked'] = True  # Buy Shop

                    # 閉じるボタンがクリックされた場合
                    elif close_button_clicked:
                        selected_tile = None

    screen.fill((0, 0, 0))  # 画面をクリア
    mouse_pos = pygame.mouse.get_pos()
    hover_tile_x, hover_tile_y = mouse_pos[0] // TILE_SIZE, (mouse_pos[1] - STATUS_HEIGHT) // TILE_SIZE

    # ステータス領域の描画
    pygame.draw.rect(screen, (100, 100, 100), (0, 0, SCREEN_WIDTH, STATUS_HEIGHT))

    # マップ領域の描画
    draw_grid()
    draw_hover_tile(hover_tile_x, hover_tile_y)  # カーソルがあるタイルの描画

    # カウンターの表示
    counter_text = f"お金: {money} | 土地所有数: {owned_land_count} | お店所有数: {owned_shops_count}"
    counter_surface = font.render(counter_text, True, (255, 255, 255))
    screen.blit(counter_surface, (10, 10))

    # タイルが選択されていれば、コマンドボックスを描画
    if selected_tile:
        pygame.draw.rect(screen, (50, 50, 50), command_box_rect)
        draw_command_buttons()
        pygame.draw.rect(screen, (255, 0, 0), close_button)

    # 閉じるボタンがクリックされたらコマンドボックスを閉じる
    if close_button.collidepoint(mouse_pos):
        selected_tile = None

    # コマンドボタンがクリックされていれば、対応するコマンドを実行
    for button in command_buttons:
        if button['clicked']:
            clicked_command = button['command']
            button['clicked'] = False  # クリックフラグを初期化

    # クリックされたコマンドに応じて処理を実行
    if clicked_command and selected_tile:
        tile_x, tile_y = selected_tile
        current_tile = grid[tile_y][tile_x]

        if clicked_command == 'buy_land':
            buy_land(tile_x, tile_y)
        elif clicked_command == 'sell_land':
            sell_land(tile_x, tile_y)
        elif clicked_command == 'buy_shop':
            buy_shop(tile_x, tile_y)
        elif clicked_command == 'sell_shop':
            sell_shop(tile_x, tile_y)

        selected_tile = None  # コマンド実行後は選択を解除

    pygame.display.flip()
    clock.tick(30)
