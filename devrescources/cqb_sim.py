import pygame
import math
import random
import ast
import sys
import os
from tkinter import filedialog
import tkinter as tk
import pygame.gfxdraw

# --- Config ---
TILE = 32
MAX_MAP_SIZE = 100
FOV_ANGLE = math.radians(130)
MAX_VIEW_DIST = 12 * TILE
PING_DURATION = 2
DOOR_THICKNESS = 4
steps = 180  # higher if CPU/GPU is strong

# --- Paths ---
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    try:
        # PyInstaller stores temp files here
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

sound_icon_path = resource_path("sound_icon.png")

# --- Load map ---
def load_thmap_file():
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename(
        title="Select .thmap file",
        filetypes=[("Tactical Hotel Map","*.thmap")]
    )
    if not filename: exit("No file selected")
    with open(filename,"r") as f: 
        game_map = ast.literal_eval(f.read())
    if len(game_map) > MAX_MAP_SIZE or any(len(row) > MAX_MAP_SIZE for row in game_map):
        exit(f"Map too large! Max {MAX_MAP_SIZE}x{MAX_MAP_SIZE}")
    return game_map

GAME_MAP = load_thmap_file()
MAP_SIZE_Y = len(GAME_MAP)
MAP_SIZE_X = len(GAME_MAP[0])
WIDTH = MAP_SIZE_X * TILE
HEIGHT = MAP_SIZE_Y * TILE

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- Load assets ---
sound_icon = pygame.image.load(sound_icon_path).convert_alpha()
sound_icon = pygame.transform.scale(sound_icon,(14,22))

# --- Classes ---
class Actor:
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.angle = 0
        self.color = color
        self.hitbox = pygame.Rect(0,0,18,28)
        self.cooldown = 0
    def rect(self):
        r = self.hitbox.copy()
        r.center = (self.x,self.y)
        return r

class Ping:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.timer = PING_DURATION
    def update(self,dt): self.timer -= dt
    def is_alive(self): return self.timer>0
    def draw(self,surface):
        surface.blit(sound_icon,(self.x-sound_icon.get_width()//2,self.y-sound_icon.get_height()//2))

class AIEnemy(Actor):
    def __init__(self,x,y):
        super().__init__(x,y,(255,0,0))
        self.cooldown = 0
        self.sound_cooldown = random.uniform(1.5,4.0)
    def can_see_player(self,player):
        dx,dy = player.x - self.x, player.y - self.y
        dist = math.hypot(dx,dy)
        if dist > MAX_VIEW_DIST: return False
        steps = int(dist/2)
        for i in range(steps):
            px = self.x + dx*i/steps
            py = self.y + dy*i/steps
            gx,gy = int(px//TILE), int(py//TILE)
            if 0<=gx<MAP_SIZE_X and 0<=gy<MAP_SIZE_Y:
                t = GAME_MAP[gy][gx]
                if t==1: return False
                if t==3 and abs(px-(gx*TILE+TILE//2))<=DOOR_THICKNESS/2: return False
                if t==4 and abs(py-(gy*TILE+TILE//2))<=DOOR_THICKNESS/2: return False
        return True
    def update(self,player,dt):
        self.angle = math.atan2(player.y-self.y, player.x-self.x)
        if self.can_see_player(player) and self.cooldown<=0:
            spread = random.uniform(-0.2,0.2)
            bullets.append([self.x,self.y,self.angle+spread,1])
            self.cooldown = 1.2
        self.cooldown = max(0,self.cooldown-dt)
        self.sound_cooldown -= dt
        if self.sound_cooldown<=0:
            pings.append(Ping(self.x,self.y))
            self.sound_cooldown=random.uniform(1.5,4.0)

# --- Actors ---
player = Actor(2*TILE,2*TILE,(0,255,0))
enemies = []
bullets = []
pings = []

for y,row in enumerate(GAME_MAP):
    for x,t in enumerate(row):
        if t==2: enemies.append(AIEnemy(x*TILE+TILE//2,y*TILE+TILE//2))

# --- Utils ---
def walkable(x,y):
    gx,gy = int(x//TILE), int(y//TILE)
    return 0<=gx<MAP_SIZE_X and 0<=gy<MAP_SIZE_Y and GAME_MAP[gy][gx] in [0,2]

def make_wall_rects():
    rects=[]
    for y,row in enumerate(GAME_MAP):
        for x,t in enumerate(row):
            cx,cy = x*TILE, y*TILE
            if t==1: rects.append(pygame.Rect(cx,cy,TILE,TILE))
            if t==3: rects.append(pygame.Rect(cx+TILE//2-DOOR_THICKNESS//2,cy,DOOR_THICKNESS,TILE))
            if t==4: rects.append(pygame.Rect(cx,cy+TILE//2-DOOR_THICKNESS//2,TILE,DOOR_THICKNESS))
    return rects

def is_blocking_fov(px,py):
    gx,gy = int(px//TILE), int(py//TILE)
    if 0<=gx<MAP_SIZE_X and 0<=gy<MAP_SIZE_Y:
        t = GAME_MAP[gy][gx]
        if t==1: return True
        if t==3 and abs(px-(gx*TILE+TILE//2))<=DOOR_THICKNESS/2: return True
        if t==4 and abs(py-(gy*TILE+TILE//2))<=DOOR_THICKNESS/2: return True
    return False

def cast_fov_pixel(origin):
    ox, oy = origin
    points = [(ox, oy)]
    for i in range(steps+1):
        angle = player.angle - FOV_ANGLE/2 + FOV_ANGLE*i/steps
        x, y = ox, oy
        for _ in range(MAX_VIEW_DIST):
            if is_blocking_fov(x, y): break
            x += math.cos(angle)
            y += math.sin(angle)
        points.append((x, y))
    fov_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.gfxdraw.filled_polygon(fov_surf, [(int(px), int(py)) for px, py in points], (255,255,255,255))
    pygame.gfxdraw.aapolygon(fov_surf, [(int(px), int(py)) for px, py in points], (255,255,255,255))
    return fov_surf

# --- Draw doors ---
def draw_doors():
    for y,row in enumerate(GAME_MAP):
        for x,t in enumerate(row):
            cx, cy = x*TILE, y*TILE
            color = (120,120,120)
            if t==3:  # vertical door
                pygame.draw.aaline(screen, color, (cx+TILE//2, cy), (cx+TILE//2, cy+TILE))
            if t==4:  # horizontal door
                pygame.draw.aaline(screen, color, (cx, cy+TILE//2), (cx+TILE, cy+TILE//2))

wall_rects = make_wall_rects()

# --- Main loop ---
running = True
while running:
    dt = clock.tick(60)/1000
    for e in pygame.event.get():
        if e.type==pygame.QUIT: running=False

    # --- Player movement ---
    mx,my = pygame.mouse.get_pos()
    player.angle = math.atan2(my-player.y, mx-player.x)
    keys = pygame.key.get_pressed()
    speed = 140*dt
    move_x=move_y=0
    if keys[pygame.K_w]: move_y-=speed
    if keys[pygame.K_s]: move_y+=speed
    if keys[pygame.K_a]: move_x-=speed
    if keys[pygame.K_d]: move_x+=speed
    if walkable(player.x+move_x,player.y): player.x+=move_x
    if walkable(player.x,player.y+move_y): player.y+=move_y

    # --- Doors ---
    if keys[pygame.K_e]:
        px_tile,py_tile=int(player.x//TILE),int(player.y//TILE)
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx,ny = px_tile+dx,py_tile+dy
            if 0<=nx<MAP_SIZE_X and 0<=ny<MAP_SIZE_Y and GAME_MAP[ny][nx] in [3,4]:
                GAME_MAP[ny][nx]=0
        wall_rects = make_wall_rects()

    # --- Shooting ---
    if pygame.mouse.get_pressed()[0] and player.cooldown<=0:
        spread = random.uniform(-0.08,0.08)
        bullets.append([player.x,player.y,player.angle+spread,0])
        player.cooldown=0.2
    player.cooldown = max(0,player.cooldown-dt)

    # --- Update enemies ---
    for en in enemies: en.update(player,dt)

    # --- Update bullets ---
    for b in bullets[:]:
        b[0]+=math.cos(b[2])*400*dt
        b[1]+=math.sin(b[2])*400*dt
        if any(rect.collidepoint(b[0],b[1]) for rect in wall_rects):
            bullets.remove(b); continue
        rect = pygame.Rect(b[0]-2,b[1]-2,4,4)
        if b[3]==0:
            for en in enemies:
                if rect.colliderect(en.rect()): enemies.remove(en); bullets.remove(b); break
        elif rect.colliderect(player.rect()): bullets.remove(b)

    # --- Draw map ---
    screen.fill((10,10,10))
    for y,row in enumerate(GAME_MAP):
        for x,t in enumerate(row):
            cx,cy = x*TILE, y*TILE
            color = (139,69,19) if t in [0,2] else (35,35,35)
            pygame.draw.rect(screen,color,(cx,cy,TILE,TILE))

    # --- Draw doors ---
    draw_doors()

    # --- Draw actors ---
    for en in enemies: pygame.draw.rect(screen,(255,60,60),en.rect())
    for b in bullets: pygame.draw.circle(screen,(255,255,0),(int(b[0]),int(b[1])),3)
    pygame.draw.rect(screen,player.color,player.rect())

    # --- Overlay FOV ---
    fov_surf = cast_fov_pixel((player.x,player.y))
    screen.blit(fov_surf,(0,0),special_flags=pygame.BLEND_MULT)

    # --- Draw pings ---
    for ping in pings[:]:
        ping.update(dt)
        if not ping.is_alive(): pings.remove(ping)
        else: ping.draw(screen)

    pygame.display.flip()

pygame.quit()
