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
        self.rect = Rect(x - self.ball_rad, y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0

# Level selection
def select_level(level):
    global rows, ball_speed_increase
    if level == 1:
        rows, ball_speed_increase = 6, 1
    elif level == 2:
        rows, ball_speed_increase = 10, 1.3
    elif level == 3:
        rows, ball_speed_increase = 14, 1.6

# Display high score
def display_high_score():
    global high_score
    draw_text(f'High Score: {high_score}', font, text_col, 5, 40)

# Game loop
def game_loop():
    global live_ball, game_over, score, current_level, high_score
    select_level(current_level)
    wall.create_wall()
    player_paddle.reset()
    ball.reset(player_paddle.rect.x + (player_paddle.width // 2), player_paddle.rect.y - player_paddle.height)

    run = True
    while run:
        clock.tick(fps)
        screen.fill(bg)
         wall.draw_wall()
        player_paddle.draw()
        ball.draw()

        # Display score and high score
        draw_text(f'Score: {score}', font, text_col, 5, 5)
        display_high_score()

        if live_ball:
            player_paddle.move()
            game_over = ball.move()
            if game_over != 0:
                live_ball = False

        # Display game messages
        if not live_ball and game_over != 0:
            if game_over == -1:
                draw_text("GAME OVER! Press 'R' to Restart", font, text_col, 150, screen_height // 2)
            elif game_over == 1:
                draw_text("YOU WON! Press 'N' for Next Level", font, text_col, 150, screen_height // 2)

            # Check for restart or next level
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and game_over == -1:  # Restart after losing
                        game_over = 0
                        score = 0
                        game_loop()
                    elif event.key == pygame.K_n and game_over == 1:  # Next level after winning
                        current_level += 1
                        if current_level > 3:
                            current_level = 1  # Restart from level 1
                        game_over = 0
                        score = 0
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not live_ball:
                live_ball = True

        pygame.display.update()
    pygame.quit()


# Initialize game objects
wall = Wall()
player_paddle = Paddle()
ball = Ball(player_paddle.rect.x + (player_paddle.width // 2), player_paddle.rect.y - player_paddle.height)

# Ask for level selection
def ask_for_level():
    global current_level
    level_bg = (255, 255, 204)  # Light yellow background for level selection screen
    level_text_col = (0, 0, 0)  # Use black text for better contrast

    while True:
        screen.fill(level_bg)  # Fill screen with bright background
        draw_text("BREAKOUT GAME", font, text_col, 150, 150)
        draw_text("Select Difficulty Level", font, text_col, 150, 250)
        draw_text("1. Easy", font, text_col, 200, 300)
        draw_text("2. Intermediate", font, text_col, 200, 350)
        draw_text("3. Hard", font, text_col, 200, 400)

        pygame.display.update()  # Refresh the display with the text

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_level = 1
                    game_loop()
                elif event.key == pygame.K_2:
                    current_level = 2
                    game_loop()
                elif event.key == pygame.K_3:
                    current_level = 3
                    game_loop()


# Start the game
ask_for_level()
pygame.quit()
