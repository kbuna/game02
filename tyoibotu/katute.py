import pygame
import sys

pygame.init()

# 画面のサイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# ステータス領域の高さ
STATUS_HEIGHT = 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("シミュレーションゲーム")

clock = pygame.time.Clock()

# グリッドのパラメータ
TILE_SIZE = 50
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = (SCREEN_HEIGHT - STATUS_HEIGHT) // TILE_SIZE

# グリッドの初期化
grid = [['Land'] * GRID_WIDTH for _ in range(GRID_HEIGHT)]  # 初期値として土地のデータを設定
owned_land = set()  # 購入した土地の座標を保存するセット
owned_shops = set()  # 購入したお店の座標を保存するセット

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

# ボタンのクラス
class Button:
    def __init__(self, rect, command, text):
        self.rect = rect
        self.command = command
        self.text = text
        self.clicked = False  # ボタンがクリックされたかどうかを示すフラグ
        
    def update(self):
        if self.clicked:
            self.clicked = False

    def draw(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (50, 50, 50), self.rect)
        else:
            pygame.draw.rect(screen, (100, 100, 100), self.rect)

        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked = True

# コマンドボタンのリスト
command_buttons = [
    Button(pygame.Rect(10, 150, 150, 30), 'buy_land', 'Buy Land'),
    Button(pygame.Rect(10, 190, 150, 30), 'sell_land', 'Sell Land'),
    Button(pygame.Rect(10, 230, 150, 30), 'buy_shop', 'Buy Shop'),
    Button(pygame.Rect(10, 270, 150, 30), 'sell_shop', 'Sell Shop'),
]

# 閉じるボタン
close_button = Button(pygame.Rect(170, 10, 20, 20), 'close', '×')

# 購入した土地の処理
def buy_land(tile_x, tile_y):
    global money, owned_land_count
    money -= 1000
    owned_land.add((tile_x, tile_y))
    owned_land_count += 1

# 売却した土地の処理
def sell_land(tile_x, tile_y):
    global money, owned_land_count
    money += 500
    owned_land.remove((tile_x, tile_y))
    owned_land_count -= 1

# 購入したお店の処理
def buy_shop(tile_x, tile_y):
    global money, owned_shops_count
    money -= 2000
    owned_shops.add((tile_x, tile_y))
    owned_shops_count += 1

# 売却したお店の処理
def sell_shop(tile_x, tile_y):
    global money, owned_shops_count
    money += 1000  # 仮の売却金額
    owned_shops.remove((tile_x, tile_y))
    owned_shops_count -= 1

# グリッドの描画
def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * TILE_SIZE, STATUS_HEIGHT + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if (x, y) in owned_land:
                pygame.draw.rect(screen, (0, 255, 0), rect)  # 購入した土地は緑色で表示
            elif (x, y) in owned_shops:
                pygame.draw.rect(screen, (255, 0, 0), rect)  # 購入したお店は赤色で表示
            elif selected_tile == (x, y):
                pygame.draw.rect(screen, (169, 169, 169), rect)  # 選択中のタイルはグレーで表示
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
        button.draw()

# ポップアップテキストを描画
def draw_popup_text(text):
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=popup_text_pos)
    screen.blit(text_surface, text_rect)

# ゲームループ
while True:
    clicked_command = None  # クリックされたコマンドを保持する変数

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左クリック
                mouse_pos = pygame.mouse.get_pos()
                tile_x, tile_y = mouse_pos[0] // TILE_SIZE, (mouse_pos[1] - STATUS_HEIGHT) // TILE_SIZE
                if 0 <= tile_x < GRID_WIDTH and 0 <= tile_y < GRID_HEIGHT:
                    selected_tile = (tile_x, tile_y)  # タイルが選択されたら座標を保持
                    for button in command_buttons:
                        button.clicked = False  # コマンドボタンのクリックフラグを初期化
                    close_button.clicked = False  # 閉じるボタンのクリックフラグを初期化
                    if grid[tile_y][tile_x] == 'Land':
                        if (tile_x, tile_y) in owned_land:
                            command_buttons[1].clicked = True  # Sell Land
                        else:
                            command_buttons[0].clicked = True  # Buy Land
                    elif (tile_x, tile_y) in owned_shops:
                        command_buttons[3].clicked = True  # Sell Shop
                    elif grid[tile_y][tile_x] == 'Shop':
                        command_buttons[2].clicked = True  # Buy Shop
                    elif close_button.rect.collidepoint(mouse_pos):
                        close_button.clicked = True

    screen.fill((0, 0, 0))  # 画面をクリア
    mouse_pos = pygame.mouse.get_pos()
    hover_tile_x, hover_tile_y = mouse_pos[0] // TILE_SIZE, (mouse_pos[1] - STATUS_HEIGHT) // TILE_SIZE

    # ステータス領域の描画
    pygame.draw.rect(screen, (100, 100, 100), (0, 0, SCREEN_WIDTH, STATUS_HEIGHT))

    # マップ領域の描画
    draw_grid()
    draw_hover_tile(hover_tile_x, hover_tile_y)  # カーソルがあるタイルの描画

    # カウンターの表示
    counter_text = f"Money: {money} | Owned Lands: {owned_land_count} | Owned Shops: {owned_shops_count}"
    counter_surface = font.render(counter_text, True, (255, 255, 255))
    screen.blit(counter_surface, (10, 10))

    # タイルが選択されていれば、コマンドボックスを描画
    if selected_tile:
        pygame.draw.rect(screen, (50, 50, 50), (10, 120, 180, 150))
        draw_command_buttons()
        close_button.draw()

    # 閉じるボタンがクリックされたらコマンドボックスを閉じる
    if close_button.clicked:
        selected_tile = None
        close_button.clicked = False

    # コマンドボタンがクリックされていれば、対応するコマンドを実行
    for button in command_buttons:
        button.update()
        button.handle_event(pygame.event.Event(pygame.USEREVENT, {}))  # イベントのダミーを生成
        if button.clicked:
            clicked_command = button.command
            button.clicked = False  # クリックフラグを初期化


     # クリックされたコマンドに応じて処理を実行
    if clicked_command and selected_tile:
        tile_x, tile_y = selected_tile
        if clicked_command == 'buy_land' and grid[tile_y][tile_x] == 'Land' and (tile_x, tile_y) not in owned_land:
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