import tkinter as tk
from tkinter import filedialog, messagebox
import ast

TILE_SIZE = 24
GRID = 20

COLORS = {
    0: "#8b6b3f",  # floor brown
    1: "#000000",  # wall black
    2: "#ff2b2b"   # enemy red
}

class Editor:
    def __init__(self, root):
        self.root = root
        self.root.title("THMAP Editor")

        self.current_tile = 1
        self.map = [[1 for _ in range(GRID)] for _ in range(GRID)]

        self.canvas = tk.Canvas(root, width=GRID*TILE_SIZE, height=GRID*TILE_SIZE, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=4)
        self.canvas.bind("<Button-1>", self.paint)
        self.canvas.bind("<B1-Motion>", self.paint)

        tk.Button(root, text="Wall", command=lambda: self.set_tile(1)).grid(row=1, column=0, sticky="ew")
        tk.Button(root, text="Floor", command=lambda: self.set_tile(0)).grid(row=1, column=1, sticky="ew")
        tk.Button(root, text="Enemy", command=lambda: self.set_tile(2)).grid(row=1, column=2, sticky="ew")
        tk.Button(root, text="Clear", command=self.clear).grid(row=1, column=3, sticky="ew")

        tk.Button(root, text="Load", command=self.load).grid(row=2, column=0, columnspan=2, sticky="ew")
        tk.Button(root, text="Save", command=self.save).grid(row=2, column=2, columnspan=2, sticky="ew")

        self.draw()

    def set_tile(self, tile):
        self.current_tile = tile

    def clear(self):
        self.map = [[0 for _ in range(GRID)] for _ in range(GRID)]
        self.draw()

    def paint(self, event):
        x = event.x // TILE_SIZE
        y = event.y // TILE_SIZE
        if 0 <= x < GRID and 0 <= y < GRID:
            self.map[y][x] = self.current_tile
            self.draw_cell(x, y)

    def draw(self):
        self.canvas.delete("all")
        for y in range(GRID):
            for x in range(GRID):
                self.draw_cell(x, y)

    def draw_cell(self, x, y):
        color = COLORS[self.map[y][x]]
        self.canvas.create_rectangle(
            x*TILE_SIZE, y*TILE_SIZE,
            (x+1)*TILE_SIZE, (y+1)*TILE_SIZE,
            fill=color, outline="#303030"
        )

    def load(self):
        path = filedialog.askopenfilename(filetypes=[("THMAP", "*.thmap")])
        if not path:
            return
        try:
            with open(path, "r") as f:
                data = ast.literal_eval(f.read())
            if len(data) != GRID or any(len(row) != GRID for row in data):
                raise ValueError("Map must be 20x20")
            self.map = data
            self.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load: {e}")

    def save(self):
        path = filedialog.asksaveasfilename(defaultextension=".thmap", filetypes=[("THMAP", "*.thmap")])
        if not path:
            return
        try:
            with open(path, "w") as f:
                f.write("[\n")
                for row in self.map:
                    f.write(str(row) + ",\n")
                f.write("]")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    Editor(root)
    root.mainloop()