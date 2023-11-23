import pygame
import sys
import random

pygame.init()

class Land:
    def __init__(self):
        self.status = 'Land'
        self.price = random.randint(1000, 5000)  # ランダムな価格
        self.owner = None

# GameState クラス内の変数名を変更
class GameState:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    STATUS_HEIGHT = 100
    TILE_SIZE = 50
    GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
    GRID_HEIGHT = (SCREEN_HEIGHT - STATUS_HEIGHT) // TILE_SIZE

    def __init__(self):
        self.grid = [[Land() for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        self.owned_land = set()
        self.owned_shops = set()
        self.money = 10000
        self.land_count = 0
        self.shop_count = 0
        self.selected_tile = None
        self.clicked_command = None

# GameLayer クラスの抽象化
class GameLayer:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw(self, game_state):
        pass

    def handle_event(self, event, game_state):
        pass

    def execute_command(self, command, game_state):
        pass

# StatusLayer クラス内の変数名とコメントの追加
class StatusLayer(GameLayer):
    def draw(self, game_state):
        pygame.draw.rect(self.screen, (100, 100, 100), (0, 0, game_state.SCREEN_WIDTH, game_state.STATUS_HEIGHT))
        status_text = f"Money: {game_state.money} | Owned Lands: {game_state.land_count} | Owned Shops: {game_state.shop_count}"
        status_surface = self.font.render(status_text, True, (255, 255, 255))
        self.screen.blit(status_surface, (10, 10))


# MapLayer クラス内の変数名の変更
class MapLayer(GameLayer):
    def draw(self, game_state):
        for y in range(game_state.GRID_HEIGHT):
            for x in range(game_state.GRID_WIDTH):
                rect = pygame.Rect(x * game_state.TILE_SIZE, game_state.STATUS_HEIGHT + y * game_state.TILE_SIZE, game_state.TILE_SIZE, game_state.TILE_SIZE)
                current_tile = game_state.grid[y][x]

                if current_tile.owner == 'Player':
                    if current_tile.status == 'Land':
                        pygame.draw.rect(self.screen, (0, 255, 0), rect)
                    elif current_tile.status == 'Shop':
                        pygame.draw.rect(self.screen, (255, 0, 0), rect)
                elif game_state.selected_tile == (x, y):
                    pygame.draw.rect(self.screen, (169, 169, 169), rect)
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)

    def handle_event(self, event, game_state):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左クリック
                mouse_pos = pygame.mouse.get_pos()
                tile_x, tile_y = mouse_pos[0] // game_state.TILE_SIZE, (mouse_pos[1] - game_state.STATUS_HEIGHT) // game_state.TILE_SIZE

                if 0 <= tile_x < game_state.GRID_WIDTH and 0 <= tile_y < game_state.GRID_HEIGHT:
                    game_state.selected_tile = (tile_x, tile_y)



# CommandLayer クラス内の変数名とコメントの追加
class CommandLayer(GameLayer):
    def __init__(self, screen, font):
        super().__init__(screen, font)
        self.dragging = False
        self.drag_offset = (0, 0)

    def draw(self, game_state):
        if game_state.selected_tile:
            pygame.draw.rect(self.screen, (50, 50, 50), pygame.Rect(10, 120, 180, 150))
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(170, 10, 20, 20))

            tile_x, tile_y = game_state.selected_tile
            current_tile = game_state.grid[tile_y][tile_x]

            commands = []

            if current_tile.status == 'Land' and current_tile.owner is None:
                commands.append('Buy Land')
            elif current_tile.status == 'Land' and current_tile.owner == 'Player':
                commands.append('Sell Land')
            elif current_tile.status == 'Shop' and current_tile.owner == 'Player':
                commands.append('Sell Shop')

            for i, command in enumerate(commands):
                text_surface = self.font.render(command, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(100, 160 + i * 40))
                self.screen.blit(text_surface, text_rect)

    def handle_event(self, event, game_state):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左クリック
                mouse_pos = pygame.mouse.get_pos()
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

# ゲームの初期化
screen = pygame.display.set_mode((GameState.SCREEN_WIDTH, GameState.SCREEN_HEIGHT))
pygame.display.set_caption("シミュレーションゲーム")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

game_state = GameState()
status_layer = StatusLayer(screen, font)
map_layer = MapLayer(screen, font)
command_layer = CommandLayer(screen, font)

# ゲームループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            status_layer.handle_event(event, game_state)
            map_layer.handle_event(event, game_state)
            command_layer.handle_event(event, game_state)

    screen.fill((0, 0, 0))
    status_layer.draw(game_state)
    map_layer.draw(game_state)
    command_layer.draw(game_state)

    pygame.display.flip()
    clock.tick(30)