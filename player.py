import pygame
import numpy as np
from pygame.math import Vector2, Vector3
from settings import *


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.color = WHITE
        self.score = 0
        self.width, self.height = WIN_WIDTH, WIN_HEIGHT
        self.racket_height = WIN_HEIGHT
        self.racket_width = WIN_WIDTH // 5
        self.image = pygame.Surface([self.racket_width, self.racket_height])
        self.image.fill(self.color)
        self.image.set_alpha(60)
        self.position = Vector3(WIN_CENTER.x, WIN_CENTER.y, 0)
        self.rect = self.image.get_rect(topleft=(self.position.x, self.position.y))
        self.last_position = Vector2(self.position.x, self.position.y)
        self.is_green = False
        self.recent_hit = False

    """
    def move(self, x, y):
        self.position.x = x - self.racket_width//2
        self.position.y = y - self.racket_height//2

        if self.position.x + self.racket_width > WIN_WIDTH:
            self.position.x = WIN_WIDTH - self.racket_width
        elif self.position.x < 0:
            self.position.x = 0
        if self.position.y + self.racket_height > WIN_HEIGHT:
            self.position.y = WIN_HEIGHT - self.racket_height
        elif self.position.y < 0:
            self.position.y = 0

        self.rect.left = self.position.x
        self.rect.top = self.position.y
    """

    def move(self, hand):
        location = hand.get_hand_location()
        if location is None:
            mx, my = (self.last_position.x, self.last_position.y)
        else:
            mx, my = (1 - location[0]) * WIN_WIDTH, location[1] * WIN_HEIGHT
            self.last_position.x, self.last_position.y = mx, my
        dist = np.linalg.norm(np.array((self.position.x, self.position.y)) - np.array((mx, my)))
        move_dist = 25 if dist >= 100 else dist * 0.25
        m = 99999
        if (mx - self.position.x) != 0:
            m = (my - self.position.y) / (mx - self.position.x)
        if mx > self.position.x:
            self.position.x = self.position.x + move_dist * np.sqrt(1 / (1 + m * m))
        else:
            self.position.x = self.position.x - move_dist * np.sqrt(1 / (1 + m * m))

        if my > self.position.y:
            self.position.y = self.position.y + m * move_dist * np.sqrt(1 / (1 + m * m))
        else:
            self.position.y = self.position.y - m * move_dist * np.sqrt(1 / (1 + m * m))

        # Restricts the ball to the window
        if self.position.x < 0:
            self.position.x = 0
        elif self.position.x + self.racket_width > WIN_WIDTH:
            self.position.x = WIN_WIDTH - self.racket_width
        if self.position.y < 0:
            self.position.y = 0
        elif self.position.y + self.racket_height > WIN_HEIGHT:
            self.position.y = WIN_HEIGHT - self.racket_height

        self.rect.left = self.position.x
        self.rect.top = self.position.y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def toggle_color(self):
        self.color = WHITE if self.is_green else GREEN