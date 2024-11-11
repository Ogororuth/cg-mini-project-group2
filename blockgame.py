import pygame
from pygame.locals import *

pygame.init()

# Screen setup
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

# Define fonts and colors
font = pygame.font.SysFont('Constantia', 30)
bg = (234, 218, 184)
block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)
paddle_col = (142, 135, 123)
paddle_outline = (100, 100, 100)
text_col = (78, 81, 139)

# Game variables
cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0
ball_speed_increase = 1
score = 0
current_level = 1
high_score = 0  # Track the high score

# Draw text function
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Wall class
class Wall:
    def _init_(self):
        self.width = screen_width // cols
        self.height = 50

    def create_wall(self):
        global score
        score = 0
        self.blocks = []
        for row in range(rows):
            block_row = []
            for col in range(cols):
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                strength = 3 if row < 2 else 2 if row < 4 else 1
                block_row.append([rect, strength])
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                color = block_blue if block[1] == 3 else block_green if block[1] == 2 else block_red
                pygame.draw.rect(screen, color, block[0])
                pygame.draw.rect(screen, bg, block[0], 2)

# Paddle class
class Paddle:
    def _init_(self):
        self.reset()

    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, paddle_col, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)

    def reset(self):
        self.height = 20
        self.width = int(screen_width / cols)
        self.x = int((screen_width / 2) - (self.width / 2))
self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)

# Ball class
class Ball:
    def _init_(self, x, y):
        self.reset(x, y)

    def move(self):
        global score
        collision_thresh = 5
        wall_destroyed = True

        for row in wall.blocks:
            for block in row:
                if self.rect.colliderect(block[0]):
                    if abs(self.rect.bottom - block[0].top) < collision_thresh or abs(self.rect.top - block[0].bottom) < collision_thresh:
                        self.speed_y *= -1
                    elif abs(self.rect.right - block[0].left) < collision_thresh or abs(self.rect.left - block[0].right) < collision_thresh:
                        self.speed_x *= -1
                    if block[1] > 1:
                        block[1] -= 1
                    else:
                        block[0] = (0, 0, 0, 0)
                    score += 10

                if block[0] != (0, 0, 0, 0):
                    wall_destroyed = False

        if wall_destroyed:
            self.game_over = 1

        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            self.game_over = -1

        if self.rect.colliderect(player_paddle.rect):
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                self.speed_x = max(min(self.speed_x, self.speed_max), -self.speed_max)

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        return self.game_over

    def draw(self):
        pygame.draw.circle(screen, paddle_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad, 3)

    def reset(self, x, y):
        self.ball_rad = 10
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
