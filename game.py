import pygame
import os
# フォントの初期化
pygame.font.init()

# フォントの設定（フォントファイルの絶対パス、フォントサイズ）
font_path = os.path.abspath("font/NotoSansJP-Regular.ttf")
font_size = 36
font = pygame.font.Font(font_path, font_size)

# フォントが正しく読み込まれたか確認
if pygame.font.get_fonts():
    print("Font loaded successfully!")
else:
    print("Error loading font.")