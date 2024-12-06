import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# -------------------- CONSTANTS --------------------
# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BREAKOUT GAME")
clock = pygame.time.Clock()

# Define the size of the falling obstacles
obstacle_width = 40  # Adjust the width as needed
obstacle_height = 40  # Adjust the height as needed

# Fonts
try:
    title_font = pygame.font.Font("arial.ttf", 80)
    sub_font = pygame.font.Font("arial.ttf", 40)
    hud_font = pygame.font.Font("arial.ttf", 30)
except FileNotFoundError:
    title_font = pygame.font.SysFont("arial", 80)
    sub_font = pygame.font.SysFont("arial", 40)
    hud_font = pygame.font.SysFont("arial", 30)

# Sounds
background_music = pygame.mixer.Sound("start.wav")
win_sound = pygame.mixer.Sound("win.wav")
lose_sound = pygame.mixer.Sound("lose.wav")

# Levels configuration
levels = {
    "easy": {"paddle_width": 150, "ball_speed": 5.5, "lives": 5},
    "intermediate": {"paddle_width": 120, "ball_speed": 6.5, "lives": 4},
    "hard": {"paddle_width": 100, "ball_speed": 7, "lives": 3, "time_limit": 60},
}

# Background music state
background_music_playing = False  # Initialize background music flag

# -------------------- GAME BUILD --------------------
# Ball and paddle properties
ball_radius = 8
ball_x, ball_y = 0, 0
ball_speed_x, ball_speed_y = 0, 0
ball_moving = False
paddle_speed= 30

# Initialize paddle and ball
paddle_x, paddle_y, paddle_width, paddle_height = 0, HEIGHT - 60, 150, 15

lives, score, current_level = 0, 0, None
blocks = []
phantom_blocks = []
time_remaining = 0

# Block properties
block_width = WIDTH // 10 - 5
block_height = 20

# Functions

def draw_text(text, font, color, x, y, centered=False):
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect()
    if centered:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(rendered_text, text_rect)

def create_blocks(level):
    blocks = []
    horizontal_gap = 4  # Horizontal gap between blocks
    vertical_gap = 4    # Vertical gap between rows

    # Adjust block size based on level
    if level == "easy":
        block_width = WIDTH // 6  # Larger blocks for easy (6 blocks horizontally)
        block_height = 40  # Larger height for easy
        rows = 4  # 4 rows of blocks
    elif level == "intermediate":
        block_width = WIDTH // 8  # Medium-sized blocks for intermediate (8 blocks horizontally)
        block_height = 30  # Medium height
        rows = 6  # 6 rows of blocks
    else:  # hard level
        block_width = WIDTH // 12  # Smaller blocks for hard (12 blocks horizontally)
        block_height = 20  # Smaller height for hard
        rows = 8  # 8 rows of blocks

    # Calculate the number of columns based on the width
    columns = WIDTH // block_width

    # Create the blocks and their positions
    for row in range(rows):
        for col in range(columns):
            x_pos = col * (block_width + horizontal_gap)  # Add horizontal gap
            y_pos = row * (block_height + vertical_gap)  # Add vertical gap
            block_rect = pygame.Rect(x_pos, y_pos, block_width, block_height)
            blocks.append({"rect": block_rect, "score": 10})  # Each block has a score value

    return blocks





def game_intro():
    global background_music_playing
    if not background_music_playing:
        background_music.play(-1)  # Loop the background music throughout the game
        background_music_playing = True  # Mark that the background music is playing

    screen.fill(BLACK)
    draw_text("BREAKOUT GAME", title_font, GREEN, WIDTH // 2, HEIGHT // 3, centered=True)
    draw_text("Press SPACE to Start", sub_font, WHITE, WIDTH // 2, HEIGHT // 2, centered=True)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False  # Proceed to the game loop

def level_selection():
    """Allow player to select game level."""
    global current_level, lives, paddle_width
    screen.fill(BLACK)
       draw_text("Choose a Level:", title_font, WHITE, WIDTH // 2, HEIGHT // 3, centered=True)
    draw_text("1 - Easy", sub_font, GREEN, WIDTH // 2, HEIGHT // 2, centered=True)
    draw_text("2 - Intermediate", sub_font, GREEN, WIDTH // 2, HEIGHT // 2 + 50, centered=True)
    draw_text("3 - Hard", sub_font, GREEN, WIDTH // 2, HEIGHT // 2 + 100, centered=True)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_level = "easy"
                elif event.key == pygame.K_2:
                    current_level = "intermediate"
                elif event.key == pygame.K_3:
                    current_level = "hard"
                if current_level:
                    lives = levels[current_level]["lives"]
                    paddle_width = levels[current_level]["paddle_width"]
                    return

def game_over(won=False, score=0):
    """Display game over screen and handle retry logic."""
    global background_music_playing
    pygame.mixer.Sound.stop(background_music )
    pygame.mixer.Sound.play(win_sound if won else lose_sound)
    screen.fill(BLACK)

    if won:
        draw_text("YOU WON!", title_font, GREEN, WIDTH // 2, HEIGHT // 3, centered=True)
        win_loop()
        # Confetti effect or animation goes here
    else:
        draw_text("YOU LOST", title_font, WHITE, WIDTH // 2, HEIGHT // 3, centered=True)
        lose_loop()


def reset_ball_and_paddle():
    """Reset the ball and paddle to the center positions with random direction, ball on top of paddle."""
    global ball_x, ball_y, ball_speed_x, ball_speed_y, ball_moving, paddle_x

    # Position the paddle at the center horizontally
    paddle_x = (WIDTH - paddle_width) // 2  # Center the paddle horizontally

    # Position the ball in the center horizontally and just above the paddle vertically
    ball_x = WIDTH // 2
    ball_y = paddle_y - ball_radius * 2  # Ball is right on top of the paddle

    # Randomly choose ball's direction (middle, left, or right) and ensure no downward movement at initialization
    direction = random.choice(["middle", "left", "right"])
    if direction == "middle":
        ball_speed_x = random.choice([-1, 1]) * random.uniform(4, 6)
        ball_speed_y = random.choice([-1, 1]) * random.uniform(4, 6)
    elif direction == "left":
        ball_speed_x = -random.uniform(4, 6)
        ball_speed_y = random.choice([-1, 1]) * random.uniform(4, 6)
    elif direction == "right":
        ball_speed_x = random.uniform(4, 6)
        ball_speed_y = random.choice([-1, 1]) * random.uniform(4, 6)

    # Ensure the ball does not start moving downwards
    if ball_speed_y > 0:  # If ball is moving downward, reverse it to move upward
        ball_speed_y = -ball_speed_y

    ball_moving = False  # Ball is initially not moving until space is pressed


# Define the size of the falling obstacles
obstacle_width = 40  # Adjust the width as needed
obstacle_height = 40  # Adjust the height as needed


def game_loop(level="easy"):
    global ball_x, ball_y, paddle_x, paddle_y, ball_speed_x, ball_speed_y, ball_moving, lives, score, blocks
    global falling_obstacles  # Declare global for falling obstacles

    # Initialize the game
    reset_ball_and_paddle()
    blocks = create_blocks(level)
    falling_obstacles = create_falling_obstacles(level)  # Function to create falling obstacles

    ball_moving = True
    block_movement_start = pygame.time.get_ticks()

    running = True
    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle_x = max(paddle_x - paddle_speed, 0)
        if keys[pygame.K_RIGHT]:
            paddle_x = min(paddle_x + paddle_speed, WIDTH - paddle_width)

        # Ball movement and collision
        if ball_moving:
            ball_x += ball_speed_x
            ball_y += ball_speed_y

            # Wall collisions for ball 1
            if ball_x <= 0 or ball_x >= WIDTH - ball_radius * 2:
                ball_speed_x *= -1
            if ball_y <= 0:
                ball_speed_y *= -1

            # Paddle collision for ball 1
            if (
                    paddle_x <= ball_x + ball_radius <= paddle_x + paddle_width
                    and paddle_y <= ball_y + ball_radius * 2 <= paddle_y + paddle_height
            ):
                ball_speed_y *= -1

            # Block collision for ball 1
            for block in blocks[:]:
                if block["rect"].colliderect(pygame.Rect(ball_x, ball_y, ball_radius * 2, ball_radius * 2)):
                    ball_speed_y *= -1
                    blocks.remove(block)
                    score += block["score"]
                    break

        # Falling obstacles movement and collision
        if level in ["intermediate", "hard"]:
            current_time = pygame.time.get_ticks()

            # Move obstacles every 100ms for both levels
            if current_time - block_movement_start > 100:
                block_movement_start = current_time
                for obstacle in falling_obstacles[:]:
                    obstacle["rect"].y += obstacle.get("speed_y", 0)

                    # Remove obstacles that go beyond the screen
                    if obstacle["rect"].y > HEIGHT:
                        falling_obstacles.remove(obstacle)

                    # Check for collision with the ball
                    if (
                            obstacle["rect"].colliderect(pygame.Rect(ball_x, ball_y, ball_radius * 2, ball_radius * 2))
