import os
import sys
import pygame as pg
import random

WIDTH, HEIGHT = 1600, 900
os.chdir(os.path.dirname(os.path.abspath(__file__)))

 #移動量辞書の定義
DELTA={
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}

def check_bound(rct: pg.Rect)-> tuple[bool,bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue，画面外ならFalse
    
    """
    yoko,tate=True,True
    if rct.left < 0 or WIDTH < rct.right:#横方向指定
        yoko=False
    if rct.top < 0 or HEIGHT < rct.bottom:#縦方向指定
        tate=False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    clock = pg.time.Clock()

    bomb= pg.Surface((20,20))
    pg.draw.circle(bomb, (255,0,0),(10,10),10)
    bomb.set_colorkey((0, 0, 0))
    x_bomb = random.randint(0,WIDTH)
    y_bomb = random.randint(0,HEIGHT)
    bomb_rct= bomb.get_rect()
    bomb_rct.center= x_bomb, y_bomb
    vx , vy= +5,+5

    tmr = 0



    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        screen.blit(bomb, bomb_rct)
        bomb_rct.move_ip(vx,vy)
        

        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
       
        """
        if key_lst[pg.K_UP]:
            sum_mv[1] -= 5
        if key_lst[pg.K_DOWN]:
            sum_mv[1] += 5
        if key_lst[pg.K_LEFT]:
            sum_mv[0] -= 5
        if key_lst[pg.K_RIGHT]:
            sum_mv[0] += 5
        """
        kk_rct.move_ip(sum_mv)
        screen.blit(kk_img, kk_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

        
       
        
      




if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
