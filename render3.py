from pyglet import *
from math import *

WINDOW_SIZE = [800, 500]
TITLE = '3D Render Test'
SCREEN_DIST = 700

#Sets the window size etc.
window = window.Window(WINDOW_SIZE[0], WINDOW_SIZE[1], TITLE)


class Plane():
    def __init__(self, dist_o, size, rotation = 80):
        self.dist_o = dist_o
        self.size = size
        self.h_size = size / 2
        self.rotation = rotation

    def vertices(self):
        #adds 3d positions of the vertices based on size & object distance.
        rotation = radians(self.rotation)
        physical_vertices = [
            [- self.h_size * cos(rotation), self.h_size, self.dist_o + self.h_size * sin(rotation)],
            [  self.h_size * cos(rotation), self.h_size, self.dist_o - self.h_size * sin(rotation)],
            [- self.h_size * cos(rotation), -self.h_size, self.dist_o + self.h_size * sin(rotation)],
            [  self.h_size * cos(rotation), -self.h_size, self.dist_o - self.h_size * sin(rotation)],
        ]
        return physical_vertices

    def projection(self, SCREEN_DIST):
        # projects the points onto a 2d plane to draw.
        vertices = self.vertices()
        screen_vertices = [[None, None] for i in range(len(vertices))]
        for i in range(len(vertices)):
            theta_horizontal = atan(vertices[i][0] / vertices[i][2])
            screen_vertices[i][0] = SCREEN_DIST * tan(theta_horizontal)
            theta_vertical = atan(vertices[i][1] / vertices[i][2])
            screen_vertices[i][1] = SCREEN_DIST * tan(theta_vertical)
        return screen_vertices

    def draw(self):
        s_v = self.projection(SCREEN_DIST) # s_v = screen vertices
        w_h = window.height // 2
        w_w = window.width // 2
        line_batch = graphics.Batch()
        line1 = shapes.Line(s_v[0][0] + w_w, s_v[0][1] + w_h, s_v[1][0] + w_w, s_v[1][1] + w_h, 2, batch=line_batch)
        line2 = shapes.Line(s_v[0][0] + w_w, s_v[0][1] + w_h, s_v[2][0] + w_w, s_v[2][1] + w_h, 2, batch=line_batch)
        line3 = shapes.Line(s_v[1][0] + w_w, s_v[1][1] + w_h, s_v[3][0] + w_w, s_v[3][1] + w_h, 2, batch=line_batch)
        line4 =  shapes.Line(s_v[2][0] + w_w, s_v[2][1] + w_h, s_v[3][0] + w_w, s_v[3][1] + w_h, 2, batch=line_batch)
        # line5 = shapes.Line(s_v[0][0] + w_w, s_v[0][1] + w_h, s_v[3][0] + w_w, s_v[3][1] + w_h, 2, batch=line_batch)
        # line6 = shapes.Line(s_v[1][0] + w_w, s_v[1][1] + w_h, s_v[2][0] + w_w, s_v[2][1] + w_h, 2, batch=line_batch)
        line_batch.draw()

    def update(self, dt):
        self.rotation += 1


plane = Plane(500, 100)


@window.event
def on_draw():
    window.clear()
    plane.draw()

#Starts the event loop.
clock.schedule_interval(plane.update, 1/120.0)
app.run()
