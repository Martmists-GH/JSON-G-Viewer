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

def get_color(data):
    return "#"+"".join("{:0<2x}".format(x) for x in [data["red"],data["green"],data["blue"]])

WIDTH = data["size"]["width"]
HEIGHT = data["size"]["height"]

bg = get_color(data["layers"][0]["default_color"])

layers = data["layers"]

window = Tk()
window.wm_title("JSON-G Viewer")
canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg=bg)
canvas.pack()
img = PhotoImage(width=WIDTH, height=HEIGHT)
canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")


for layer in layers:
    for pixel in layer["pixels"]:
        pos = pixel["position"]
        img.put(get_color(pixel["color"]), (pos["x"]+1, pos["y"]+1))

mainloop()
