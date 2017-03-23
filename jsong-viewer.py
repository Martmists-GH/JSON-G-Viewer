from tkinter import Tk, Canvas, PhotoImage, mainloop
from threading import Thread
from sys import exit, argv
from json import load
from json.decoder import JSONDecodeError

usage = """
Usage: python json-viewer.py <path> [thread_count]

Arguments:
    path            Path to the jsong-g file
    thread_count    Amount of threads to use during rendering
                    Default: 4
"""

if len(argv) < 2:
    print(usage)
    exit(1)

with open(argv[1]) as f:
    try:
        data = load(f)
    except JSONDecodeError as e:
        print("Invalid JSON-G!")
        print(" ".join(e.args))
        exit(1)

if len(argv) > 3:
	thread_count = argv[2]
    
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

class Window(Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.deiconify()

WIDTH = data["size"]["width"]
HEIGHT = data["size"]["height"]
bg_data = data["layers"][0]["default_color"]
bg = Color.from_rgb(bg_data["red"],bg_data["green"],bg_data["blue"])

layers = data["layers"]

window = Window()
window.wm_title("JSON-G Viewer")
canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg=str(bg))
canvas.pack()
img = PhotoImage(width=WIDTH, height=HEIGHT)
canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")

def load_pixels(img, data, pixels):
    for pixel in pixels:
        pos = pixel["position"]
        clr = pixel["color"]
        color = Color.from_rgb(clr["red"],clr["green"],clr["blue"])
        if data["transparency"] is True and clr["alpha"] != 255:
            color.add_alpha(clr["alpha"])
            other = Color.from_rgb(*img.get(pos["x"]+1, pos["y"]+1))
            new = color.blend(other)
        else:
            new = color
        img.put(str(new), (pos["x"]+1, pos["y"]+1))

def load_image(img, data, thread_count):
    for layer in layers:
        pixel_count = len(layer["pixels"])
        num_per_thread = round(pixel_count/thread_count)
        for i in range(thread_count):
            t = Thread(target=load_pixels, args=(img, data, layer["pixels"][i*num_per_thread:(i+1)*num_per_thread]))
            t.start()

# The amount of threads you want to use. 
# I have experienced it to perform best at around 4 or 5, 
# but this may vary depending on the hardware you have.
try:
	# Check if it was defined in sys.argv
	thread_count
except:
	thread_count = 4

t = Thread(target=load_image, args=(img, data, thread_count))
t.start()
window.mainloop()
