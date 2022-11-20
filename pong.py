import random
import pygame
import time
import numpy as np
from pygame.math import Vector2, Vector3
from find_hand import FindHand
from player import Player
from computer import Computer
from settings import *


hand = FindHand()
pygame.init()

FONT = pygame.font.SysFont('Helvetica', 25)


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


def game_over(screen, message, left_paper, right_player):
    gray_overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    gray_overlay.fill(GRAY)
    gray_overlay.set_colorkey(GRAY)
    pygame.draw.rect(gray_overlay, BLACK, [0, 0, WIN_WIDTH, WIN_HEIGHT])
    gray_overlay.set_alpha(99)
    screen.blit(gray_overlay, (0, 0))
    font = pygame.font.SysFont(None, 100)
    game_over = font.render(message, True, WHITE)
    screen.blit(game_over, (WIN_WIDTH / 2 - 300, WIN_HEIGHT / 2 - 100))
    scoreline = font.render(
        '{} - {}'.format(left_paper.score, right_player.score), True, WHITE)
    screen.blit(scoreline, (WIN_WIDTH / 2 - 50, WIN_HEIGHT / 2 + 100))
    pygame.display.update()
    pygame.time.delay(2000)
    main()


def render_score(player, computer, font):
    """Render player scores onto surfaces."""
    player_score = font.render(str(player.score), True, (255, 255, 255))
    computer_score = font.render(str(computer.score), True, (255, 255, 255))
    return player_score, computer_score


def paddle_hit(paddle, ball, time_elapsed):
    in_paddle_xrange = ball.position.x > int(paddle.position.x) - 4 and \
        ball.position.x < int(paddle.position.x) + paddle.racket_width + 4
    in_paddle_yrange = ball.position.y > int(paddle.position.y) - 4 and \
        ball.position.y < int(paddle.position.y) + paddle.racket_height + 4

    in_paddle_zrange = abs(ball.position.z - paddle.position.z) < 50
    paddle.recent_hit = time_elapsed < 0.5

    hit = in_paddle_xrange and in_paddle_yrange and in_paddle_zrange and not paddle.recent_hit
    if hit:
        paddle.toggle_color()

    return hit


def drawBackground(screen, ball_depth):
    # Calculates marker positions
    depth = ball_depth / WIN_DEPTH
    left_marker_x = depth * ((WIN_WIDTH - BACK_WIN_WIDTH) // 2)
    right_marker_x = WIN_WIDTH - left_marker_x
    marker_top_y = depth * ((WIN_HEIGHT - BACK_WIN_HEIGHT) // 2)
    marker_bottom_y = WIN_HEIGHT - marker_top_y
    marker_width = int((1 - depth) * 6) + 1

    # Draws ball depth markers
    pygame.draw.line(screen, RED, [left_marker_x, marker_top_y], [left_marker_x, marker_bottom_y], marker_width)
    pygame.draw.line(screen, RED, [right_marker_x, marker_top_y], [right_marker_x, marker_bottom_y], marker_width)

    # Draws background lines
    pygame.draw.line(screen, BLACK, POINT_1, POINT_5, 3)  # Top left diagonal
    pygame.draw.line(screen, BLACK, POINT_2, POINT_6, 3)  # Top right diagonal
    pygame.draw.line(screen, BLACK, POINT_3, POINT_7, 3)  # Bottom left diagonal
    pygame.draw.line(screen, BLACK, POINT_4, POINT_8, 3)  # Bottom right diagonal
    pygame.draw.line(screen, BLACK, POINT_5, POINT_6, 2)  # Next four commands build the inner rectangle
    pygame.draw.line(screen, BLACK, POINT_6, POINT_8, 2)
    pygame.draw.line(screen, BLACK, POINT_7, POINT_5, 2)
    pygame.draw.line(screen, BLACK, POINT_8, POINT_7, 2)


def main():
    screen = pygame.display.set_mode(DISPLAY, 0, 32)
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    last_hit_time = 0

    # Creates game objects
    player = Player()
    computer = Computer()
    curr_ball = Ball()

    all_sprites = pygame.sprite.Group(player, computer, curr_ball)

    # Displays score
    goal_text = FONT.render(str(MAX_SCORE), True, (255, 255, 0))
    player_score, computer_score = render_score(player, computer, FONT)

    player_recent_hit = False
    computer_recent_hit = False
    done = False

    # Main game loop
    while not done:
        # Event handling.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Registers if the user presses 'q' to quit the game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            done = True

        """
        # Moves the player and computer
        mx, my, = pygame.mouse.get_pos()
        player.move(mx, my)
        """
        player.move(hand)
        computer.move(curr_ball.position, curr_ball.direction.z)

        # Game logic.
        all_sprites.update()
        # Determine winner.
        if player.score >= MAX_SCORE or computer.score >= MAX_SCORE:
            # This is a conditional expression (similar
            # to a ternary in other languages).
            message = 'You Win!' if player.score > computer.score else 'Computer Wins!'
            game_over(screen, message, player, computer)
            done = True

        # Collision detection with the rackets/players.
        time_elapsed = time.process_time() - last_hit_time
        col_player = paddle_hit(player, curr_ball, time_elapsed)
        col_computer = paddle_hit(computer, curr_ball, time_elapsed)

        if player_recent_hit is True and not player.recent_hit:
            player.toggle_color()
            player_recent_hit = False
        if computer_recent_hit is True and not computer.recent_hit:
            computer.toggle_color()
            player_recent_hit = False

        if col_player or col_computer:
            curr_ball.direction.z *= -1  # Reverse the z component of the vector.
            curr_ball.hit()
            last_hit_time = time.process_time()

        if curr_ball.position.z <= 0:  # front wall
            computer.score += 1
            curr_ball.initialize()
            player_score, computer_score = render_score(
                player, computer, FONT)
        elif curr_ball.position.z >= WIN_DEPTH:  # back wall
            player.score += 1
            curr_ball.initialize()
            player_score, computer_score = render_score(
                player, computer, FONT)

        # Drawing
        screen.fill((60, 60, 140))
        screen.blit(player_score, (WIN_CENTER.x - 100, 10))
        screen.blit(computer_score, (WIN_CENTER.x + 100, 10))
        screen.blit(goal_text, (WIN_CENTER.x, 0))
        drawBackground(screen, curr_ball.position.z)
        # all_sprites.draw(screen)

        player.draw(screen)
        computer.draw(screen)
        curr_ball.draw(screen)

        pygame.display.set_caption("3-D Pong")

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
    pygame.quit()
