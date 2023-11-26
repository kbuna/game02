import pygame
import sys

pygame.init()

# ユーザー定義のカスタムイベントタイプ
CUSTOM_EVENT_TYPE = pygame.USEREVENT + 1

# カスタムイベントの生成
custom_event = pygame.event.Event(CUSTOM_EVENT_TYPE, message="Hello, Custom Event!")

# カスタムイベントをイベントキューに追加
pygame.event.post(custom_event)

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == CUSTOM_EVENT_TYPE:
            # カスタムイベントが発生したときの処理
            print("カスタムイベントが発生しました:", event.message)

pygame.quit()
sys.exit()
