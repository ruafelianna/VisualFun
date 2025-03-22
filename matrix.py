import tkinter as tk
import random

DROPS_COUNT = 400
REDRAW_DELAY_MS = 50
CHARS = "アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトホモヨョロヲゴゾドボポヴッンABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

class Point:
    def __init__(self,x, y, color_g, color_rb, step, length):
        self.x = x
        self.y = y
        self.color_g = color_g
        self.color_rb = color_rb
        self.step = step
        self.length = length

    @property
    def color(self):
        color(self.color_g, self.color_rb)

def color(color_g:int, color_rb:int):
    return f'#{color_rb:02x}{color_g:02x}{color_rb:02x}'

class MatrixEffect:
    def __init__(self, root : tk.Tk):
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.root.config(cursor="none")
        self.root.title("The Matrix")
        self.root.bind('<Escape>', lambda _: root.destroy())

        self.canvas = tk.Canvas(root, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.chars = CHARS
        self.delta_time = REDRAW_DELAY_MS
        self.drops = []
        self.drops_update : dict[Point, list[int]] = {}
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.create_drops()
        self.animate()

    def create_drops(self):
        for _ in range(DROPS_COUNT):
            x = random.randint(0, self.width)
            y = random.randint(-self.height, 0)
            color_g = random.choice((random.randint(55, 254), 255))
            color_rb = random.randint(0, 200) if color_g == 255 else 0
            step = random.randint(5, 25)
            length = random.randint(1, step)

            drop = Point(x, y, color_g, color_rb, step, length)
            self.drops.append(drop)
            self.drops_update[drop] = []

    def animate(self):
        drop : Point
        for drop in self.drops:
            symbol = random.choice(self.chars)
            text_obj = self.canvas.create_text(drop.x, drop.y, text=symbol, fill=drop.color, font=('Courier', 12))

            self.drops_update[drop].append(text_obj)

            for i, text_id in enumerate(self.drops_update[drop]):
                color_g = drop.color_g
                color_rb = drop.color_rb
                delta = 255 - (i * 10)
                if delta >= color_rb:
                    color_rb = 0
                    color_g = max(color_g - delta + color_rb, 20)
                else:
                    color_rb = max(color_rb - delta, 20)
                self.canvas.itemconfig(text_id, fill=color(color_g, color_rb))

            if len(self.drops_update[drop]) > drop.length:
                val = self.drops_update[drop].pop(0)
                self.canvas.delete(val)

            if drop.y > self.height:
                drop.x = random.randint(0, self.width)
                drop.y = -10
            else:
                drop.y += drop.step

        self.root.after(self.delta_time, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    matrix = MatrixEffect(root)
    root.mainloop()
