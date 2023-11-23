import pygame
import sys
import os

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("経営型ゲーム")

font = pygame.font.Font(None, 36)

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

hover_sound = load_sound("sound/hover.mp3")  # hover.wav はSEの例です

img_title = [
    load_image("image/o1.webp"),
    load_image("image/logo.png")
]

# ゲームの状態を表す変数
game_state = "menu"  # 初めはメニュー画面

# ボタンのクラス
class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False  # ホバー中かどうかを示す変数
        self.prev_hovered = False  # 前回のホバー状態を記憶する変数

    def draw(self, color, hover_sound=None):
        draw_text(self.text, color, self.rect.centerx, self.rect.centery)

        if hover_sound is not None and self.hovered and not self.prev_hovered:
            hover_sound.play()

    def set_hovered(self, value):
        self.prev_hovered = self.hovered
        self.hovered = value

# ボタンの初期設定
start_button = Button("START", screen_width // 6, screen_height // 4 + 30, 200, 50)
continue_button = Button("CONTINUE", screen_width // 6, screen_height // 4 + 60, 200, 50)

# BGMの読み込みと再生
def load_music(file_path):
    if os.path.exists(file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(-1)
    else:
        raise FileNotFoundError(f"File not found: {file_path}")

load_music("sound/title.mp3")

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu":
                if start_button.rect.collidepoint(event.pos):
                    game_state = "start"
                elif continue_button.rect.collidepoint(event.pos):
                    game_state = "continue"

    # ボタンのホバーエフェクト
    start_button.set_hovered(start_button.rect.collidepoint(pygame.mouse.get_pos()))
    continue_button.set_hovered(continue_button.rect.collidepoint(pygame.mouse.get_pos()))

    screen.fill(pygame.Color("white"))

    if game_state == "menu":
        # タイトルロゴ表示
        screen.blit(img_title[0], [0, 0])
        screen.blit(img_title[1], [340, 80])

        start_color = pygame.Color("blue") if start_button.hovered else pygame.Color("black")
        start_button.draw(start_color, hover_sound=hover_sound)

        continue_color = pygame.Color("blue") if continue_button.hovered else pygame.Color("black")
        continue_button.draw(continue_color, hover_sound=hover_sound)

    pygame.display.flip()

# BGMの停止
pygame.mixer.music.stop()

pygame.quit()
sys.exit()
