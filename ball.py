import pygame
import random
import numpy as np
from pygame.math import Vector2, Vector3
from settings import *


class Ball(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.width, self.height = WIN_WIDTH, WIN_HEIGHT
        self.image = pygame.Surface([10, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.initialize()
        self.max_size = 30
        self.min_size = int(self.max_size * DEPTH_RATIO)

    def initialize(self):
        """Reset the attributes of the ball for a restart.

        Called when the ball leaves the screen and a player scores.
        """
        self.direction = Vector3(random.choice([-8, 8]), random.choice([-8, 8]), random.choice([-10, 10]))
        self.position = Vector3(WIN_CENTER.x, WIN_CENTER.y, WIN_CENTER.z)
        self.rect.center = (self.position.x, self.position.y)
        self.speed_up = 1.0

    def hit(self):
        self.speed_up += 0.1

    def update(self):
        if self.position.y <= 40 or self.position.y >= self.height - 40:
            self.direction.y *= -1
        if self.position.x <= 40 or self.position.x >= self.width - 40:
            self.direction.x *= -1

        self.position += self.direction * self.speed_up
        self.rect.center = (self.position.x, self.position.y)

    def draw(self, screen):
        depth_factor = self.position.z / WIN_DEPTH
        size_differential = self.max_size - self.min_size
        size = self.max_size - int(depth_factor * size_differential)
        radius = size // 2

        ball_center = Vector2(self.position.x + radius, self.position.y + radius)
        dist_from_center = Vector2(ball_center.x - WIN_CENTER.x, ball_center.y - WIN_CENTER.y)

        k = 1 - depth_factor + (depth_factor * DEPTH_RATIO)
        new_dist_from_center = Vector2(int(dist_from_center.x * k), int(dist_from_center.y * k))
        draw_position = Vector2(WIN_CENTER.x + new_dist_from_center.x, WIN_CENTER.y + new_dist_from_center.y)

        pygame.draw.circle(screen, WHITE, (int(draw_position.x), int(draw_position.y)), radius)