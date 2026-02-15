import tkinter as tk
from tkinter import filedialog, messagebox
import ast  # safer than eval

TILE_SIZE = 30  # pixels per tile
MAX_SIZE = 100  # max map size

COLOR_MAP = {
    0: "saddlebrown",  # floor
    1: "black",        # wall
    2: "red",          # enemy
    3: "gray",         # door vertical
    4: "lightgray",    # door horizontal
}

class MapViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Tactical Hotel Map Viewer")
        self.canvas = None
        self.game_map = []
        self.spawn_pos = None

        tk.Button(root, text="Open .thmap", command=self.open_file).pack(pady=5)

    def open_file(self):
        filename = filedialog.askopenfilename(
            title="Select .thmap file", 
            filetypes=[("Tactical Hotel Map", "*.thmap")]
        )
        if not filename:
            return
        try:
            with open(filename, "r") as f:
                content = f.read()
            game_map = ast.literal_eval(content)
            if len(game_map) > MAX_SIZE or any(len(row) > MAX_SIZE for row in game_map):
                messagebox.showerror("Error", f"Map exceeds maximum size of {MAX_SIZE}x{MAX_SIZE}")
                return
            self.game_map = game_map
            self.spawn_pos = self.find_spawn(game_map)
            self.draw_map()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load map: {e}")

    def find_spawn(self, game_map):
        for r, row in enumerate(game_map):
            for c, tile in enumerate(row):
                if tile == 0:
                    return (r, c)
        return None

    def draw_map(self):
        if self.canvas:
            self.canvas.destroy()
        rows = len(self.game_map)
        cols = len(self.game_map[0])
        self.canvas = tk.Canvas(self.root, width=cols*TILE_SIZE, height=rows*TILE_SIZE)
        self.canvas.pack()

        for r, row in enumerate(self.game_map):
            for c, tile in enumerate(row):
                x1 = c * TILE_SIZE
                y1 = r * TILE_SIZE
                x2 = x1 + TILE_SIZE
                y2 = y1 + TILE_SIZE

                # Highlight spawn point
                color = "green" if self.spawn_pos == (r, c) else COLOR_MAP.get(tile, "magenta")
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

                # Draw door direction line
                if tile == 3:
                    # vertical line for up/down door
                    self.canvas.create_line(
                        x1 + TILE_SIZE//2, y1 + 4,
                        x1 + TILE_SIZE//2, y2 - 4,
                        fill="#555555", width=2
                    )
                elif tile == 4:
                    # horizontal line for left/right door
                    self.canvas.create_line(
                        x1 + 4, y1 + TILE_SIZE//2,
                        x2 - 4, y1 + TILE_SIZE//2,
                        fill="#555555", width=2
                    )


if __name__ == "__main__":
    root = tk.Tk()
    viewer = MapViewer(root)
    root.mainloop()
