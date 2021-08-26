from pyglet import *
import numpy as np
from pyglet.window import key

WINDOW_SIZE = (1280, 720)
TITLE = '3D Render Test'

#Sets the window size etc.
window = window.Window(*WINDOW_SIZE, TITLE)

@window.event
def on_draw():
    window.clear()

Moving = False
x_pos = 0

@window.event
def on_key_press(symbol, modifiers):
    global Moving
    if symbol == key.W:
        Moving = True


@window.event
def on_key_release(symbol, modifiers):
    global Moving
    if symbol == key.W:
        Moving = False


def update(dt):
    global x_pos
    if Moving == True:
        x_pos += 10
    print(x_pos)


def main():
    clock.schedule_interval(update, 1/60.0)
    app.run()


main()