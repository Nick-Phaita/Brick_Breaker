import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, PADDLE_COLOR, BALL_COLOR, BRICK_COLOR, POWER_UP_WIDTH, \
    POWER_UP_HEIGHT, POWER_UP_SPEED, PADDLE_HEIGHT, PADDLE_SPEED, BALL_RADIUS, BALL_INITIAL_SPEED, PADDLE_WIDTH, \
    BRICK_WIDTH, BRICK_HEIGHT


class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.color = PADDLE_COLOR
        self.texture = None
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - self.height - 10
        self.speed = PADDLE_SPEED

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def draw(self, screen):
        if hasattr(self, 'texture') and self.texture:
            screen.blit(pygame.transform.scale(self.texture, (self.width, self.height)), (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Draw border
        pygame.draw.rect(
            screen,
            (0, 0, 0),  # Black border
            (self.x, self.y, self.width, self.height),
            2  # Border thickness
        )


class Ball:
    def __init__(self):
        self.radius = BALL_RADIUS
        self.color = BALL_COLOR
        self.texture = None
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.dx = BALL_INITIAL_SPEED
        self.dy = -BALL_INITIAL_SPEED

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Bounce off walls
        if self.x - self.radius < 0:
            self.x = self.radius  # Reset position to the left boundary
            self.dx *= -1

        if self.x + self.radius > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius  # Reset position to the right boundary
            self.dx *= -1

        # Bounce off top boundary
        if self.y - self.radius <= 50:  # Use UI_HEIGHT as the top boundary
            self.dy *= -1

    def draw(self, screen):
        if self.texture:
            texture = pygame.image.load(self.texture)
            texture = pygame.transform.scale(texture, (self.radius * 2, self.radius * 2))
            screen.blit(texture, (self.x - self.radius, self.y - self.radius))
        else:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # Draw border
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius, 2)  # Black border

    def check_paddle_collision(self, paddle):
        # Predict the next position of the ball
        next_x = self.x + self.dx
        next_y = self.y + self.dy

        # Ball rectangle for predicted position
        ball_rect = pygame.Rect(next_x - self.radius, next_y - self.radius, self.radius * 2, self.radius * 2)

        # Paddle rectangle
        paddle_rect = pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height)

        if ball_rect.colliderect(paddle_rect):
            # Determine the overlap amounts to detect collision side
            overlap_top = abs(next_y + self.radius - paddle.y)
            overlap_left = abs(next_x + self.radius - paddle.x)
            overlap_right = abs(next_x - self.radius - (paddle.x + paddle.width))

            # Check if the ball hit the top of the paddle
            if overlap_top < overlap_left and overlap_top < overlap_right:
                self.dy = -abs(self.dy)  # Bounce the ball upward
                self.y = paddle.y - self.radius  # Position the ball just above the paddle

                # Adjust horizontal velocity based on where the ball hits the paddle
                paddle_center = paddle.x + paddle.width / 2
                distance_from_center = self.x - paddle_center
                self.dx += distance_from_center * 0.05  # Fine-tune the bounce angle
            elif overlap_left < overlap_right:
                # Ball hit the left edge of the paddle
                self.dx = -abs(self.dx)  # Reverse horizontal direction
                self.x = paddle.x - self.radius  # Position the ball left of the paddle
            elif overlap_right < overlap_left:
                # Ball hit the right edge of the paddle
                self.dx = abs(self.dx)  # Reverse horizontal direction
                self.x = paddle.x + paddle.width + self.radius  # Position the ball right of the paddle

            return True  # Collision detected

        return False  # No collision

    def check_brick_collision(self, bricks, power_ups, particles):
        for brick in bricks:
            if brick.visible and (
                    brick.x <= self.x <= brick.x + brick.width
                    and brick.y <= self.y <= brick.y + brick.height
            ):
                self.dy *= -1  # Reverse vertical direction
                if brick.power_up:
                    print(f"Power-Up '{brick.power_up}' created at ({brick.x}, {brick.y})")
                    # Spawn power-up at brick's position
                    power_ups.append(PowerUp(brick.x + brick.width // 2, brick.y, brick.power_up))
                for _ in range(5):  # Generate 5 particles
                    particle = Particle(brick.x + brick.width // 2, brick.y + brick.height // 2, brick.color)
                    particles.append(particle)
                    #print("Particle generated at:", brick.x, brick.y)

                brick.visible = False
                return True  # Indicate that a collision occurred
        return False

    def reset_position(self):
        """Reset the ball's position to the center of the screen."""
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2

    def reset_speed(self):
        """Reset the ball's speed to its initial values."""
        self.dx = 4
        self.dy = -4

class Brick:
    def __init__(self, x, y, color, texture=None):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.color = color
        self.texture = texture
        self.visible = True
        self.power_up = None  # Default no power-up

        # Assign a power-up with a 20% chance
        if random.random() < 0.2:
            self.power_up = random.choice(["expand", "shrink", "slow", "fast"])

    def draw(self, screen):
        if self.visible:
            if self.texture:
                # Draw brick texture
                texture = pygame.image.load(self.texture)
                texture = pygame.transform.scale(texture, (self.width, self.height))
                screen.blit(texture, (self.x, self.y))
            else:
                # Pulsate brightness for bricks
                glow = int((pygame.time.get_ticks() // 100) % 50)  # Animate brightness
                animated_color = (
                    min(self.color[0] + glow, 255),
                    min(self.color[1] + glow, 255),
                    min(self.color[2] + glow, 255),
                )
                # Draw brick color
                pygame.draw.rect(screen, animated_color, (self.x, self.y, self.width, self.height))

            # Draw the outline
            pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)

class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.color = (0, 255, 0) if type in ["expand", "shrink"] else (255, 0, 0)
        self.width = POWER_UP_WIDTH
        self.height = POWER_UP_HEIGHT
        self.speed = POWER_UP_SPEED
        self.active = True

    def move(self):
        self.y += self.speed  # Move power-up downward

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            # Add a glowing border effect
            glow_color = (255, 255, 0)  # Yellow glow
            pygame.draw.rect(
                screen,
                glow_color,
                (self.x - 2, self.y - 2, self.width + 4, self.height + 4),
                1  # Border thickness
            )

    def check_collision(self, paddle):
        # Check if the power-up intersects with the paddle
        if (
            self.y + self.height >= paddle.y
            and self.x + self.width >= paddle.x
            and self.x <= paddle.x + paddle.width
        ):
            self.active = False
            return True
        return False

class Particle:
    def __init__(self, x, y, color, lifetime=20):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)  # Make particles larger for testing
        self.lifetime = lifetime  # Increase lifetime

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.size, 1)

    def update(self):
        self.y += random.randint(-2, 2)  # Random motion
        self.x += random.randint(-2, 2)
        self.lifetime -= 1
