from math import *
from pyglet import *
from pyglet.window import key

WINDOW_SIZE = [1280, 720]
TITLE = '3D Render Test'
SCREEN_DIST = 1500

position = [0, 0, 100]
rotation = [0, 0, 0]


class Cube():
    def __init__(self, size, position, rotation):
        """Initialises a cube.

        Args:
            size (int / float): The sidelength of the cube.
            position (list): The x, y & z co-ordinates of the cube's center.
            rotation (list): The cube's rotations around the x, y & z axis.
        """
        self.size = ((2 * size **2) ** 0.5)
        self.radius = self.size / 2
        self.position = position
        self.rotation = [radians(x) for x in rotation]

    def vertices(self):
        """Calculates the vertices x, y & z position based on the cube's location, size
        and rotation.

        Returns:
            real_vertices(list): A list of lists containing the x, y & z co-ordinates of
            each vertice.
        """
        rotator = [(((2 * self.radius ** 2) ** 0.5) * sin(self.rotation[0] + (pi / 4)) * sin(self.rotation[2] + (pi / 4))),
                   (((2 * self.radius ** 2) ** 0.5) * sin(self.rotation[0] + (pi / 4)) * sin(self.rotation[1] + (pi / 4))),
                   (((2 * self.radius ** 2) ** 0.5) * sin(self.rotation[1] + (pi / 4)) * sin(self.rotation[2] + (pi / 4)))]
        real_vertices = [
            [self.position[0] - rotator[0], self.position[1] + rotator[1], self.position[2] - rotator[2]],
            [self.position[0] + rotator[0], self.position[1] + rotator[1], self.position[2] - rotator[2]],
            [self.position[0] - rotator[0], self.position[1] + rotator[1], self.position[2] + rotator[2]],
            [self.position[0] + rotator[0], self.position[1] + rotator[1], self.position[2] + rotator[2]],
            [self.position[0] - rotator[0], self.position[1] - rotator[1], self.position[2] - rotator[2]],
            [self.position[0] + rotator[0], self.position[1] - rotator[1], self.position[2] - rotator[2]],
            [self.position[0] - rotator[0], self.position[1] - rotator[1], self.position[2] + rotator[2]],
            [self.position[0] + rotator[0], self.position[1] - rotator[1], self.position[2] + rotator[2]]]
        return real_vertices

    def projection(self, SCREEN_DIST):
        """Projects each 3d vertice to a 2d x & y.

        Returns:
            screen_vertices (list): A list of 2d co-ordinates.
        """
        vertices = self.vertices()
        screen_vertices = [[None, None] for i in range(len(vertices))]
        for i in range(len(vertices)):
            theta_horizontal = atan(vertices[i][0] / vertices[i][2])
            screen_vertices[i][0] = SCREEN_DIST * tan(theta_horizontal)
            theta_vertical = atan(vertices[i][1] / vertices[i][2])
            screen_vertices[i][1] = SCREEN_DIST * tan(theta_vertical)
        return screen_vertices

    def draw(self):
        """Draws the lines that connect the 2d vertices to form a cube.
        """
        s_v = self.projection(SCREEN_DIST) # s_v = screen vertices
        w_h = WINDOW_SIZE[1] // 2
        w_w = WINDOW_SIZE[0] // 2
        line_batch = graphics.Batch()

        line1 = shapes.Line(s_v[0][0] + w_w, s_v[0][1] + w_h, s_v[1][0] + w_w, s_v[1][1] + w_h, 2, batch=line_batch)
        line2 = shapes.Line(s_v[0][0] + w_w, s_v[0][1] + w_h, s_v[2][0] + w_w, s_v[2][1] + w_h, 2, batch=line_batch)
        line3 = shapes.Line(s_v[3][0] + w_w, s_v[3][1] + w_h, s_v[1][0] + w_w, s_v[1][1] + w_h, 2, batch=line_batch)
        line4 = shapes.Line(s_v[3][0] + w_w, s_v[3][1] + w_h, s_v[2][0] + w_w, s_v[2][1] + w_h, 2, batch=line_batch)

        line5 = shapes.Line(s_v[4][0] + w_w, s_v[4][1] + w_h, s_v[5][0] + w_w, s_v[5][1] + w_h, 2, batch=line_batch)
        line6 = shapes.Line(s_v[4][0] + w_w, s_v[4][1] + w_h, s_v[6][0] + w_w, s_v[6][1] + w_h, 2, batch=line_batch)
        line7 = shapes.Line(s_v[7][0] + w_w, s_v[7][1] + w_h, s_v[6][0] + w_w, s_v[6][1] + w_h, 2, batch=line_batch)
        line8 = shapes.Line(s_v[7][0] + w_w, s_v[7][1] + w_h, s_v[5][0] + w_w, s_v[5][1] + w_h, 2, batch=line_batch)

        line9 = shapes.Line(s_v[0][0] + w_w, s_v[0][1] + w_h, s_v[4][0] + w_w, s_v[4][1] + w_h, 2, batch=line_batch)
        line10 = shapes.Line(s_v[1][0] + w_w, s_v[1][1] + w_h, s_v[5][0] + w_w, s_v[5][1] + w_h, 2, batch=line_batch)
        line11 = shapes.Line(s_v[2][0] + w_w, s_v[2][1] + w_h, s_v[6][0] + w_w, s_v[6][1] + w_h, 2, batch=line_batch)
        line12 = shapes.Line(s_v[3][0] + w_w, s_v[3][1] + w_h, s_v[7][0] + w_w, s_v[7][1] + w_h, 2, batch=line_batch)
        line_batch.draw()

    def update(self, dt):
        pass

cube = Cube(10, position, rotation)


#Sets the window size etc.
window = window.Window(WINDOW_SIZE[0], WINDOW_SIZE[1], TITLE)


@window.event
def on_draw():
    window.clear()
    cube.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.W:
        position[1] += 1
    elif symbol == key.A:
        position[0] -= 1
    elif symbol == key.S:
        position[1] -= 1
    elif symbol == key.D:
        position[0] += 1
    elif symbol == key.Q:
        position[2] += 1
    elif symbol == key.E:
        position[2] -= 1



def main():
    clock.schedule_interval(cube.update, 1/120.0)
    app.run()


main()