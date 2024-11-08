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


# Create bricks
def create_bricks():
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            brick_x = col * (BRICK_WIDTH + 10) + 35
            brick_y = row * (BRICK_HEIGHT + 10) + 35
            brick = pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)
            bricks.append(brick)
    return bricks


bricks = create_bricks()
powerups = []


# Function to draw objects
def draw_objects():
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, RED, ball)
    for brick in bricks:
        pygame.draw.rect(screen, WHITE, brick)
    for powerup, _ in powerups:
        pygame.draw.rect(screen, YELLOW, powerup)

    # Display score, lives, and level
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))
    screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, 10))
    pygame.display.flip()

# Function to display Game Over message
def display_game_over():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.right += PADDLE_SPEED

    # Ball movement
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball collision with walls
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_speed[0] = -ball_speed[0]
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]

    # Ball collision with paddle
    if ball.colliderect(paddle):
        hit_sound.play()
        # Adjust ball direction based on hit location on paddle
        offset = (ball.centerx - paddle.centerx) / (PADDLE_WIDTH // 2)
        ball_speed[0] = BALL_SPEED_X * offset
        ball_speed[1] = -abs(ball_speed[1])

    # Ball collision with bricks
    hit_index = ball.collidelist(bricks)
    if hit_index != -1:
        brick = bricks.pop(hit_index)
        break_sound.play()
        ball_speed[1] = -ball_speed[1]
        score += 10
        if random.random() < 0.2:  # Random chance of a powerup
            powerup = pygame.Rect(brick.x, brick.y, POWERUP_SIZE, POWERUP_SIZE)
            powerups.append((powerup, random.choice(powerup_types)))

    # Ball out of bounds
    if ball.bottom >= SCREEN_HEIGHT:
        lives -= 1
        ball.x, ball.y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        if lives == 0:
            display_game_over()  # Display Game Over message
            pygame.time.delay(2000)  # Delay to show Game Over screen for 2 seconds
            running = False

    # Handle powerup falling
    for powerup in powerups[:]:
        powerup[0].y += 3
        if powerup[0].colliderect(paddle):
            powerup_sound.play()
            powerup_type = powerup[1]
            if powerup_type == "expand":
                paddle.width += 20
            elif powerup_type == "shrink":
                paddle.width = max(paddle.width - 20, 50)
            elif powerup_type == "slow":
                ball_speed[0] = max(1, ball_speed[0] - 1)
                ball_speed[1] = max(1, ball_speed[1] - 1)
            elif powerup_type == "fast":
                ball_speed[0] += 1
                ball_speed[1] += 1
            powerups.remove(powerup)

    # Next level if all bricks are cleared
    if not bricks:
        level += 1
        ball_speed[0] += 1 if ball_speed[0] > 0 else -1  # Increase speed while keeping the same direction
        ball_speed[1] = abs(ball_speed[1]) + 1  # Ensure the ball moves downward at the start of the level
        ball.x, ball.y = SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2  # Reset ball position to center
        bricks = create_bricks()

    # Draw everything
    draw_objects()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()