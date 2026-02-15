import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import ast

TILE_SIZE = 24
MAX_SIZE = 100
DEFAULT_SIZE = 20

# Added door tiles 3 and 4
COLORS = {
    0: "#8b6b3f",  # floor brown
    1: "#000000",  # wall black
    2: "#ff2b2b",  # enemy red
    3: "#888888",  # door vertical (up/down)
    4: "#aaaaaa",  # door horizontal (left/right)
}

class Editor:
    def __init__(self, root):
        self.root = root
        self.root.title("THMAP Editor")

        self.map_size = DEFAULT_SIZE
        self.current_tile = 1
        self.map = [[1 for _ in range(self.map_size)] for _ in range(self.map_size)]

        self.canvas = tk.Canvas(root, width=self.map_size*TILE_SIZE, height=self.map_size*TILE_SIZE, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=6)
        self.canvas.bind("<Button-1>", self.paint)
        self.canvas.bind("<B1-Motion>", self.paint)

        # Tile selection buttons
        tk.Button(root, text="Wall", command=lambda: self.set_tile(1)).grid(row=1, column=0, sticky="ew")
        tk.Button(root, text="Floor", command=lambda: self.set_tile(0)).grid(row=1, column=1, sticky="ew")
        tk.Button(root, text="Enemy", command=lambda: self.set_tile(2)).grid(row=1, column=2, sticky="ew")
        tk.Button(root, text="Door UD", command=lambda: self.set_tile(3)).grid(row=1, column=3, sticky="ew")
        tk.Button(root, text="Door LR", command=lambda: self.set_tile(4)).grid(row=1, column=4, sticky="ew")
        tk.Button(root, text="Clear", command=self.clear).grid(row=1, column=5, sticky="ew")

        # File buttons
        tk.Button(root, text="Load", command=self.load).grid(row=2, column=0, columnspan=2, sticky="ew")
        tk.Button(root, text="Save", command=self.save).grid(row=2, column=2, columnspan=2, sticky="ew")
        tk.Button(root, text="New Map", command=self.new_map).grid(row=2, column=4, columnspan=2, sticky="ew")

        self.draw()

    def set_tile(self, tile):
        self.current_tile = tile

    def clear(self):
        self.map = [[0 for _ in range(self.map_size)] for _ in range(self.map_size)]
        self.draw()

    def paint(self, event):
        x = event.x // TILE_SIZE
        y = event.y // TILE_SIZE
        if 0 <= x < self.map_size and 0 <= y < self.map_size:
            self.map[y][x] = self.current_tile
            self.draw_cell(x, y)

    def draw(self):
        self.canvas.delete("all")
        for y in range(self.map_size):
            for x in range(self.map_size):
                self.draw_cell(x, y)

    def draw_cell(self, x, y):
        tile = self.map[y][x]
        color = COLORS.get(tile, "#ff00ff")  # fallback to bright magenta for unknown tiles
        self.canvas.create_rectangle(
            x*TILE_SIZE, y*TILE_SIZE,
            (x+1)*TILE_SIZE, (y+1)*TILE_SIZE,
            fill=color, outline="#303030"
        )
        # Optionally show door direction symbol
        if tile == 3:
            # vertical line
            self.canvas.create_line(
                x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + 2,
                x*TILE_SIZE + TILE_SIZE//2, (y+1)*TILE_SIZE - 2,
                fill="#555555", width=2
            )
        elif tile == 4:
            # horizontal line
            self.canvas.create_line(
                x*TILE_SIZE + 2, y*TILE_SIZE + TILE_SIZE//2,
                (x+1)*TILE_SIZE - 2, y*TILE_SIZE + TILE_SIZE//2,
                fill="#555555", width=2
            )

    def load(self):
        path = filedialog.askopenfilename(filetypes=[("THMAP", "*.thmap")])
        if not path: return
        try:
            with open(path, "r") as f:
                data = ast.literal_eval(f.read())
            if len(data) > MAX_SIZE or any(len(row) > MAX_SIZE for row in data):
                raise ValueError(f"Map too big! Max size is {MAX_SIZE}x{MAX_SIZE}")
            self.map_size = len(data)
            self.map = data
            self.canvas.config(width=self.map_size*TILE_SIZE, height=self.map_size*TILE_SIZE)
            self.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load: {e}")

    def save(self):
        path = filedialog.asksaveasfilename(defaultextension=".thmap", filetypes=[("THMAP", "*.thmap")])
        if not path: return
        try:
            with open(path, "w") as f:
                f.write("[\n")
                for row in self.map:
                    f.write(str(row)+",\n")
                f.write("]")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def new_map(self):
        size = simpledialog.askinteger("New Map", f"Enter map size (1-{MAX_SIZE}):", minvalue=1, maxvalue=MAX_SIZE)
        if not size: return
        self.map_size = size
        self.map = [[1 for _ in range(size)] for _ in range(size)]
        self.canvas.config(width=self.map_size*TILE_SIZE, height=self.map_size*TILE_SIZE)
        self.draw()

if __name__ == "__main__":
    root = tk.Tk()
    Editor(root)
    root.mainloop()
