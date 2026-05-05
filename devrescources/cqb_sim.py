import pygame
import math
import random
import ast
import sys
import os
from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
import pygame.gfxdraw

# ---------------- CONFIG ----------------
TILE = 32
MAX_MAP_SIZE = 100
FOV_ANGLE = math.radians(130)
MAX_VIEW_DIST = 12 * TILE
steps = 180

# ---------------- PATH ----------------
def resource_path(p):
    try:
        base = sys._MEIPASS
    except:
        base = os.path.abspath(".")
    return os.path.join(base, p)

sound_icon_path = resource_path("sound_icon.png")

# ---------------- MAP ----------------
def load_map():
    root = tk.Tk()
    root.withdraw()
    f = filedialog.askopenfilename(filetypes=[("*.thmap","*.thmap")])
    if not f:
        exit()
    with open(f,"r") as file:
        return ast.literal_eval(file.read())

GAME_MAP = load_map()
H = len(GAME_MAP)
W = len(GAME_MAP[0])

WIDTH = W * TILE
HEIGHT = H * TILE

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

sound_icon = pygame.image.load(sound_icon_path).convert_alpha()
sound_icon = pygame.transform.scale(sound_icon,(14,22))

font = pygame.font.SysFont(None, 48)
small = pygame.font.SysFont(None, 26)

# ---------------- STATE ----------------
STATE = "LOADING"
load_t = 0

# ---------------- SHARED COLLISION ----------------
def is_blocking(x, y):
    gx, gy = int(x // TILE), int(y // TILE)

    if 0 <= gx < W and 0 <= gy < H:
        t = GAME_MAP[gy][gx]

        if t == 1:
            return True

        if t in [3,4]:
            lx = x - gx*TILE
            ly = y - gy*TILE

            if t == 3 and abs(lx - TILE/2) < 2:
                return True
            if t == 4 and abs(ly - TILE/2) < 2:
                return True

    return False

# ---------------- ENTITIES ----------------
class Player:
    def __init__(self):
        self.x = 2*TILE
        self.y = 2*TILE
        self.angle = 0
        self.rect = pygame.Rect(0,0,18,28)
        self.cooldown = 0
        self.lives = 3
        self.inv = 0

    def r(self):
        r=self.rect.copy()
        r.center=(self.x,self.y)
        return r

player = Player()

class Enemy:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.cooldown=0
        self.alert=0
        self.max_alert=0.7

    def sees(self,p):
        dx,dy=p.x-self.x,p.y-self.y
        dist=math.hypot(dx,dy)

        if dist>MAX_VIEW_DIST:
            return False

        for i in range(int(dist/2)):
            x=self.x+dx*i/(dist/2)
            y=self.y+dy*i/(dist/2)

            if is_blocking(x,y):
                return False

        return True

    def update(self,p,dt):
        self.alert += dt if self.sees(p) else -dt*0.7
        self.alert = max(0,min(self.alert,self.max_alert))
        if random.random() < 0.001:
            pings.append(Ping(self.x, self.y))

        self.cooldown -= dt

        if self.alert>=self.max_alert and self.cooldown<=0:
            bullets.append([self.x,self.y,math.atan2(p.y-self.y,p.x-self.x),1])
            self.cooldown=1.4
class Ping:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 2.0

    def update(self, dt):
        self.timer -= dt

    def alive(self):
        return self.timer > 0

    def draw(self, screen):
        screen.blit(sound_icon, (self.x - 7, self.y - 11))
enemies=[]
for y,row in enumerate(GAME_MAP):
    for x,t in enumerate(row):
        if t==2:
            enemies.append(Enemy(x*TILE+TILE//2,y*TILE+TILE//2))

# ---------------- WORLD ----------------
bullets=[]
pings=[]

def walkable(x,y):
    gx,gy=int(x//TILE),int(y//TILE)
    return 0<=gx<W and 0<=gy<H and GAME_MAP[gy][gx] in [0,2]

def make_walls():
    r=[]
    for y,row in enumerate(GAME_MAP):
        for x,t in enumerate(row):
            if t==1:
                r.append(pygame.Rect(x*TILE,y*TILE,TILE,TILE))
    return r

walls=make_walls()

# ---------------- FOV ----------------
def fov():
    ox,oy=player.x,player.y
    pts=[(ox,oy)]

    for i in range(steps):
        a=player.angle-FOV_ANGLE/2+FOV_ANGLE*i/steps
        x,y=ox,oy

        for _ in range(MAX_VIEW_DIST):
            if is_blocking(x,y):
                break
            x+=math.cos(a)
            y+=math.sin(a)

        pts.append((x,y))

    surf=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
    pygame.gfxdraw.filled_polygon(surf,[(int(p[0]),int(p[1])) for p in pts],(255,255,255,255))
    return surf

# ---------------- LOOP ----------------
running=True

while running:
    dt=clock.tick(60)/1000

    # EVENTS
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False

        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_e:
                px,py=int(player.x//TILE),int(player.y//TILE)

                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=px+dx,py+dy

                    if 0<=nx<W and 0<=ny<H:
                        if GAME_MAP[ny][nx] in [3,4]:
                            GAME_MAP[ny][nx]=0
                            walls=make_walls()

    # LOADING
    if STATE=="LOADING":
        load_t+=dt
        screen.fill((10,10,15))

        t=font.render("TACTICAL SIM",1,(200,200,255))
        screen.blit(t,(WIDTH//2-t.get_width()//2,HEIGHT//3))

        pygame.draw.rect(screen,(40,40,50),(WIDTH*0.2,HEIGHT//2,WIDTH*0.6,20))
        pygame.draw.rect(screen,(80,200,120),(WIDTH*0.2,HEIGHT//2,WIDTH*0.6*(load_t/2),20))

        pygame.display.flip()

        if load_t>=2:
            STATE="PLAY"
        continue

    # PLAYER
    mx,my=pygame.mouse.get_pos()
    player.angle=math.atan2(my-player.y,mx-player.x)

    keys=pygame.key.get_pressed()
    sp=140*dt
    dx=dy=0

    if keys[pygame.K_w]:dy-=sp
    if keys[pygame.K_s]:dy+=sp
    if keys[pygame.K_a]:dx-=sp
    if keys[pygame.K_d]:dx+=sp

    if walkable(player.x+dx,player.y):player.x+=dx
    if walkable(player.x,player.y+dy):player.y+=dy

    # SHOOT
    if pygame.mouse.get_pressed()[0] and player.cooldown<=0:
        bullets.append([player.x,player.y,player.angle,0])
        player.cooldown=0.2

    player.cooldown=max(0,player.cooldown-dt)

    # ENEMIES
    for e in enemies:
        e.update(player,dt)

    # BULLETS
    for b in bullets[:]:
        b[0]+=math.cos(b[2])*400*dt
        b[1]+=math.sin(b[2])*400*dt

        if is_blocking(b[0],b[1]):
            bullets.remove(b)
            continue

        r=pygame.Rect(b[0],b[1],4,4)

        if b[3]==0:
            for e in enemies:
                if r.colliderect(e.x-8,e.y-8,16,16):
                    enemies.remove(e)
                    bullets.remove(b)
                    break

        else:
            if r.colliderect(player.r()):
                bullets.remove(b)
                if player.inv<=0:
                    player.lives -= 1
                    player.lives = max(0, player.lives)
                    player.inv=1.2
                    if player.lives<=0:
                        STATE="LOSE"
                        root.destroy()
                        running = False


   

    if not enemies:
        STATE = "WIN"

        root = tk.Tk()
        root.withdraw()

        messagebox.showinfo("Result", "YOU WIN")

        root.destroy()
        running = False

    player.inv=max(0,player.inv-dt)

    # DRAW
    screen.fill((10,10,10))

    for y,row in enumerate(GAME_MAP):
        for x,t in enumerate(row):
            cx,cy=x*TILE,y*TILE

            if t in [0,2]:
                col=(139,90,43)
            elif t==1:
                col=(60,60,60)
            elif t in [3,4]:
                col=(170,170,170)
            else:
                col=(50,50,50)

            pygame.draw.rect(screen,col,(cx,cy,TILE,TILE))

            # thin door line
            if t==3:
                pygame.draw.line(screen,(200,200,200),(cx+TILE//2,cy+4),(cx+TILE//2,cy+TILE-4),3)
            if t==4:
                pygame.draw.line(screen,(200,200,200),(cx+4,cy+TILE//2),(cx+TILE-4,cy+TILE//2),3)

    for e in enemies:
        pygame.draw.rect(screen,(255,60,60),(e.x-8,e.y-8,16,16))

    for b in bullets:
        pygame.draw.circle(screen,(255,255,0),(int(b[0]),int(b[1])),3)

    pygame.draw.rect(screen,(0,255,0),player.r())

    screen.blit(fov(),(0,0),special_flags=pygame.BLEND_MULT)

    screen.blit(small.render(f"Lives: {player.lives}",1,(255,255,255)),(10,10))


    for p in pings[:]:
        p.update(dt)
        if not p.alive():
            pings.remove(p)
        else:
            p.draw(screen)

    pygame.display.flip()

root.destroy()
running = False