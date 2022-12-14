import pygame as pg
import sys
import random

def check_bound(obj_rct,scr_rct):
    #第1引数：こうかとんrectまたは
    #範囲内：＋1/範囲外：－1

    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1

    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate

def main():
    clock = pg.time.Clock()
    #練習1
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((1600, 900))
    scrn_rct = scrn_sfc.get_rect()

    pgbg_sfc = pg.image.load("fig/pg_bg.jpg")
    pgbg_rct = pgbg_sfc.get_rect()

    #練習3
    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 900, 400
    scrn_sfc.blit(tori_sfc, tori_rct)

    #練習5
    bomb_sfc = pg.Surface((20,20))#正方形の空のSurface
    bomb_sfc.set_colorkey((0,0,0))
    pg.draw.circle(bomb_sfc,(255,0,0),(10,10),10)
    bomb_rct = bomb_sfc.get_rect()
    bomb_rct.centerx = random.randint(0,scrn_rct.width)
    bomb_rct.centery = random.randint(0,scrn_rct.height)
    scrn_sfc.blit(bomb_sfc,bomb_rct)


    help_sfc = pg.Surface((20,20))#正方形の空のSurface
    help_sfc.set_colorkey((0,0,0))
    pg.draw.circle(help_sfc,(0,255,0),(10,10),10)
    help_rct = help_sfc.get_rect()
    help_rct.centerx = random.randint(0,scrn_rct.width)
    help_rct.centery = random.randint(0,scrn_rct.height)
    scrn_sfc.blit(help_sfc,help_rct)

    vx, vy = +1, +1
    #練習2
    while True:
        scrn_sfc.blit(pgbg_sfc,pgbg_rct)
        for event in pg.event.get():
            if event.type ==pg.QUIT:
                return
        #練習4
        key_dct = pg.key.get_pressed() #辞書型
        if key_dct[pg.K_UP]:
            tori_rct.centery -= 1
        if key_dct[pg.K_DOWN]:
            tori_rct.centery += 1
        if key_dct[pg.K_LEFT]:
            tori_rct.centerx -= 1
        if key_dct[pg.K_RIGHT]:
            tori_rct.centerx += 1
        if key_dct[pg.K_ESCAPE]:
            vx,vy = 0,0 #追加機能２:エスケープを押すと弾が停止
        if key_dct[pg.K_1]:
            vx, vy = +1,+1 #追加機能３：１を押すと弾が方向を変える
            
        if check_bound(tori_rct,scrn_rct) != (+1,+1):
            if key_dct[pg.K_UP]:
                tori_rct.centery += 1
            if key_dct[pg.K_DOWN]:
                tori_rct.centery -= 1
            if key_dct[pg.K_LEFT]:
                tori_rct.centerx += 1
            if key_dct[pg.K_RIGHT]:
                tori_rct.centerx -= 1      

        scrn_sfc.blit(tori_sfc, tori_rct)
        
        #練習6
        if key_dct[pg.K_2]:#追加機能4：弾を大きくする
            byoko = bomb_rct.centerx
            btate = bomb_rct.centery
            bomb_sfc = pg.Surface((100,100))
            bomb_sfc.set_colorkey((0,0,0))
            pg.draw.circle(bomb_sfc,(255,0,0),(50,50),50)
            bomb_rct = bomb_sfc.get_rect()
            bomb_rct.centerx = byoko
            bomb_rct.centery = btate
            scrn_sfc.blit(bomb_sfc,bomb_rct)
        bomb_rct.move_ip(vx, vy)
        help_rct.move_ip(vx,vy)
        scrn_sfc.blit(bomb_sfc,bomb_rct)
        scrn_sfc.blit(help_sfc,help_rct)
        yoko,tate = check_bound(bomb_rct,scrn_rct)
        hyoko,htate = check_bound(help_rct,scrn_rct)
        vx *= yoko
        vy *= tate
        vx *= hyoko
        vy *= htate
        
        #練習8
        if tori_rct.colliderect(bomb_rct):
            reyoko = tori_rct.centerx
            retate = tori_rct.centery
            tori_sfc = pg.image.load("fig/kfc.png")
            tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 0.5)
            tori_rct = tori_sfc.get_rect()
            tori_rct.center = (reyoko,retate)
            scrn_sfc.blit(tori_sfc, tori_rct)#追加機能１：爆弾がこうかとんに当たると画像変更

        if tori_rct.colliderect(help_rct):
            hyoko = tori_rct.centerx
            htate = tori_rct.centery
            tori_sfc = pg.image.load("fig/9.png")#追加5緑の弾に当たるとこうかとんが小さくなる
            tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 0.5)
            tori_rct = tori_sfc.get_rect()
            tori_rct.center = (hyoko,htate)
            scrn_sfc.blit(tori_sfc, tori_rct)
     
        pg.display.update()
        clock.tick(1000)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()