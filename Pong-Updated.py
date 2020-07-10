import pygame
import sys
import random


# Working with sprites


class Block(pygame.sprite.Sprite):
    def __init__(self, path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))


# Three classes will inherit from Block class


class Player(Block):
    def __init__(self, path, pos_x, pos_y, paddle_speed):
        super().__init__(path, pos_x, pos_y)
        self.paddle_speed = paddle_speed
        self.movement = 0

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()


class Opponent(Block):
    def __init__(self, path, pos_x, pos_y, paddle_speed):
        super().__init__(path, pos_x, pos_y)
        self.paddle_speed = paddle_speed
        self.movement = 0

    def constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def update(self, ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.top += self.paddle_speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.bottom -= self.paddle_speed
        self.constrain()


class Ball(Block):
    def __init__(self, path, pos_x, pos_y, speed_x, speed_y, paddles):
        super().__init__(path, pos_x, pos_y)
        self.speed_x = speed_x * random.choice([1, -1])
        self.speed_y = speed_y * random.choice([1, -1])
        self.paddles = paddles
        self.ball_move = False
        self.score_time = 0

    def update(self):
        if self.ball_move:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.delay_reset_ball()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            pygame.mixer.Sound.play(pong_sound)
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            pygame.mixer.Sound.play(pong_sound)
            collided_paddle = pygame.sprite.spritecollide(self, self.paddles,
                                                          False)[0].rect
            if abs(self.rect.right - collided_paddle.left) < 10 and \
                    self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collided_paddle.right) < 10 and \
                    self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.bottom - collided_paddle.top) < 10 and \
                    self.speed_y > 0:
                self.speed_y *= -1
            if abs(self.rect.top - collided_paddle.bottom) < 10 and \
                    self.speed_y < 0:
                self.speed_y *= -1

    def reset(self):
        self.ball_move = False
        self.speed_x *= random.choice([1, -1])
        self.speed_y *= random.choice([1, -1])
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.mixer.Sound.play(score_sound)

    def delay_reset_ball(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.score_time >= 2100:
            self.ball_move = True


class GameManager:
    def __init__(self, ball_group, paddles):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddles

    def run_game(self):
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset()
        self.draw_score()

    def reset(self):
        if self.ball_group.sprite.rect.left <= 0:
            # Player Score
            self.player_score += 1
            self.ball_group.sprite.reset()
        if self.ball_group.sprite.rect.right >= SCREEN_WIDTH:
            # Opponent Score
            self.opponent_score += 1
            self.ball_group.sprite.reset()

    def draw_score(self):
        player_score_text = SCORE_FONT.render(str(self.player_score), 1, WHITE)
        opponent_score_text = SCORE_FONT.render(str(self.opponent_score), 1, WHITE)

        player_score_rect = player_score_text.get_rect(topleft=(3*SCREEN_WIDTH // 4, 40))
        opponent_score_rect = opponent_score_text.get_rect(topleft=(SCREEN_WIDTH // 4, 40))

        screen.blit(player_score_text, player_score_rect)
        screen.blit(opponent_score_text, opponent_score_rect)


# Initialize Game and Window

pygame.mixer.pre_init(44100, -16, 512)
pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 680
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PONG")

# Game Objects
player = Player("Pong Paddle.png", SCREEN_WIDTH-20, SCREEN_HEIGHT//2, 8)
opponent = Opponent("Pong Paddle.png", 10, SCREEN_HEIGHT//2, 8)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)
ball = Ball("Pong Ball.png", SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 6, 6, paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

# Text and Scores
player_score = 0
SCORE_FONT = pygame.font.Font("bit5x3.ttf", 50)
opponent_score = 0

# Colours
bg_colour = pygame.Color('grey12')
LIGHT_GREY = (200, 200, 200)
WHITE = (255, 255, 255)
middle_line = pygame.Rect((SCREEN_WIDTH//2 - 1, 0), (2, SCREEN_HEIGHT))

# Timer
score_time = 1

# Sound

pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

game_manager = GameManager(ball_sprite, paddle_group)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Reading up and down arrow input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.movement += player.paddle_speed
            if event.key == pygame.K_UP:
                player.movement -= player.paddle_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player.movement -= player.paddle_speed
            if event.key == pygame.K_UP:
                player.movement += player.paddle_speed
    # Drawing
    screen.fill(bg_colour)
    pygame.draw.rect(screen, LIGHT_GREY, middle_line)

    # Run Game

    game_manager.run_game()

    # Render Display

    pygame.display.flip()
    clock.tick(60)
