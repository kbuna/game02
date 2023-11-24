import pygame as pg
from pygame.locals import*
import sys

tmr = 0 #タイマー
idx = 0 #インデックス


color = {"white":(255,255,255),"alice blue":(240,248,255),"bleu turquoise":(0,101,129)}#色指定

img1 = pg.image.load("character.png")

def draw_text(siz,txt,col,bg,x,y):#テキストの描画
  fnt = pg.font.Font("NotoSansJP-Regular.ttf",siz)
  sur = fnt.render(txt,True,col)
  bg.blit(sur,[x,y])

def draw_button(bg,col_r,button,w,siz,txt,col_f):#ボタンの描画
  pg.draw.rect(bg,col_r,button,width = w,border_radius=10)
  fnt = pg.font.Font("NotoSansJP-Regular.ttf",siz)
  sur = fnt.render(txt,True,col_f)
  w = button[0] + button[2]/2 - sur.get_width()/2#幅
  h = button[1] + button[3]/2 - sur.get_height()/2#高さ
  bg.blit(sur,[w,h])

def main():#main処理
  global tmr

  pg.init()
  pg.display.set_caption("nv")
  screen = pg.display.set_mode((1280,720))
  clock = pg.time.Clock()

  button = [pg.Rect(115,360,120,40),#START
            pg.Rect(175,430,120,40),#COUNTINUE
            pg.Rect(245,500,120,40)]#QUIT
  words = ["START","COUNTINUE","QUIT"]

  while True:
    tmr += 1
    for e in pg.event.get():#イベントの種類
      if e.type == QUIT:
        pg.quit()
        sys.exit()
      elif e.type == KEYDOWN:
        if e.key == K_F1:
          screen = pg.display.set_mode((1280,720),FULLSCREEN)
        if e.key == K_F2 or e.key == K_ESCAPE:
          screen = pg.display.set_mode((1280,720))

    if idx == 0:#タイトル画面
      draw_text(75,"SYATYOO",color["white"],screen,30,100)
      draw_text(75,"Come back!",color["white"],screen,30,220)
      screen.blit(img1,[550,50])
      for i in range(3):
        draw_button(screen,color["alice blue"],button[i],0,24,words[i],
                    color["bleu turquoise"])
        
    if idx == 1:#ゲーム本編
      screen.fill(color["black"])
      draw_text(75,"pushed START!",color["white"],screen,80,260)
      if tmr > 30: #タイマーが30を超えたらタイトルへ戻る
        idx = 0
        tmr = 0
        screen.fill(color["black"])
    if idx ==2: #セーブ＆ロード
      screen.fill(color["black"])
      draw_text(75,"pushed START!",color["white"],screen,80,260)
      if tmr > 30: #タイマーが30を超えたらタイトルへ戻る
        idx = 0
        tmr = 0
        screen.fill(color["black"])

    pg.display.update()
    clock.tick(15)

if __name__=="__main__":
  main()