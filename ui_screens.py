import pygame

from settings import SCREEN_WIDTH, UI_HEIGHT, UI_FONT_SIZE, UI_COLOR, SCREEN_HEIGHT


def draw_ui(screen, score, lives, level, font, font_color, bg_color):
    # Draw a background for the UI
    pygame.draw.rect(screen, bg_color, (0, 0, SCREEN_WIDTH, UI_HEIGHT))  # Dynamic background color

    # Render score, lives, and level with the given font and color
    score_text = font.render(f"Score: {str(score)}", True, font_color)
    lives_text = font.render(f"Lives: {str(lives)}", True, font_color)
    level_text = font.render(f"Level: {str(level)}", True, font_color)

    # Draw UI elements on the screen
    screen.blit(score_text, (10, 10))  # Left-align score
    screen.blit(lives_text, (SCREEN_WIDTH // 2 - 50, 10))  # Center-align lives
    screen.blit(level_text, (SCREEN_WIDTH - 150, 10))  # Right-align level



def welcome_screen(screen):
    # Fonts and colors
    title_font = pygame.font.Font(None, 72)
    options_font = pygame.font.Font(None, 36)
    title_color = (255, 255, 255)  # White text
    bg_color = (0, 0, 0)  # Black background

    # Render title and options
    title_text = title_font.render("Brick Breaker", True, title_color)
    start_text = options_font.render("Press ENTER to Start", True, title_color)
    instructions_text = options_font.render("Press I for Instructions", True, title_color)

    # Display the welcome screen
    screen.fill(bg_color)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 300))
    screen.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, 350))
    pygame.display.flip()

    # Wait for player input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start the game
                    waiting = False
                elif event.key == pygame.K_i:  # Show instructions
                    instructions_screen(screen)

def instructions_screen(screen):
    # Fonts and colors
    font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)  # White text
    bg_color = (0, 0, 0)  # Black background

    # Instructions content
    instructions = [
        "Welcome to Brick Breaker!",
        "Instructions:",
        "- Move the paddle with the Left and Right arrow keys.",
        "- Bounce the ball to break all the bricks.",
        "- Collect power-ups for an advantage.",
        "- Press P to Pause the game.",
        "Press ENTER to return to the main menu.",
    ]

    # Display instructions
    screen.fill(bg_color)
    for i, line in enumerate(instructions):
        text = font.render(line, True, text_color)
        screen.blit(text, (50, 100 + i * 50))
    pygame.display.flip()

    # Wait for player input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

    # Clear lingering keypress events
    pygame.event.clear()

    # Return control to the main logic
    return

def pause_menu(screen):
    pygame.mixer.music.pause()
    font = pygame.font.Font(None, 72)
    pause_text = font.render("Paused", True, (255, 255, 255))
    resume_text = pygame.font.Font(None, 36).render(
        "Press P to Resume or Q to Quit", True, (255, 255, 255)
    )

    screen.fill((0, 0, 0))
    screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 150))
    screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, 300))
    pygame.display.flip()

    # Wait for player input
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Resume game
                    paused = False
                elif event.key == pygame.K_q:  # Quit game
                    pygame.quit()
                    exit()

    # Unpause the music
    pygame.mixer.music.unpause()

    # Clear lingering keypress events
    pygame.event.clear()

def game_over_screen(screen, score):
    pygame.mixer.music.stop()

    # Play game over sound
    game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.wav")
    game_over_sound.play()

    font = pygame.font.Font(None, 72)
    text = font.render("GAME OVER", True, (255, 0, 0))
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))

    # Center the text
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    screen.fill((0, 0, 0))  # Black background
    screen.blit(text, text_rect)
    screen.blit(score_text, score_rect)
    pygame.display.flip()

    # Wait for the player to quit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False

def you_win_screen(screen, score):
    pygame.mixer.music.stop()

    # Play you win sound
    you_win_sound = pygame.mixer.Sound("assets/sounds/you_win.wav")
    you_win_sound.play()

    font = pygame.font.Font(None, 72)
    win_text = font.render("YOU WIN!", True, (0, 255, 0))  # Green text
    score_text = pygame.font.Font(None, 36).render(f"Final Score: {score}", True, (255, 255, 255))

    # Center the text
    win_text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    screen.fill((0, 0, 0))  # Black background
    screen.blit(win_text, win_text_rect)
    screen.blit(score_text, score_text_rect)
    pygame.display.flip()

    # Wait for the player to quit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
