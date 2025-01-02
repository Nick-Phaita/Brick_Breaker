# Game settings
TOTAL_LEVELS = 5  # Define the total number of levels

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)  # Black background

# Paddle settings
PADDLE_COLOR = (255, 255, 255)  # White paddle
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_SPEED = 10
PADDLE_MIN_WIDTH = 40
PADDLE_EXPAND_AMOUNT = 40

# Ball settings
BALL_COLOR = (255, 255, 0)  # Yellow ball
BALL_RADIUS = 10
BALL_INITIAL_SPEED = 4

# Brick settings
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
BRICK_PADDING = 10
SCREEN_PADDING = 15  # Space from the edges of the screen
UI_HEIGHT = 50  # Space at the top reserved for the UI
PLAY_AREA_HEIGHT = SCREEN_HEIGHT - UI_HEIGHT  # Height of the play area
BRICK_ROWS = 5
BRICK_COLUMNS = (SCREEN_WIDTH - 2 * SCREEN_PADDING) // (BRICK_WIDTH + BRICK_PADDING)
BRICK_START_Y = UI_HEIGHT + 10
BRICK_POWER_UP_CHANCE = 0.2  # 20% chance to drop a power-up
BRICK_COLOR = (200, 0, 0)

# Power-up settings
POWER_UP_WIDTH = 20
POWER_UP_HEIGHT = 20
POWER_UP_SPEED = 3
POWER_UP_DURATION = 5  # In seconds

# UI settings
UI_FONT_SIZE = 28
UI_COLOR = (255, 255, 255)  # White text


LEVEL_CONFIG = {
    1: {"rows": 4, "theme": "minimalistic", "music" : "assets/music/level1.mp3"},
    2: {"rows": 4, "theme": "candy_land", "music" : "assets/music/level2.mp3"},
    3: {"rows": 5, "theme": "retro_neon", "music" : "assets/music/level3.mp3"},
    4: {"rows": 5, "theme": "cyberpunk", "music" : "assets/music/level4.mp3"},
    5: {"rows": 6, "theme": "lava", "music" : "assets/music/level5.mp3"},
}


themes = {
    "minimalistic": {
        "background": "assets/backgrounds/minimalist.png",  # White background
        "brick_colors": [(92, 92, 92), (160, 160, 160), (211, 211, 211)],  # Grayscale bricks
        "paddle_color": (0, 0, 0),  # Black paddle
        "ball_color": (255, 106, 0),
        "ui_font_color": (0, 0, 0),  # Black for minimalist theme
        "ui_bg_color": (230, 230, 230),
        "ui_font": "assets/fonts/minimalist_font.otf",
        "paddle_texture" : "assets/textures/lava_ball.png",

    },
    "candy_land": {
        "background": "assets/backgrounds/candy_land.jpg",  # Light pink
        "brick_colors": [
            (255, 20, 147),  # Hot Pink
            (0, 255, 255),   # Bright Cyan
            (255, 255, 0),   # Bright Yellow
            (148, 0, 211),   # Electric Purple
        ],
        "paddle_color": (255, 0, 255),  # Bright Magenta
        "ball_color": (0, 255, 0), # White paddle
        "ui_font_color": (255, 20, 147),  # Bright pink
        "ui_bg_color": (255, 228, 225),  # Light pink background
        "ui_font": "assets/fonts/candy_font.ttf",

    },
    "retro_neon": {
        "background": "assets/backgrounds/retro_land.jpg",  # Black background
        "brick_colors": [
            (57, 255, 20),    # Neon Green
            (155, 48, 255),   # Neon Purple
            (0, 255, 255),    # Bright Cyan
            (255, 105, 180),  # Electric Pink
        ],
        "paddle_color": (0, 255, 255),  # Electric Cyan
        "ball_color": (255, 20, 147),  # Neon green paddle
        "ui_font_color": (0, 255, 255),  # Neon cyan
        "ui_bg_color": (10, 10, 30),  # Dark background
        "ui_font": "assets/fonts/retro_font.ttf",  # Retro neon font

    },
    "cyberpunk": {
        "background": "assets/backgrounds/cyberpunk.jpg",  # Deep purple (cyberpunk vibe)
        "brick_colors": [
            (255, 50, 50),   # Neon Red
            (0, 255, 255),   # Bright Cyan
            (150, 0, 255),   # Electric Purple
            (255, 255, 0),   # Bright Yellow
        ],
        "paddle_color": (255, 0, 255),
        "ball_color": (57, 255, 20),
        "ui_font_color": (255, 0, 255),  # Magenta for cyberpunk
        "ui_bg_color": (30, 0, 60),
        "ui_font": "assets/fonts/cyberpunk_font.ttf",  # Cyberpunk font

    },
    "lava": {
        "background": "assets/backgrounds/lava_land.jpg",  # Black background
        "brick_colors": [
            (255, 50, 50),   # Bright Red
            (255, 85, 0),    # Deep Orange
            (255, 200, 0),   # Fiery Yellow
            (70, 70, 70),    # Charcoal Gray
        ],
        "paddle_color": (50, 0, 0),  # Molten Orange
        "ball_color": (255, 223, 0),   # Bright Yellow
        "ui_font_color": (255, 69, 0),  # Fiery orange
        "ui_bg_color": (50, 0, 0),
        "ui_font": "assets/fonts/lava_font.ttf",  # Lava-themed font
        "paddle_texture" : "assets/textures/lava_ball.png",

    },
}




