import pygame
import numpy as np

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
GREEN = (0, 255, 0)
pygame.display.set_caption("Renderer")


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
            [self.position[0]    , self.position[1]    , self.position[2]    ] # \
            [self.position[0] + 1, self.position[1]    , self.position[2]    ] #  |_ top face
            [self.position[0] + 1, self.position[1]    , self.position[2] - 1] #  |
            [self.position[0]    , self.position[1]    , self.position[2] - 1] # /

            [self.position[0]    , self.position[1] - 1, self.position[2]    ] # \
            [self.position[0] + 1, self.position[1] - 1, self.position[2]    ] #  |_ bottom face
            [self.position[0] + 1, self.position[1] - 1, self.position[2] - 1] #  |
            [self.position[0]    , self.position[1] - 1, self.position[2] - 1] # /
        ])
        return vertice_list


def draw():
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
        draw()
    pygame.quit()


if __name__ == "__main__":
    main()