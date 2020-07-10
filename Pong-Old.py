import pygame
import sys
import random


def ball_animations():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        # Player Score
        if ball.left <= 0:
            player_score += 1
            pygame.mixer.Sound.play(score_sound)
        else:
            # Opponent Score
            opponent_score += 1
            pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            pygame.mixer.Sound.play(pong_sound)
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            pygame.mixer.Sound.play(pong_sound)
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            pygame.mixer.Sound.play(pong_sound)
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        if abs(ball.left - opponent.right) < 10:
            pygame.mixer.Sound.play(pong_sound)
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            pygame.mixer.Sound.play(pong_sound)
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            pygame.mixer.Sound.play(pong_sound)
            ball_speed_y *= -1


def player_animations(speed):
    player.y += speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT


def opponent_movement(opp_speed):
    if opponent.top < ball.y:
        opponent.top += opp_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opp_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= SCREEN_HEIGHT:
        opponent.bottom = SCREEN_HEIGHT


def ball_restart():
    global ball_speed_x, ball_speed_y, score_time
    current_time = pygame.time.get_ticks()
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    if current_time - score_time < 2000:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_x = 7 * random.choice([1, -1])
        ball_speed_y = 7 * random.choice([1, -1])
        score_time = None


# Initialize Game and Window
pygame.mixer.pre_init(44100, -16, 512)
pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 680
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PONG")

# Game Objects
BALL_WIDTH = 30
BALL_HEIGHT = 30
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_WIDTH // 2,
                   SCREEN_HEIGHT // 2 - BALL_HEIGHT // 2, BALL_WIDTH,
                   BALL_HEIGHT)
player = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2 - 70, 10, 140)
opponent = pygame.Rect(10, SCREEN_HEIGHT // 2 - 70, 10, 140)
ball_speed_x = 7 * random.choice([1, -1])
ball_speed_y = 7 * random.choice([1, -1])
player_speed = 0
opponent_speed = 7

# Text and Scores
player_score = 0
SCORE_FONT = pygame.font.Font("bit5x3.ttf", 50)
opponent_score = 0

# Colours
bg_colour = pygame.Color('grey12')
LIGHT_GREY = (200, 200, 200)
WHITE = (255, 255, 255)

# Timer
score_time = 1

# Sound

pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Reading up and down arrow input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7
    ball_animations()
    player_animations(player_speed)
    opponent_movement(opponent_speed)
    # Drawing
    screen.fill(bg_colour)
    pygame.draw.rect(screen, LIGHT_GREY, player)
    pygame.draw.rect(screen, LIGHT_GREY, opponent)
    pygame.draw.ellipse(screen, LIGHT_GREY, ball)
    pygame.draw.aaline(screen, LIGHT_GREY, (SCREEN_WIDTH // 2, 0),
                       (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    if score_time is not None:
        ball_restart()

    text = SCORE_FONT.render(str(player_score), 1, WHITE)
    text2 = SCORE_FONT.render(str(opponent_score), 1, WHITE)
    screen.blit(text2, (SCREEN_WIDTH // 4, 40))
    screen.blit(text, (3 * SCREEN_WIDTH // 4, 40))

    pygame.display.flip()
    clock.tick(60)
