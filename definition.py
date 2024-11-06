import pygame
import random
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # For sound effects

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Paddle properties
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 7

# Ball properties
BALL_RADIUS = 10
BALL_SPEED_X = 3
BALL_SPEED_Y = -3

# Brick properties
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_ROWS = 5
BRICK_COLS = 8

# Game properties
score = 0
lives = 3
level = 1

# Power-Up properties
POWERUP_SIZE = 20
powerup_types = ["expand", "shrink", "slow", "fast"]

# Load sounds
hit_sound = pygame.mixer.Sound('hit.wav')
break_sound = pygame.mixer.Sound('break.wav')
powerup_sound = pygame.mixer.Sound('powerup.wav')

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Brick Breaker")

# Create paddle
paddle = pygame.Rect((SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 50), (PADDLE_WIDTH, PADDLE_HEIGHT))

# Create ball
ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]