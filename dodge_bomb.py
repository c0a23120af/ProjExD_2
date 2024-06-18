import os
import sys
import pygame as pg
import random

WIDTH, HEIGHT = 1600, 900

DELTA={    #移動量辞書の定義
    pg.K_UP: (0, -5),
    pg.K_RIGHT: (+5, 0),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5,0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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


def kk_direction() -> dict:#こうかとんの向きを変える関数
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_img2 = pg.transform.flip(kk_img,True,False)
    return {  #こうかとんの画像の向きの方向辞書
    (0, 0):kk_img,#何もキーを押していないとき
    (+5,0):kk_img2,#右キーを押したとき
    (+5,-5):pg.transform.rotozoom(kk_img2,45,1.0),#右キーと上キーを押したとき
    (0,-5):pg.transform.rotozoom(kk_img2,90,1.0),#上キーを押したとき
    (+5,+5):pg.transform.rotozoom(kk_img2,-45,1.0),#右キーと下キーを押したとき
    (0,+5):pg.transform.rotozoom(kk_img2,-45,1.0),#下キーを押したとき
    (-5,+5):pg.transform.rotozoom(kk_img,45,1.0),#下キーと左キーを押したとき
    (-5,0):pg.transform.rotozoom(kk_img,0,1.0),#左キーを押したとき
    (-5,-5):pg.transform.rotozoom(kk_img,-45,1.0)#左キーと上キーを押したとき
    }

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_imgs=kk_direction()
    kk_img=kk_imgs[(0,0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    clock = pg.time.Clock()
    bomb= pg.Surface((20,20))# 1辺が20の空のSurfaceを作る
    pg.draw.circle(bomb, (255,0,0),(10,10),10)# 空のSurfaceに赤い円を描く
    bomb.set_colorkey((0, 0, 0))
    x_bomb = random.randint(0,WIDTH)
    y_bomb = random.randint(0,HEIGHT)
    bomb_rct= bomb.get_rect()# 爆弾Rect
    bomb_rct.center= x_bomb, y_bomb
    vx , vy= +5,+5 #爆弾の横方向速度，縦方向速度
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
          
        if kk_rct.colliderect(bomb_rct):#衝突判定
            return  #ゲームオーバー  
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():#こうかとんが動く方向
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        kk_img=kk_imgs[tuple(sum_mv)]

        if check_bound(kk_rct)!=(True,True):#こうかとんと爆弾の跳ね返り
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)    
        bomb_rct.move_ip(vx,vy)
        yoko,tate=check_bound(bomb_rct)
        if not tate:#縦方向にはみ出たら
            vy *= -1
        if not yoko:#横方向にはみ出たら
            vx *= -1 
        screen.blit(bomb, bomb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
