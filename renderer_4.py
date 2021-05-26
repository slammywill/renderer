import pygame
import numpy as np

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
GREEN = (0, 255, 0)
pygame.display.set_caption("Renderer")


class Camera():
    """Creates the Camera class."""
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
        rotate_x = np.array([[1, 0, 0], [0, np.cos(self.angle[0]), - np.sin(self.angle[0])], [0, np.sin(self.angle[0]), np.cos(self.angle[0])]])
        rotate_y = np.array([[np.cos(self.angle[1]), 0, np.sin(self.angle[1])], [0, 1, 0], [- np.sin(self.angle[1]), 0, np.cos(self.angle[1])]])
        rotate_z = np.array([[np.cos(self.angle[2]), - np.sin(self.angle[2]), 0], [np.sin(self.angle[2]), np.cos(self.angle[2]), 0], [0, 0, 1]])

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


camera_position = [0, 0, -200]
camera_angle = [0, 0, 0]
screen_position = [0, 0, -180]
camera = Camera(camera_position, camera_angle, screen_position)


class Cube:
    """Creates a cube."""
    num_of_cubes = 0

    def __init__(self, position):
        """Initialises a cube with a position as (x, y, z)."""
        self.position = position
        self.vertices = vertices()
        Cube.add_cube()

    @classmethod
    def add_cube(cls):
        """Adds 1 to number of cubes."""
        cls.num_of_cubes += 1


    def vertices(self):
        """Creates the cubes 8 vertices."""
        vertice_list = np.array([
            [self.position[0]    , self.position[1]    , self.position[2]    ], # \
            [self.position[0] + 1, self.position[1]    , self.position[2]    ], #  |_ top face
            [self.position[0] + 1, self.position[1]    , self.position[2] - 1], #  |
            [self.position[0]    , self.position[1]    , self.position[2] - 1], # /

            [self.position[0]    , self.position[1] - 1, self.position[2]    ], # \
            [self.position[0] + 1, self.position[1] - 1, self.position[2]    ], #  |_ bottom face
            [self.position[0] + 1, self.position[1] - 1, self.position[2] - 1], #  |
            [self.position[0]    , self.position[1] - 1, self.position[2] - 1]  # /
        ])
        return vertice_list


def draw_window():
    """Draws to the window."""
    pygame.draw.aaline(WIN, GREEN, (0, 0), (100, 100))
    pygame.display.update()


def main():
    """Main."""
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window()
    pygame.quit()


if __name__ == "__main__":
    main()