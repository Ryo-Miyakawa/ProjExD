import random
import sys
import os

import pygame as pg

MAX_SHOTS = 2

main_dir = os.path.split(os.path.abspath(__file__))[0]


class Screen:
    def __init__(self, title, wh, img_path):
        #練習1
        pg.display.set_caption(title)#逃げろ！こうかとん
        self.sfc = pg.display.set_mode(wh)#1600,900
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(img_path)
        self.bgi_rct = self.bgi_sfc.get_rect()
    
    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)


class Bird:
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }

    def __init__(self,img_path,ratio,xy):
        self.sfc = pg.image.load(img_path)#"fig/6.png"
        self.sfc = pg.transform.rotozoom(self.sfc, 0, ratio)#2.0)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy#900, 400
        self.reloading = 0

    def blit(self,scr:Screen):
        scr.sfc.blit(self.sfc,self.rct)
    
    def update(self, scr:Screen):
        key_dct = pg.key.get_pressed()
        wall_sound = load_sound("car_door.wav")
        for key, delta in Bird.key_delta.items():
            if key_dct[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]
            if check_bound(self.rct, scr.rct) != (+1, +1):
                self.rct.centerx -= delta[0]
                self.rct.centery -= delta[1]
                if pg.mixer:
                    wall_sound.play()#追加１：壁にぶつかると衝突音が鳴る
        self.blit(scr)
    
    def gunpos(self):
        pos = self.facing * self.gun_offset + self.rect.centerx
        return pos, self.rect.top


class Bomb:
    def __init__(self,color,rad,vxy,scr:Screen):
        self.sfc = pg.Surface((2*rad, 2*rad)) # 正方形の空のSurface
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy
    
    def blit(self,scr:Screen):
        scr.sfc.blit(self.sfc,self.rct)

    def update(self,scr:Screen):
        self.rct.move_ip(self.vx, self.vy) 
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)

        
class Enemy:#追加3：チキンにぶつかると自機が大きくなる機能を追加
    def __init__(self,img_path,ratio,vxy,scr:Screen):
        self.sfc = pg.image.load(img_path)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, ratio)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy

    def blit(self,scr:Screen):
        scr.sfc.blit(self.sfc,self.rct)

    def update(self,scr:Screen):
        self.rct.move_ip(self.vx, self.vy) 
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)


class Help:#追加4：小さいこうかとんに接触すると自機が小さくなる機能を追加
    def __init__(self,img_path,ratio,vxy,scr:Screen):
        self.sfc = pg.image.load(img_path)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, ratio)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy

    def blit(self,scr:Screen):
        scr.sfc.blit(self.sfc,self.rct)

    def update(self,scr:Screen):
        self.rct.move_ip(self.vx, self.vy) 
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)
    

def check_bound(obj_rct, scr_rct):
    """
    第1引数：こうかとんrectまたは爆弾rect
    第2引数：スクリーンrect
    範囲内：+1／範囲外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate

class Shot:
    def __init__(self, xy ):
        self.sfc = pg.image.load("ex05/data/shot.gif")
        self.rxt = self.sfc.get_rect()
        self.rct = self.sfc.get_rect()
        self.vx, self.vy = 0,-3
        self.rct.center = xy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.rct.move_ip(self.vx, self.vy)
        self.blit(scr)


def load_sound(file):
    """because pygame can be be compiled without mixer."""
    if not pg.mixer:
        return None
    file = os.path.join(main_dir, "data", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print("Warning, unable to load, %s" % file)
    return None


def main():
    clock =pg.time.Clock()
    # 練習１
    scr = Screen("逃げろ！こうかとん",(1600, 900), "fig/pg_bg.jpg")

    # 練習３
    kkt = Bird("fig/6.png",2.0,(900,400))
    kkt.update(scr)

    if pg.mixer:
        music = os.path.join(main_dir, "data", "house_lo.wav")#追加2：BGMを導入
        pg.mixer.music.load(music)
        pg.mixer.music.play(-1)


    # 練習５
    bkd_lst = []
    for _ in range(5):
        bkd = Bomb((255,0,0), 10, (+1, +1), scr)
        bkd_lst.append(bkd)
    #bkd.update(scr)

    ekt = Enemy("fig/kfc.png",0.1,(+1,+1),scr)
    ekt.update(scr)

    hit = Help("fig/0.png",1.0,(+1,+1),scr)
    hit.update(scr)

    shots = 0

    # 練習２
    while True:
        scr.blit()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            
        kkt.update(scr)
        ekt.update(scr)
        hit.update(scr)

        if kkt.rct.colliderect(hit.rct):
            kkt = Bird("fig/6.png",0.5,(900,400))
        if kkt.rct.colliderect(ekt.rct):
            kkt = Bird("fig/6.png",4.0,(900,400))
        for i in range(5):
            bkd_lst[i].update(scr)
            if kkt.rct.colliderect(bkd_lst[i].rct):
                return
        
        key_dct = pg.key.get_pressed()
        if key_dct[pg.K_SPACE]:
            shots = Shot(kkt.rct.center)
        if shots:
            shots.update(scr)

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
