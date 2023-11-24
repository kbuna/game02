import pygame
import sys
import random

pygame.init()

class Land:
    def __init__(self):
        self.status = 'Land'
        self.price = random.randint(1000, 5000)
        self.owner = None

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

class StatusLayer(GameLayer):
    def draw(self, game_state):
        pygame.draw.rect(self.screen, (100, 100, 100), (0, 0, game_state.SCREEN_WIDTH, game_state.STATUS_HEIGHT))
        status_text = f"Money: {game_state.money} | Owned Lands: {game_state.land_count} | Owned Shops: {game_state.shop_count}"
        status_surface = self.font.render(status_text, True, (255, 255, 255))
        self.screen.blit(status_surface, (10, 10))

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
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                tile_x, tile_y = mouse_pos[0] // game_state.TILE_SIZE, (mouse_pos[1] - game_state.STATUS_HEIGHT) // game_state.TILE_SIZE

                if 0 <= tile_x < game_state.GRID_WIDTH and 0 <= tile_y < game_state.GRID_HEIGHT:
                    game_state.selected_tile = (tile_x, tile_y)

class CommandLayer(GameLayer):
    def __init__(self, screen, font):
        super().__init__(screen, font)
        self.dragging = False
        self.drag_offset = (0, 0)

    def draw(self, game_state):
        if game_state.selected_tile:
            pygame.draw.rect(self.screen, (50, 50, 50), pygame.Rect(610, 10, 180, 150))
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(760, 10, 20, 20))

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
                text_rect = text_surface.get_rect(center=(700, 40 + i * 40))
                command_box_center = (700, 40 + i * 40)
                self.screen.blit(text_surface, text_rect)

                # コマンドボックスのRectを作成
                command_box_rect = pygame.Rect(610, 10 + i * 40, 180, 40)

                # クリックされた位置がコマンドボックス内かどうかを判定
                if command_box_rect.collidepoint(pygame.mouse.get_pos()):
                    # マウスがクリックされた瞬間だけ実行
                    if pygame.mouse.get_pressed()[0]:  # 左クリック
                        self.execute_command(command, game_state)

    def handle_event(self, event, game_state):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                close_button_clicked = pygame.Rect(760, 10, 20, 20).collidepoint(mouse_pos)
                if close_button_clicked:
                    game_state.selected_tile = None
                else:
                    tile_x, tile_y = game_state.selected_tile
                    current_tile = game_state.grid[tile_y][tile_x]

                    commands = []

                    if current_tile.status == 'Land' and current_tile.owner is None:
                        commands.append('Buy Land')
                    elif current_tile.status == 'Land' and current_tile.owner == 'Player':
                        commands.append('Sell Land')
                    elif current_tile.status == 'Shop' and current_tile.owner == 'Player':
                        commands.append('Sell Shop')

                    for command in commands:
                        command_box_rect = pygame.Rect(610, 10 + commands.index(command) * 40, 180, 40)
                        if command_box_rect.collidepoint(mouse_pos):
                            if pygame.mouse.get_pressed()[0]:  # 左クリック
                                self.execute_command(command, game_state)
                                break

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and game_state.selected_tile:
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

    def execute_command(self, command, game_state):
        if command == 'Buy Land':
            # Buy Landの処理
            tile_x, tile_y = game_state.selected_tile
            selected_tile = game_state.grid[tile_y][tile_x]

            # 所持金が購入価格以上かつ、選択中のタイルがLandでかつ未所有の場合
            if game_state.money >= selected_tile.price and selected_tile.status == 'Land' and selected_tile.owner is None:
                # 所持金を減らす
                game_state.money -= selected_tile.price
                # 所有土地のセットに追加
                game_state.owned_land.add((tile_x, tile_y))
                # 所有土地の総数を増やす
                game_state.land_count += 1
                # 選択中のタイルの所有者を'Player'に設定
                selected_tile.owner = 'Player'
                # 選択中のタイルの色を変更
                selected_tile_color = (0, 255, 0)  # 例として緑に設定
                pygame.draw.rect(self.screen, selected_tile_color, pygame.Rect(tile_x * game_state.TILE_SIZE, game_state.STATUS_HEIGHT + tile_y * game_state.TILE_SIZE, game_state.TILE_SIZE, game_state.TILE_SIZE))

        elif command == 'Sell Land':
            # Sell Landの処理
            tile_x, tile_y = game_state.selected_tile
            selected_tile = game_state.grid[tile_y][tile_x]

            # 選択中のタイルがLandでかつ所有者がPlayerの場合
            if selected_tile.status == 'Land' and selected_tile.owner == 'Player':
                # 所持金を増やす（購入価格の半額）
                game_state.money += selected_tile.price // 2
                # 所有土地のセットから削除
                game_state.owned_land.remove((tile_x, tile_y))
                # 所有土地の総数を減らす
                game_state.land_count -= 1
                # 選択中のタイルの所有者をNoneに設定
                selected_tile.owner = None
                # 選択中のタイルの色を変更
                selected_tile_color = (255, 255, 255)  # 白に設定
                pygame.draw.rect(self.screen, selected_tile_color, pygame.Rect(tile_x * game_state.TILE_SIZE, game_state.STATUS_HEIGHT + tile_y * game_state.TILE_SIZE, game_state.TILE_SIZE, game_state.TILE_SIZE), 1)

        elif command == 'Buy Shop':
            # Buy Shopの処理
            tile_x, tile_y = game_state.selected_tile
            selected_tile = game_state.grid[tile_y][tile_x]

            # 所持金が購入価格以上かつ、選択中のタイルがShopでかつ未所有の場合
            if game_state.money >= selected_tile.price and selected_tile.status == 'Shop' and selected_tile.owner is None:
                # 所持金を減らす
                game_state.money -= selected_tile.price
                # 所有店のセットに追加
                game_state.owned_shops.add((tile_x, tile_y))
                # 所有店の総数を増やす
                game_state.shop_count += 1
                # 選択中のタイルの所有者を'Player'に設定
                selected_tile.owner = 'Player'
                # 選択中のタイルの色を変更
                selected_tile_color = (255, 0, 0)  # 例として赤に設定
                pygame.draw.rect(self.screen, selected_tile_color, pygame.Rect(tile_x * game_state.TILE_SIZE, game_state.STATUS_HEIGHT + tile_y * game_state.TILE_SIZE, game_state.TILE_SIZE, game_state.TILE_SIZE))

        elif command == 'Sell Shop':
            # Sell Shopの処理
            tile_x, tile_y = game_state.selected_tile
            selected_tile = game_state.grid[tile_y][tile_x]

            # 選択中のタイルがShopでかつ所有者がPlayerの場合
            if selected_tile.status == 'Shop' and selected_tile.owner == 'Player':
                # 所持金を増やす（購入価格の半額）
                game_state.money += selected_tile.price // 2
                # 所有店のセットから削除
                game_state.owned_shops.remove((tile_x, tile_y))
                # 所有店の総数を減らす
                game_state.shop_count -= 1
                # 選択中のタイルの所有者をNoneに設定
                selected_tile.owner = None
                # 選択中のタイルの色を変更
                selected_tile_color = (255, 255, 255)  # 白に設定
                pygame.draw.rect(self.screen, selected_tile_color, pygame.Rect(tile_x * game_state.TILE_SIZE, game_state.STATUS_HEIGHT + tile_y * game_state.TILE_SIZE, game_state.TILE_SIZE, game_state.TILE_SIZE), 1)


screen = pygame.display.set_mode((GameState.SCREEN_WIDTH, GameState.SCREEN_HEIGHT))
pygame.display.set_caption("シミュレーションゲーム")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

game_state = GameState()
status_layer = StatusLayer(screen, font)
map_layer = MapLayer(screen, font)
command_layer = CommandLayer(screen, font)

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
