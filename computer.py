import pygame
import numpy as np
from pygame.math import Vector2, Vector3
from settings import *


class Computer(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.color = GRAY
        self.score = 0
        self.width, self.height = WIN_WIDTH, WIN_HEIGHT
        self.racket_height = 150
        self.racket_width = 150
        self.movement_speed = 9
        self.image = pygame.Surface([self.racket_width, self.racket_height])
        self.image.fill(self.color)
        self.position = Vector3(WIN_WIDTH // 2, WIN_HEIGHT // 2, WIN_DEPTH)
        self.rect = self.image.get_rect(topleft=(self.position.x, self.position.y))
        self.is_green = False
        self.recent_hit = False

    def move_up(self):
        if self.position.y > 0:
            self.position.y -= self.movement_speed
            self.rect.top = self.position.y

    def move_down(self):
        if self.position.y + self.racket_height < self.height:
            self.position.y += self.movement_speed
            self.rect.top = self.position.y

    def move_left(self):
        if self.position.x > 0:
            self.position.x -= self.movement_speed
            self.rect.left = self.position.x

    def move_right(self):
        if self.position.x + self.racket_width < self.width:
            self.position.x += self.movement_speed
            self.rect.left = self.position.x

    def move_to_middle(self):
        paddle_center = Vector2(self.position.x + self.racket_width // 2, self.position.y + self.racket_height // 2)
        tolerance = 10

        in_middle_x = abs(paddle_center.x - WIN_CENTER.x) < tolerance
        in_middle_y = abs(paddle_center.y - WIN_CENTER.y) < tolerance

        if not in_middle_x:
            if paddle_center.x > WIN_CENTER.x:
                self.move_left()
            else:
                self.move_right()

        if not in_middle_y:
            if paddle_center.y < WIN_CENTER.y:
                self.move_down()
            else:
                self.move_up()

    def move(self, ball_position, ball_zdirection):
        paddle_center = Vector2(self.position.x + self.racket_width // 2, self.position.y + self.racket_height // 2)

        if ball_zdirection < 0:
            self.move_to_middle()
        else:
            if paddle_center.x < ball_position.x:
                self.move_right()
            else:
                self.move_left()
            if paddle_center.y < ball_position.y:
                self.move_down()
            else:
                self.move_up()

    def draw(self, screen):
        paddle_center = Vector2(self.position.x + self.racket_width // 2, self.position.y + self.racket_height // 2)
        dist_from_center = Vector2(paddle_center.x - WIN_CENTER.x, paddle_center.y - WIN_CENTER.y)
        size = Vector2(int(DEPTH_RATIO * self.racket_width), int(DEPTH_RATIO * self.racket_height))

        new_dist_from_center = Vector2(int(dist_from_center.x * DEPTH_RATIO), int(dist_from_center.y * DEPTH_RATIO))
        draw_position = Vector2(WIN_CENTER.x + new_dist_from_center.x - size.x // 2, 
                                WIN_CENTER.y + new_dist_from_center.y - size.y // 2)

        draw_image = pygame.Surface([size.x, size.y])
        draw_image.fill(GRAY)
        draw_rect = draw_image.get_rect(topleft=(draw_position.x, draw_position.y))
        screen.blit(draw_image, draw_rect)

    def toggle_color(self):
        self.color = GRAY if self.is_green else GREEN