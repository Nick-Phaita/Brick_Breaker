import pygame
import random


from objects import Paddle, Ball, Brick
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BACKGROUND_COLOR,
    FPS,
    BRICK_WIDTH,
    BRICK_HEIGHT,
    BRICK_PADDING,
    BRICK_COLUMNS, BRICK_START_Y, BRICK_ROWS, TOTAL_LEVELS, themes, LEVEL_CONFIG, SCREEN_PADDING, UI_FONT_SIZE
)
from ui_screens import draw_ui, welcome_screen, game_over_screen, you_win_screen, pause_menu

# Initial values to reset power-ups
INITIAL_PADDLE_WIDTH = 100
INITIAL_BALL_SPEED = (4, -4)


def create_brick_grid(rows, theme_name):
    theme = themes[theme_name]
    brick_colors = theme["brick_colors"]
    brick_texture = theme.get("brick_texture")
    bricks = [
        Brick(
            x * (BRICK_WIDTH + BRICK_PADDING) + SCREEN_PADDING,
            y * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_START_Y,
            random.choice(brick_colors),
            brick_texture
        )
        for x in range(BRICK_COLUMNS) for y in range(rows)
    ]
    return bricks


def tint_texture(texture, color):
    """
    Tints a texture with a specific color.

    Args:
        texture (pygame.Surface): The base texture.
        color (tuple): RGB color to apply as a tint.

    Returns:
        pygame.Surface: A tinted texture.
    """

    tinted_texture = pygame.Surface(texture.get_size(), flags=pygame.SRCALPHA)
    tinted_texture.fill(color)  # Fill the surface with the tint color
    texture = texture.copy()
    texture.blit(tinted_texture, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return texture


def apply_theme(theme_name, paddle, ball, bricks, screen):
    theme = themes[theme_name]

    #paddle.base_texture = pygame.image.load(theme["paddle_texture"]).convert_alpha()
    #paddle.texture = tint_texture(paddle.base_texture, theme["paddle_color"])

    if "background" in theme:
        background_image = pygame.image.load(theme["background"])
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background_image, (0, 0))  # Draw the background image
    paddle.color = theme["paddle_color"]
    ball.color = theme["ball_color"]

    # Load UI properties
    global current_ui_font, current_ui_font_color, current_ui_bg_color
    current_ui_font = pygame.font.Font(theme["ui_font"], UI_FONT_SIZE)
    current_ui_font_color = theme["ui_font_color"]
    current_ui_bg_color = theme["ui_bg_color"]




def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Brick Breaker")
    clock = pygame.time.Clock()

    # Show the welcome screen
    welcome_screen(screen)

    # Create game objects
    paddle = Paddle()
    ball = Ball()
    current_level = 1 # Start with the first level (1-indexed for better readability)
    level_config = LEVEL_CONFIG[current_level]  # Fetch the configuration for the current level
    bricks = create_brick_grid(level_config["rows"], level_config["theme"])  # Pass rows and theme to create the grid
    # Apply the theme to the game objects

    score = 0
    lives = 3
    level = 1

    power_ups = []
    particles = []
    power_up_timers = {"expand": 0, "shrink": 0, "slow": 0, "fast": 0}

    pygame.mixer.init()
    hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
    break_sound = pygame.mixer.Sound("assets/sounds/break.wav")
    powerup_sound = pygame.mixer.Sound("assets/sounds/powerup.wav")


    # Default values (fallbacks)

    pygame.mixer.music.load(level_config["music"])
    pygame.mixer.music.play(-1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:  # Pause menu
                pause_menu(screen)

        # Handle input
        keys = pygame.key.get_pressed()
        paddle.move(keys)
        ball.move()

        # Check collisions
        if ball.check_paddle_collision(paddle):
            hit_sound.play()

        #particles = []  # Initialize particles


        # Check brick collisions and update score
        if ball.check_brick_collision(bricks, power_ups, particles):
            break_sound.play()
            score += 10  # Increment score for each brick hit



        # Check if all bricks are cleared
        if all(not brick.visible for brick in bricks):  # All bricks cleared
            current_level += 1
            if current_level > TOTAL_LEVELS:
                you_win_screen(screen, score)
                running = False
            else:
                level_config = LEVEL_CONFIG[current_level]
                bricks = create_brick_grid(level_config["rows"], level_config["theme"])
                ball.reset_speed()
                ball.reset_position()

                pygame.mixer.music.load(level_config["music"])
                pygame.mixer.music.play(-1)



        # Check if ball falls below paddle
        if ball.y - ball.radius > SCREEN_HEIGHT:  # Ball fell below paddle
            lives -= 1
            if lives == 0:
                game_over_screen(screen, score)
                running = False  # End the game
            else:
                ball.reset_position()
                ball.reset_speed()

        # Draw everything
        apply_theme(level_config["theme"], paddle, ball, bricks, screen)
        draw_ui(screen, score, lives, current_level, current_ui_font, current_ui_font_color, current_ui_bg_color)
        paddle.draw(screen)
        ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)

        # Update and draw power-ups
        for power_up in power_ups[:]:
            if power_up.active:
                power_up.move()

                # Check if power-up falls below the screen
                if power_up.y > SCREEN_HEIGHT:
                    power_up.active = False  # Mark as inactive when off-screen

                power_up.draw(screen)

                if power_up.check_collision(paddle):
                    powerup_sound.play()
                    if power_up.type == "expand":
                        paddle.width += 40
                    elif power_up.type == "shrink":
                        paddle.width = max(40, paddle.width - 40)
                    elif power_up.type == "slow":
                        ball.dx *= 0.9
                        ball.dy *= 0.9
                    elif power_up.type == "fast":
                        ball.dx *= 1.1
                        ball.dy *= 1.1
                    power_up_timers[power_up.type] = FPS * 5
                    power_up.active = False

        # Safely remove inactive power-ups
        power_ups[:] = [power_up for power_up in power_ups if power_up.active]

        # Safely remove inactive power-ups
        power_ups[:] = [power_up for power_up in power_ups if power_up.active]

        # Reset power-up effects after duration
        for effect, timer in power_up_timers.items():
            if timer > 0:
                power_up_timers[effect] -= 1
                if power_up_timers[effect] == 0:
                    if effect in ["expand", "shrink"]:
                        paddle.width = INITIAL_PADDLE_WIDTH
                    elif effect in ["slow", "fast"]:
                        ball.dx, ball.dy = INITIAL_BALL_SPEED

        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        #print("Number of particles:", len(particles))  # Check if particles exist


        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
