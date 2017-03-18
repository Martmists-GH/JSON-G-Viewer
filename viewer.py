from tkinter import Tk, Canvas, PhotoImage, mainloop
import sys
import json

if len(sys.argv) < 2:
    print("No path given.")
    sys.exit(1)

with open(sys.argv[1]) as f:
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print("Invalid JSON-G!")
        print(" ".join(e.args))
        sys.exit(1)
    
class Color:
    def __init__(self, value):
        if not value:
            value = 0
        elif isinstance(value, str):
            value = int(value.strip("#"), 16)
        self.value = value

    def _get_rgb(self, byte):
        return (self.value >> (8 * byte)) & 0xff

    def __str__(self):
        return '#{:0>6x}'.format(self.value)

    def blend(self, clr):
        return Color.from_rgb(
            (self.r + clr.r)/2,
            (self.g + clr.g)/2,
            (self.b + clr.b)/2
        )

    def add_alpha(self, alpha):
        self.r = self.r*(alpha/255)
        self.g = self.g*(alpha/255)
        self.b = self.b*(alpha/255)
            
    @property
    def r(self):
        return self._get_rgb(2)

    @property
    def g(self):
        return self._get_rgb(1)

    @property
    def b(self):
        return self._get_rgb(0)

    @r.setter
    def r(self, value):
        self = Color.from_rgb(value, self.g, self.b)

    @g.setter
    def g(self, value):
        self = Color.from_rgb(self.r, value, self.b)

    @b.setter
    def b(self, value):
        self = Color.from_rgb(self.r, self.g, value)

    @classmethod
    def from_rgb(cls, r, g, b):
        """ (0,0,0) to (255,255,255) """
        value = ((int(r) << 16) + (int(g) << 8) + int(b))
        return cls(value)

WIDTH = data["size"]["width"]
HEIGHT = data["size"]["height"]
bg_data = data["layers"][0]["default_color"]
bg = Color.from_rgb(bg_data["red"],bg_data["green"],bg_data["blue"])

layers = data["layers"]

window = Tk()
window.wm_title("JSON-G Viewer")
canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg=str(bg))
canvas.pack()
img = PhotoImage(width=WIDTH, height=HEIGHT, format="RGBA")
canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")

for layer in layers:
    for pixel in layer["pixels"]:
        pos = pixel["position"]
        clr = pixel["color"]
        color = Color.from_rgb(clr["red"],clr["green"],clr["blue"])
        color.add_alpha(clr["alpha"])
        if clr["alpha"] != 255:
            other = Color.from_rgb(*img.get(pos["x"]+1, pos["y"]+1))
            new = color.blend(other)
        else:
            new = color
        img.put(str(new), (pos["x"]+1, pos["y"]+1))

mainloop()
