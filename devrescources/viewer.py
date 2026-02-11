import tkinter as tk
from tkinter import filedialog
import ast  # safer than eval for literal Python structures

TILE_SIZE = 30  # pixels per tile

COLOR_MAP = {
    0: "saddlebrown",  # floor
    1: "black",        # wall
    2: "red",          # enemy
}

def load_thmap(filename):
    """Load a .thmap file that contains a Python-style 2D array."""
    with open(filename, "r") as f:
        content = f.read()
    # Convert string into Python list safely
    game_map = ast.literal_eval(content)
    
    # Find the spawn position (first 0 in upper-left area)
    spawn_pos = None
    for r, row in enumerate(game_map):
        for c, tile in enumerate(row):
            if tile == 0:
                spawn_pos = (r, c)
                break
        if spawn_pos:
            break
    return game_map, spawn_pos

def draw_map(game_map, spawn_pos):
    rows = len(game_map)
    cols = len(game_map[0])
    
    root = tk.Tk()
    root.title("Tactical Hotel Map Viewer")
    
    canvas = tk.Canvas(root, width=cols*TILE_SIZE, height=rows*TILE_SIZE)
    canvas.pack()
    
    for r, row in enumerate(game_map):
        for c, tile in enumerate(row):
            x1 = c * TILE_SIZE
            y1 = r * TILE_SIZE
            x2 = x1 + TILE_SIZE
            y2 = y1 + TILE_SIZE
            
            # Spawn is green
            if spawn_pos == (r, c):
                color = "green"
            else:
                color = COLOR_MAP.get(tile, "saddlebrown")
            
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
    
    root.mainloop()

# File picker
filename = filedialog.askopenfilename(title="Select .thmap file", filetypes=[("Tactical Hotel Map", "*.thmap")])
if filename:
    game_map, spawn_pos = load_thmap(filename)
    draw_map(game_map, spawn_pos)
