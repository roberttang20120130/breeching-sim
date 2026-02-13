# Top-down CQB Simulator (45° FOV, visible bullets, smooth FOV without stripes, brown floor, enemies pathfinding and firing)
# Requires: pygame (pip install pygame)

import pygame
import math
import random
import heapq
import ast
from tkinter import filedialog
import tkinter as tk

TILE = 32
MAX_MAP_SIZE = 100
FOV_ANGLE = math.radians(130)
MAX_VIEW_DIST = 12 * TILE

def load_thmap_file():
    """Open a file dialog to pick a .thmap file and parse it safely"""
    root = tk.Tk()
    root.withdraw()  # hide the root window
    filename = filedialog.askopenfilename(
        title="Select .thmap file",
        filetypes=[("Tactical Hotel Map", "*.thmap")]
    )
    if not filename:
        print("No file selected, exiting.")
        exit()
    with open(filename, "r") as f:
        content = f.read()
    game_map = ast.literal_eval(content)
    if len(game_map) > MAX_MAP_SIZE or any(len(row) > MAX_MAP_SIZE for row in game_map):
        print(f"Map too large! Maximum is {MAX_MAP_SIZE}x{MAX_MAP_SIZE}")
        exit()
    return game_map

GAME_MAP = load_thmap_file()
MAP_SIZE_Y = len(GAME_MAP)
MAP_SIZE_X = len(GAME_MAP[0])
WIDTH = MAP_SIZE_X * TILE
HEIGHT = MAP_SIZE_Y * TILE

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Actor:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.angle = 0
        self.color = color
        self.hitbox = pygame.Rect(0, 0, 18, 28)
        self.cooldown = 0
    def rect(self):
        r = self.hitbox.copy()
        r.center = (self.x, self.y)
        return r

player = Actor(2*TILE, 2*TILE, (0,255,0))
enemies = []
for y,row in enumerate(GAME_MAP):
    for x,t in enumerate(row):
        if t == 2:
            enemies.append(Actor(x*TILE+TILE//2, y*TILE+TILE//2, (255,0,0)))

bullets = []

def walkable(x,y):
    gx = int(x//TILE)
    gy = int(y//TILE)
    return 0 <= gx < MAP_SIZE_X and 0 <= gy < MAP_SIZE_Y and GAME_MAP[gy][gx] != 1

def astar(start, goal):
    sx,sy = start
    gx,gy = goal
    open_list = [(0,(sx,sy))]
    came = {}
    g_score = { (sx,sy):0 }
    while open_list:
        _, cur = heapq.heappop(open_list)
        if cur == (gx,gy):
            break
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx,ny = cur[0]+dx, cur[1]+dy
            if 0 <= nx < MAP_SIZE_X and 0 <= ny < MAP_SIZE_Y and GAME_MAP[ny][nx] != 1:
                ng = g_score[cur] + 1
                if (nx,ny) not in g_score or ng < g_score[(nx,ny)]:
                    g_score[(nx,ny)] = ng
                    f = ng + abs(nx-gx) + abs(ny-gy)
                    heapq.heappush(open_list, (f,(nx,ny)))
                    came[(nx,ny)] = cur
    path = []
    cur = (gx,gy)
    while cur in came:
        path.append(cur)
        cur = came[cur]
    return path[::-1]

# Smooth FOV using polygon raycasting
def cast_fov(surface, origin, angle):
    ox, oy = origin
    fov_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    points = [(ox, oy)]
    steps = 200
    for i in range(steps+1):
        a = angle - FOV_ANGLE/2 + FOV_ANGLE*i/steps
        for d in range(0, MAX_VIEW_DIST, 2):
            x = ox + math.cos(a)*d
            y = oy + math.sin(a)*d
            gx = int(x//TILE)
            gy = int(y//TILE)
            if not (0 <= gx < MAP_SIZE_X and 0 <= gy < MAP_SIZE_Y):
                break
            if GAME_MAP[gy][gx] == 1:
                points.append((x,y))
                break
        else:
            points.append((x,y))
    pygame.draw.polygon(fov_surf, (255,255,255,255), points)
    surface.blit(fov_surf, (0,0))

running = True
while running:
    dt = clock.tick(60)/1000
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    mx, my = pygame.mouse.get_pos()
    player.angle = math.atan2(my-player.y, mx-player.x)

    keys = pygame.key.get_pressed()
    speed = 140*dt
    move_x = move_y = 0
    if keys[pygame.K_w]: move_y -= speed
    if keys[pygame.K_s]: move_y += speed
    if keys[pygame.K_a]: move_x -= speed
    if keys[pygame.K_d]: move_x += speed
    if walkable(player.x+move_x, player.y): player.x += move_x
    if walkable(player.x, player.y+move_y): player.y += move_y

    if pygame.mouse.get_pressed()[0] and player.cooldown <= 0:
        spread = random.uniform(-0.08,0.08)
        bullets.append([player.x, player.y, player.angle+spread, 0])
        player.cooldown = 0.2
    player.cooldown = max(0, player.cooldown - dt)

    for en in enemies:
        gx = int(en.x//TILE)
        gy = int(en.y//TILE)
        px = int(player.x//TILE)
        py = int(player.y//TILE)
        path = astar((gx,gy), (px,py))
        if path:
            tx,ty = path[0]
            vx = tx*TILE+TILE/2 - en.x
            vy = ty*TILE+TILE/2 - en.y
            dist = math.hypot(vx,vy)
            if dist > 2: en.x += vx/dist*60*dt; en.y += vy/dist*60*dt
        en.angle = math.atan2(player.y-en.y, player.x-en.x)
        if en.cooldown <= 0 and random.random() < 0.02:
            spread = random.uniform(-0.4,0.4)
            bullets.append([en.x, en.y, en.angle+spread, 1])
            en.cooldown = 1.2
        en.cooldown = max(0, en.cooldown-dt)

    for b in bullets[:]:
        b[0] += math.cos(b[2])*400*dt
        b[1] += math.sin(b[2])*400*dt
        if not walkable(b[0],b[1]): bullets.remove(b); continue
        rect = pygame.Rect(b[0]-2, b[1]-2, 4, 4)
        if b[3]==0:
            for en in enemies:
                if rect.colliderect(en.rect()):
                    enemies.remove(en); bullets.remove(b); break
        else:
            if rect.colliderect(player.rect()):
                bullets.remove(b)

    screen.fill((10,10,10))

    # draw floor and walls
    for y,row in enumerate(GAME_MAP):
        for x,t in enumerate(row):
            if t==0:
                pygame.draw.rect(screen,(139,69,19),(x*TILE,y*TILE,TILE,TILE))
            elif t==1:
                pygame.draw.rect(screen,(35,35,35),(x*TILE,y*TILE,TILE,TILE),1)

    vis = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    cast_fov(vis,(player.x,player.y),player.angle)

    for en in enemies: pygame.draw.rect(screen,(255,60,60),en.rect())
    for b in bullets: pygame.draw.circle(screen,(255,255,0),(int(b[0]),int(b[1])),3)

    pygame.draw.rect(screen, player.color, player.rect())
    screen.blit(vis,(0,0), special_flags=pygame.BLEND_MULT)
    pygame.display.flip()

pygame.quit()
