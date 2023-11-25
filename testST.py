import pygame
import sys
import os
from Isomet2 import generate_tilemap, generate_npcs, main_game_loop

pygame.init()

# スクリーンサイズ
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("経営型ゲーム")
font = pygame.font.Font(None, 36)

# ゲームの状態
class GameState:
    MENU = "menu"
    START = "start"
    CONTINUE = "continue"

# 画像の読み込み
def load_image(file_path):
    if os.path.exists(file_path):
        return pygame.image.load(file_path)
    else:
        raise FileNotFoundError(f"File not found: {file_path}")

# 効果音の読み込み
def load_sound(file_path):
    if os.path.exists(file_path):
        return pygame.mixer.Sound(file_path)
    else:
        raise FileNotFoundError(f"File not found: {file_path}")

# BGMの読み込みと再生
def load_music(file_path):
    if os.path.exists(file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(-1)
    else:
        raise FileNotFoundError(f"File not found: {file_path}")

# テキストを描画する関数
def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# ボタンのクラス
class Button:
    def __init__(self, text, x, y, width, height):
        self._rect = pygame.Rect(x, y, width, height)
        self._text = text
        self._hovered = False
        self._prev_hovered = False

    def draw(self, color, hover_sound=None):
        draw_text(self._text, color, self._rect.centerx, self._rect.centery)

        if hover_sound is not None and self._hovered and not self._prev_hovered:
            hover_sound.play()

    def set_hovered(self, value):
        self._prev_hovered = self._hovered
        self._hovered = value

    @property
    def rect(self):
        return self._rect

    @property
    def hovered(self):
        return self._hovered

# ボタンの位置を設定
start_button = Button("START", SCREEN_WIDTH // 6, SCREEN_HEIGHT // 4 + 30, 200, 50)
continue_button = Button("CONTINUE", SCREEN_WIDTH // 6, SCREEN_HEIGHT // 4 + 60, 200, 50)

# 画像と効果音のインスタンス
img_title = [load_image("image/o1.webp"), load_image("image/logo.png")]
hover_sound = load_sound("sound/hover.mp3")

# BGMを読み込み・再生
load_music("sound/title.mp3")


# ゲームの状態を初期化
game_state = GameState.MENU

# ゲームデータの生成
tilemap = generate_tilemap(20, 20)
npcs = generate_npcs(20, 20, 3)

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == GameState.MENU:
                if start_button.rect.collidepoint(event.pos):
                    game_state = GameState.START
                elif continue_button.rect.collidepoint(event.pos):
                    game_state = GameState.CONTINUE

    # ボタンのホバーエフェクト
    start_button.set_hovered(start_button.rect.collidepoint(pygame.mouse.get_pos()))
    continue_button.set_hovered(continue_button.rect.collidepoint(pygame.mouse.get_pos()))

    screen.fill(pygame.Color("white"))

    if game_state == GameState.MENU:
        # タイトルロゴ表示
        screen.blit(img_title[0], [0, 0])
        screen.blit(img_title[1], [340, 80])

        start_color = pygame.Color("blue") if start_button.hovered else pygame.Color("black")
        start_button.draw(start_color, hover_sound=hover_sound)

        continue_color = pygame.Color("blue") if continue_button.hovered else pygame.Color("black")
        continue_button.draw(continue_color, hover_sound=hover_sound)

    elif game_state == GameState.START:
           # STARTボタンが押されたら、別のファイルのコードを直接実行
           exec(open("Isomet2.py", errors="ignore").read(), globals())


    elif game_state == GameState.CONTINUE:
        # CONTINUEの処理をここに書く
        pass

    pygame.display.flip()

# BGMの停止
pygame.mixer.music.stop()

pygame.quit()
sys.exit()
