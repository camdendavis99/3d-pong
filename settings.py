from pygame.math import Vector3

MOUSE_MODE = True
FPS = 30
WIN_WIDTH = 1538
WIN_HEIGHT = 834
WIN_DEPTH = int(WIN_WIDTH * 1.5)
WIN_CENTER = Vector3(WIN_WIDTH // 2, WIN_HEIGHT // 2, WIN_DEPTH // 2)
DEPTH_RATIO = 1 / 4
BACK_WIN_WIDTH = int(WIN_WIDTH * DEPTH_RATIO)
BACK_WIN_HEIGHT = int(WIN_HEIGHT * DEPTH_RATIO)
MAX_SCORE = 3
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (160, 160, 160)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

# Points connecting lines in background
POINT_1 = [0, 0]
POINT_2 = [WIN_WIDTH, 0]
POINT_3 = [0, WIN_HEIGHT]
POINT_4 = [WIN_WIDTH, WIN_HEIGHT]
POINT_5 = [(WIN_WIDTH - BACK_WIN_WIDTH) // 2, (WIN_HEIGHT - BACK_WIN_HEIGHT) // 2]
POINT_6 = [(WIN_WIDTH + BACK_WIN_WIDTH) // 2, (WIN_HEIGHT - BACK_WIN_HEIGHT) // 2]
POINT_7 = [(WIN_WIDTH - BACK_WIN_WIDTH) // 2, (WIN_HEIGHT + BACK_WIN_HEIGHT) // 2]
POINT_8 = [(WIN_WIDTH + BACK_WIN_WIDTH) // 2, (WIN_HEIGHT + BACK_WIN_HEIGHT) // 2]