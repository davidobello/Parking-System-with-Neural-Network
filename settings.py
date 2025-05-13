import pygame

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

obstacles = []
grid_size = 2
cell_size = HEIGHT // (grid_size + 1)

PARKING_SPOTS = [pygame.Rect(100 + i * 110, 250, 50, 100) for i in range(6)]
PARKING_SPOTS = [pygame.Rect(100, 250, 50, 100), pygame.Rect(100 + 550, 250, 50, 100)]

# for i in range(grid_size):
#     for j in range(grid_size):
#         ox = (i + 1) * cell_size
#         oy = (j + 1) * cell_size
#         obstacles.append(pygame.Rect(ox, oy, 50, 50))

obstacles = [pygame.Rect(200, 210, 50, 50), pygame.Rect(300, 210, 50, 50),
             pygame.Rect(200, 320, 50, 50), pygame.Rect(300, 320, 50, 50)]