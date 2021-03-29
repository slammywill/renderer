from math import *
from pyglet import *
import numpy as np


WINDOW_SIZE = [1280, 720]
TITLE = '3D Render Test'
SCALE = 25

orthographic = np.array([[1, 0, 0],
                         [0, 1, 0]])

class Cube():
    def __init__(self, size, position, angle):
        """Creates a cube object.

        Args:
            size (int / float): The sidelength of the cube.
            position (list): The x,y,z co-ordinates of the cube.
            angle ([type]): The rotations around the x,y,z axis' of the cube.
        """
        self.angle = [radians(x) for x in angle]
        self.size = size
        self.position = position
        self.rad = size / 2
        self.vertice = self.vertices()

    def vertices(self):
        """Creates the 3d vertices of the cube based on the sidelength and position of the cube.

        Returns:
            list: The x,y,z co-ordinates of the vertices.
        """
        physical_vertices = np.array([
            [self.position[0] - self.rad, self.position[1] + self.rad, self.position[2] - self.rad],
            [self.position[0] + self.rad, self.position[1] + self.rad, self.position[2] - self.rad],
            [self.position[0] + self.rad, self.position[1] + self.rad, self.position[2] + self.rad],
            [self.position[0] - self.rad, self.position[1] + self.rad, self.position[2] + self.rad],
            [self.position[0] - self.rad, self.position[1] - self.rad, self.position[2] - self.rad],
            [self.position[0] + self.rad, self.position[1] - self.rad, self.position[2] - self.rad],
            [self.position[0] + self.rad, self.position[1] - self.rad, self.position[2] + self.rad],
            [self.position[0] - self.rad, self.position[1] - self.rad, self.position[2] + self.rad],
        ])
        return physical_vertices

    def rotate(self):
        """Performs a rotation around the center of the cube to the vertices.

        Returns:
            list: The x,y,z co-ordinates of the newly rotated vertices.
        """
        vertices = self.vertice
        rotate_x = np.array([[1, 0, 0], [0, cos(self.angle[0]), - sin(self.angle[0])], [0, sin(self.angle[0]), cos(self.angle[0])]])
        rotate_y = np.array([[cos(self.angle[1]), 0, sin(self.angle[1])], [0, 1, 0], [- sin(self.angle[1]), 0, cos(self.angle[1])]])
        rotate_z = np.array([[cos(self.angle[2]), - sin(self.angle[2]), 0], [sin(self.angle[2]), cos(self.angle[2]), 0], [0, 0, 1]])

        rotated_vertices = np.array([np.matmul(rotate_x, x) for x in vertices])
        rotated_vertices = np.array([np.matmul(rotate_y, x) for x in rotated_vertices])
        rotated_vertices = np.array([np.matmul(rotate_z, x) for x in rotated_vertices])
        return rotated_vertices

    def projection(self, p_matrix):
        """Projects the 3d positions of the vertices onto a 2d plane to render.

        Args:
            p_matrix (list): The projection matrix that does the 3d -> 2d transformation.

        Returns:
            list: The x,y points of the cubes vertices after projection.
        """
        vertices = self.rotate()
        points = np.array([np.matmul(p_matrix, x) for x in vertices])
        return points

    def draw(self):
        """Creates and draws the lines between the points on the cube.
        """
        points = self.projection(orthographic)
        w_h = WINDOW_SIZE[1] // 2
        w_w = WINDOW_SIZE[0] // 2
        line_batch = graphics.Batch()
        lines = dict()
        color = (0, 255, 0)

        for i in range(4):
            lines[f"a{i}"] = shapes.Line(points[i][0] + w_w, points[i][1] + w_h,
            points[(i + 1) % 4][0] + w_w, points[(i + 1) % 4][1] + w_h, 2, color, batch=line_batch)
            lines[f"b{i}"] = shapes.Line(points[i + 4][0] + w_w, points[i + 4][1] + w_h,
            points[((i + 1) % 4) + 4][0] + w_w, points[((i + 1) % 4) + 4][1] + w_h, 2, color, batch=line_batch)
            lines[f"c{i}"] = shapes.Line(points[i][0] + w_w, points[i][1] + w_h,
            points[i + 4][0] + w_w, points[i + 4][1] + w_h, 2, color, batch=line_batch)
        line_batch.draw()

    def update(self, dt):
        """Performs the update on the cube every timestep.

        Args:
            dt (float): The timestep in seconds.
        """
        self.angle[0] += 0.05
        self.angle[1] += 0.05
        self.angle[2] += 0.011


position = [0, 0, 0]
angle = [0, 0, 0]
cube = Cube(100, position, angle)

window = window.Window(WINDOW_SIZE[0], WINDOW_SIZE[1], TITLE)


@window.event
def on_draw():
    """Renders the pyglet window.
    """
    window.clear()
    cube.draw()


def main():
    """Runs the main program.
    """
    clock.schedule_interval(cube.update, 1/120.0)
    app.run()


main()