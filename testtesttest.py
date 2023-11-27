import sys
import pygame

def main():
    pygame.init()
    # メイン画面（Surface）初期化(横, 縦)
    main_surface = pygame.display.set_mode((300, 300)) 
    # メイン画面のタイトル
    pygame.display.set_caption("Pygame Sample")

    # フォントオブジェクト生成（引数：フォント名とフォントサイズ）
    # フォント名にNoneを指定するとPygameの既定のフォントになる
    font = pygame.font.Font(None, 30)
    # テキストのSurfaceオブジェクトの生成（引数：テキスト内容、antialias、文字の色RGB）
    text_surface = font.render("Hello World", True, (0, 0, 255))
    #メイン画面の色設定（引数：RGB）
    main_surface.fill((220, 220, 220))
    # メイン画面上にテキストを配置（引数：配置するSurface、座標）
    main_surface.blit(text_surface, (100, 100)) 

    # メイン画面の更新
    pygame.display.update()
    
    # Clockオブジェクトの生成
    clock = pygame.time.Clock()
    # ループを続けるかのフラグ
    going = True
    # 終了イベント発生までループをまわす
    while going:
        # イベントを取得
        for event in pygame.event.get():
            # 終了イベント（画面の×ボタン押下など）の場合、
            # ループを抜ける
            if event.type == pygame.QUIT:
                going = False
 
        # フレームレート（1秒間に何回画面を更新するか）の設定
        clock.tick(10)
    # 終了処理
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main()