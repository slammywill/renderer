from math import *
from pyglet import *
import numpy as np


WINDOW_SIZE = (1280, 720)
TITLE = '3D Render Test'


class Camera():
    def __init__(self, position, angle, screen_position):
        """Creates the camera and screen.

        Args:
            position (list): The x,y,z co-ordinates of the camera object.
            angles (list): The rotations around the x,y,z axis' of the camera.
            screen_position (list): The x,y,z co-ordinates of the projection screen.
        """
        self.position = position
        self.angle = angle
        self.screen_position = screen_position

    def camera_matrices(self, vertice_position):
        """Defines the matrices used in the projection calculation

        Args:
            angle (list): The rotations around the x,y,z axis' of the camera.
        """
        rotate_x = np.array([[1, 0, 0], [0, cos(self.angle[0]), - sin(self.angle[0])], [0, sin(self.angle[0]), cos(self.angle[0])]])
        rotate_y = np.array([[cos(self.angle[1]), 0, sin(self.angle[1])], [0, 1, 0], [- sin(self.angle[1]), 0, cos(self.angle[1])]])
        rotate_z = np.array([[cos(self.angle[2]), - sin(self.angle[2]), 0], [sin(self.angle[2]), cos(self.angle[2]), 0], [0, 0, 1]])

        position_offset = np.subtract(vertice_position, self.position)
        return(rotate_x, rotate_y, rotate_z, position_offset)

    def camera_transform(self, vertice_position):
        """Does the camera transform on the vertices.

        Args:
            vertice_position (list): The x,y,z co-ordinates of the vertices.

        Returns:
            vect_d (list): The vectors to convert to 2d.
        """
        arguments = self.camera_matrices(vertice_position)
        vect_d = arguments[0] @ arguments[1] @ arguments[2] @ arguments[3]
        return vect_d

    def projection(self, vertice_position):
        """Converts the 3d vectors to 2d points.

        Args:
            vertice_position (list): The x,y,z co-ordinates of the vertices.

        Returns:
            vertice_2d (list): The 2d points of the vertices.
        """
        vect_d = self.camera_transform(vertice_position)
        vertice_2d = [None, None]
        vertice_2d[0] = (self.screen_position[2] / vect_d[2]) * vect_d[0] + self.screen_position[0]
        vertice_2d[1] = (self.screen_position[2] / vect_d[2]) * vect_d[1] + self.screen_position[1]
        return vertice_2d

    def camera_transform(self, vertice_position):
        """Does the camera transform on the vertices.

        Args:
            vertice_position (list): The x,y,z co-ordinates of the vertices.

        Returns:
            vect_d (list): The vectors to convert to 2d.
        """
        arguments = self.camera_matrices(vertice_position)
        vect_d = arguments[0] @ arguments[1] @ arguments[2] @ arguments[3]
        return vect_d


class Cube():
    def __init__(self, size, position, angle):
        """Creates a cube object.

        Args:
            size (int / float): The sidelength of the cube.
            position (list): The x,y,z co-ordinates of the cube.
            angle (list): The rotations around the x,y,z axis' of the cube.
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
        """Performs a rotation around 0, 0, 0 to the vertices.

        Returns:
            list: The x,y,z co-ordinates of the newly rotated vertices.
        """
        vertices = self.vertice
        rotate_x = np.array([[1, 0, 0], [0, cos(self.angle[0]), - sin(self.angle[0])], [0, sin(self.angle[0]), cos(self.angle[0])]])
        rotate_y = np.array([[cos(self.angle[1]), 0, sin(self.angle[1])], [0, 1, 0], [- sin(self.angle[1]), 0, cos(self.angle[1])]])
        rotate_z = np.array([[cos(self.angle[2]), - sin(self.angle[2]), 0], [sin(self.angle[2]), cos(self.angle[2]), 0], [0, 0, 1]])

        rotated_vertices = np.array([rotate_x @ x for x in vertices])
        rotated_vertices = np.array([rotate_y @ x for x in rotated_vertices])
        rotated_vertices = np.array([rotate_z @ x for x in rotated_vertices])
        return rotated_vertices

    def draw(self):
        """Creates and draws the lines between the points on the cube.
        """
        vertices = self.rotate()
        points = [camera.projection(x) for x in vertices]
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
        self.angle[1] += 0.01
        self.angle[2] += 0.05


camera_position = [0, 0, -200]
camera_angle = [0, 0, 0]
screen_position = [0, 0, -180]
camera = Camera(camera_position, camera_angle, screen_position)

cube_position = [0, 0, 0]
cube_angle = [0, 0, 0]
cube = Cube(100, cube_position, cube_angle)

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
    clock.schedule_interval(cube.update, 1/60.0)
    app.run()


main()

