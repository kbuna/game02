import pygame
import sys
import time

# Pygameの初期化
pygame.init()

# 画面の設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ノベルゲーム")

# 色の定義
white = (255, 255, 255)
black = (0, 0, 0)

# フォントの設定
font = pygame.font.Font(None, 36)

# キャラクターの画像読み込み
character_image = pygame.image.load("character.png")
character_rect = character_image.get_rect()
character_rect.center = (screen_width // 2, screen_height // 2)

# ゲームループ
clock = pygame.time.Clock()
running = True
show_choices = False

while running:
    screen.fill(white)

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # キャラクターの表示
    screen.blit(character_image, character_rect)

    # キャラの名前とセリフの表示
    text = font.render("キャラの名前: こんにちは！", True, black)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height - 50))
    screen.blit(text, text_rect)

    # 一定時間後に選択肢を表示
    if not show_choices:
        pygame.display.flip()
        pygame.time.delay(3000)  # 3秒待機
        show_choices = True
    else:
        # 選択肢の表示
        choice1 = font.render("1. はい", True, black)
        choice2 = font.render("2. いいえ", True, black)
        choice1_rect = choice1.get_rect(center=(screen_width // 2, screen_height - 100))
        choice2_rect = choice2.get_rect(center=(screen_width // 2, screen_height - 50))
        screen.blit(choice1, choice1_rect)
        screen.blit(choice2, choice2_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
