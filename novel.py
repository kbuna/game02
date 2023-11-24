import pygame
import sys
import os

# Pygameの初期化
pygame.init()

# フォントファイルのパス
font_path = os.path.join(os.path.dirname(__file__), 'NotoSansJP-Regular.ttf')

# 画面のサイズと作成
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ノベルゲーム")

# フォントの設定
font = pygame.font.Font(font_path, 36)

# テキスト表示関数
def display_text(lines, current_line, current_char):
    y_offset = 50
    for i, line in enumerate(lines):
        if i < current_line:
            # 既に表示された行は完全に表示
            text_surface = font.render(line, True, (255, 255, 255))
        elif i == current_line:
            # 現在の行は一部だけ表示
            text_surface = font.render(line[:current_char], True, (255, 255, 255))
        else:
            # これから表示される行は非表示
            text_surface = font.render("", True, (255, 255, 255))

        screen.blit(text_surface, (50, y_offset))  # テキストの位置を調整
        y_offset += text_surface.get_height()

# ページごとのテキストのリスト
novel_pages = [
    [
        "これはテストです。画面に収めるために改行を入れます。",
        "改行された部分です。",
        "次のシーンに進みます。",
    ],
    [
        "新しいページのテキストです。",
        "このページも順番に表示されます。",
    ],
    [
        "最後のページの文章です。",
        "これでノベルゲームのページ遷移が実装されました。",
    ]
]

# 現在のページのインデックス
current_page_index = 0

# 現在の行のインデックス
current_line_index = 0

# 現在の文字のインデックス
current_char_index = 0

# クリック待ちフラグ
waiting_for_click = False

# ゲームループ
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            if waiting_for_click:
                # クリック待ち状態であれば、次の行またはページに進む
                if current_line_index < len(novel_pages[current_page_index]) - 1 or current_char_index < len(novel_pages[current_page_index][-1]):
                    current_line_index += 1
                    current_char_index = 0
                    waiting_for_click = False
                else:
                    current_page_index += 1
                    current_line_index = 0
                    current_char_index = 0
                    waiting_for_click = False

    screen.fill((0, 0, 0))  # 画面をクリア

    # 現在のテキストを表示（タイピングアニメーション）
    display_text(novel_pages[current_page_index], current_line_index, current_char_index)

    pygame.display.flip()  # 画面を更新

    if current_line_index < len(novel_pages[current_page_index]) - 1 or current_char_index < len(novel_pages[current_page_index][current_line_index]):
        # 次の行または文字がまだ表示されていない場合は、一定の速度で表示
        if current_char_index < len(novel_pages[current_page_index][current_line_index]):
            current_char_index += 1
        else:
            waiting_for_click = True

    clock.tick(30)  # フレームレートを30に設定

    # ページ遷移時にクリア
    if current_line_index == 0 and current_char_index == 0 and waiting_for_click and current_page_index > 0:
        pygame.time.wait(500)  # 500ミリ秒待機（クリア後の表示を少し待つ）

        # 新しいページの先頭から描画を始める
        current_line_index = 0
        current_char_index = 0
        waiting_for_click = False

        # すべてのテキストが表示された場合、次のページに進む
        if current_page_index >= len(novel_pages):
            pygame.quit()
            sys.exit()
