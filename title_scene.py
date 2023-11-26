import pygame
import os



#初期化関数
color = 255,255,255
#モデル
class GameStateSet:
    MENU = "menu"
    START = "start"
    CONTINUE = "continue"

#画像ファイルパスを読み込む
def load_image(file_path):
    if os.path.exists(file_path):
        return pygame.image.load(file_path)
    else:
        raise FileNotFoundError(f"File not found: {file_path}")
    
#SEファイルパスを読み込む
def load_sound(file_path):
    if os.path.exists(file_path):
        return pygame.mixer.Sound(file_path)
    else:
        raise FileNotFoundError(f"File not found: {file_path}")
    
#音楽ファイルパスを読み込む 
def load_music(file_path):
    if os.path.exists(file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(-1)
    else:
        raise FileNotFoundError(f"File not found: {file_path}")
    

# テキストを描画する関数
def draw_text(screen,text,font,color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


# ボタンのクラス
class Button:
    #ボタンは、矩形属性(x,y,w,h)、テキスト、ホバーしているか、ホバー前からの真偽値を持つ
    def __init__(self,screen,text,font, x, y, width, height):
        self._rect = pygame.Rect(x, y, width, height)
        self._text = text
        self._hovered = False
        self._prev_hovered = False
        self.font = font
        self.screen = screen
    #ボタンは上記の要素に加えて、色と、ホバー時のサウンドを使って描画される   
    def draw(self,color, hover_sound=None):
        #テキストを描画する、色と、縦横の中心の位置を使って
        draw_text(self.screen,self._text, self.font,color,self._rect.centerx, self._rect.centery)
        #ボタンがサウンドを持っていて、ホバーしていて、ホバー前でないならば音を鳴らす
        if hover_sound is not None and self._hovered and not self._prev_hovered:
            hover_sound.play()
    #プロパティ。ホバー以前にホバー状態の値を入れてから、ホバー状態かどうかを新たにセットする。
    def set_hovered(self, value):
        self._prev_hovered = self._hovered
        self._hovered = value
    #プロパティ。矩形情報をセットする
    #none からtrueが入ったらロジックエラーにならない？
    @property
    def rect(self):
        return self._rect
    #プロパティ。ホバー
    @property
    def hovered(self):
        return self._hovered










