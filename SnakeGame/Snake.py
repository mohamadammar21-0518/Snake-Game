import pygame
import random
import os
import time

# Initialization
pygame.init()
pygame.mixer.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (35, 45, 40)
BG_COLOR = (230, 240, 255)

# Constants
STATUS_BAR_HEIGHT = 60
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600 + STATUS_BAR_HEIGHT  # Extra space for status bar
GAME_AREA_TOP = STATUS_BAR_HEIGHT

# Window Setup
GAME_WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game by Ammar")

# Load Assets
BG = pygame.image.load("SnakeGame/Screen/Backgroundnew.jpg")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
INTRO = pygame.image.load("SnakeGame/Screen/Blue Modern Esport Game PresentationIntrolast.jpg")
OUTRO = pygame.image.load("SnakeGame/Screen/Game_over.jpg")

pygame.mixer.music.load("SnakeGame\Music\Landing_Music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.6)

EAT_SOUND = pygame.mixer.Sound("SnakeGame/Music/mixkit-arcade-retro-game-over-213.wav")

# Fonts and Clock
FONT = pygame.font.SysFont("Harrington", 35)
CLOCK = pygame.time.Clock()

# Helper Functions
def text_screen(text, color, x, y, center=False):
    screen_text = FONT.render(text, True, color)
    text_rect = screen_text.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    GAME_WINDOW.blit(screen_text, text_rect)

def plot_snake(win, body_color, snk_list, size):
    for i, (x, y) in enumerate(snk_list):
        if i == len(snk_list) - 1:
            pygame.draw.ellipse(win, (0, 200, 0), [x, y, size, size])  # Head
            eye_radius = size // 6
            eye_offset_x = size // 4
            eye_offset_y = size // 4
            pygame.draw.circle(win, WHITE, (x + eye_offset_x, y + eye_offset_y), eye_radius)
            pygame.draw.circle(win, WHITE, (x + size - eye_offset_x, y + eye_offset_y), eye_radius)
        else:
            pygame.draw.rect(win, body_color, [x, y, size, size])

def spawn_food():
    return (
        random.randint(20, SCREEN_WIDTH - 50),
        random.randint(GAME_AREA_TOP + 20, SCREEN_HEIGHT - 50),
        (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    )

def load_highscore():
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        return int(f.read())

def save_highscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

def pause_screen():
    paused = True
    while paused:
        GAME_WINDOW.blit(BG, (0, 0))
        text_screen("Game Paused. Press 'Enter' to Resume", BLACK, 450, 300, center=True)
        text_screen("Press Backspace to Exit", BLACK, 450, 350, center=True)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    paused = False
                elif event.key == pygame.K_BACKSPACE:
                    confirm_exit_screen()

def confirm_exit_screen():
    while True:
        GAME_WINDOW.blit(BG, (0, 0))
        text_screen("Are you sure you want to exit? (Y/N)", RED, 230, 280)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_n:
                    return

def game_over_screen(score, highscore, duration):
    pygame.mixer.music.load("SnakeGame/Music/Game_Over.mp3")
    pygame.mixer.music.play(-1)
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    time_str = f"{minutes:02}:{seconds:02}"

    while True:
        GAME_WINDOW.blit(OUTRO, (0, 0))
        text_screen("GAME OVER!", RED, SCREEN_WIDTH // 2, 240, center=True)
        text_screen(f"Your Score: {score}", WHITE, SCREEN_WIDTH // 2, 280, center=True)
        text_screen(f"High Score: {highscore}", WHITE, SCREEN_WIDTH // 2, 320, center=True)
        text_screen(f"Time Played: {time_str}", WHITE, SCREEN_WIDTH // 2, 360, center=True)
        text_screen("Press Enter to Play Again or Esc to Quit", BLACK, SCREEN_WIDTH // 2, 420, center=True)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    welcome()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

def gameloop(init_velocity, mode_label):
    snake_x, snake_y = 45, GAME_AREA_TOP + 55
    velocity_x, velocity_y = 0, 0
    snake_list = []
    snake_length = 1

    food_x, food_y, food_color = spawn_food()
    score = 0
    snake_size = 30
    fps = 60
    highscore = load_highscore()
    game_over = False

    start_time = time.time()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and velocity_x == 0:
                    velocity_x = init_velocity
                    velocity_y = 0
                elif event.key == pygame.K_LEFT and velocity_x == 0:
                    velocity_x = -init_velocity
                    velocity_y = 0
                elif event.key == pygame.K_UP and velocity_y == 0:
                    velocity_y = -init_velocity
                    velocity_x = 0
                elif event.key == pygame.K_DOWN and velocity_y == 0:
                    velocity_y = init_velocity
                    velocity_x = 0
                elif event.key == pygame.K_SPACE:
                    pause_screen()

        snake_x += velocity_x
        snake_y += velocity_y

        if abs(snake_x - food_x) < 20 and abs(snake_y - food_y) < 20:
            score += 10
            EAT_SOUND.play()
            food_x, food_y, food_color = spawn_food()
            snake_length += 5
            if score > highscore:
                highscore = score

        GAME_WINDOW.fill(BG_COLOR)
        GAME_WINDOW.blit(BG, (0, 0))

        # Draw top status bar
        pygame.draw.rect(GAME_WINDOW, (20, 20, 20), [0, 0, SCREEN_WIDTH, STATUS_BAR_HEIGHT])
        text_screen(f"Score: {score}", WHITE, 20, 15)
        text_screen(f"Mode: {mode_label}", WHITE, SCREEN_WIDTH // 2 - 200, 15)  # Mode display
        text_screen(f"High Score: {highscore}", WHITE, SCREEN_WIDTH - 250, 15)

        # Draw food
        pygame.draw.rect(GAME_WINDOW, food_color, [food_x, food_y, snake_size, snake_size])

        # Snake logic
        head = [snake_x, snake_y]
        snake_list.append(head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Collision
        if (head in snake_list[:-1] or
            not (0 <= snake_x <= SCREEN_WIDTH - snake_size) or
            not (GAME_AREA_TOP <= snake_y <= SCREEN_HEIGHT - snake_size)):
            save_highscore(highscore)
            duration = time.time() - start_time
            game_over_screen(score, highscore, duration)
            return

        plot_snake(GAME_WINDOW, BLACK, snake_list, snake_size)
        pygame.display.update()
        CLOCK.tick(fps)


def gameloop_ai_mode(init_velocity, mode_label="AI Mode"):
    snake_x, snake_y = 45, GAME_AREA_TOP + 55
    velocity_x, velocity_y = init_velocity, 0
    snake_list = []
    snake_length = 1
    food_x, food_y, food_color = spawn_food()
    score = 0
    snake_size = 30
    fps = 30
    highscore = load_highscore()
    game_over = False
    start_time = time.time()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_SPACE:
                    pause_screen()

        # Basic AI logic: move closer to food while avoiding self
        possible_moves = [
            (init_velocity, 0),   # Right
            (-init_velocity, 0),  # Left
            (0, init_velocity),   # Down
            (0, -init_velocity)   # Up
        ]

        # Prioritize directions: move toward food
        prioritized_moves = sorted(possible_moves, key=lambda mv: (
            abs((snake_x + mv[0]) - food_x) + abs((snake_y + mv[1]) - food_y)
        ))

        # Pick the first move that doesn't collide with self
        for move in prioritized_moves:
            new_head = [snake_x + move[0], snake_y + move[1]]
            if new_head not in snake_list and \
               0 <= new_head[0] <= SCREEN_WIDTH - snake_size and \
               GAME_AREA_TOP <= new_head[1] <= SCREEN_HEIGHT - snake_size:
                velocity_x, velocity_y = move
                break  # Valid move found

        snake_x += velocity_x
        snake_y += velocity_y

        # Eat food
        if abs(snake_x - food_x) < 20 and abs(snake_y - food_y) < 20:
            score += 10
            EAT_SOUND.play()
            food_x, food_y, food_color = spawn_food()
            snake_length += 5
            if score > highscore:
                highscore = score

        GAME_WINDOW.fill(BG_COLOR)
        GAME_WINDOW.blit(BG, (0, 0))

        # Status bar
        pygame.draw.rect(GAME_WINDOW, (20, 20, 20), [0, 0, SCREEN_WIDTH, STATUS_BAR_HEIGHT])
        text_screen(f"Score: {score}", WHITE, 20, 15)
        text_screen(f"Mode: {mode_label}", WHITE, SCREEN_WIDTH // 2 - 200, 15)  # Mode display
        text_screen(f"High Score: {highscore}", WHITE, SCREEN_WIDTH - 250, 15)

        # Draw food
        pygame.draw.rect(GAME_WINDOW, food_color, [food_x, food_y, snake_size, snake_size])

        # Snake logic
        head = [snake_x, snake_y]
        snake_list.append(head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Collision detection
        if (head in snake_list[:-1] or
            not (0 <= snake_x <= SCREEN_WIDTH - snake_size) or
            not (GAME_AREA_TOP <= snake_y <= SCREEN_HEIGHT - snake_size)):
            save_highscore(highscore)
            duration = time.time() - start_time
            game_over_screen(score, highscore, duration)
            return

        plot_snake(GAME_WINDOW, BLACK, snake_list, snake_size)
        pygame.display.update()
        CLOCK.tick(fps)


def welcome():
    while True:
        GAME_WINDOW.blit(INTRO, (0, 0))
        text_screen("Press 1 for Easy | 2 for Medium | 3 for Hard | 4 for AI Mode", WHITE, 5, 540)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    gameloop(2, "Easy")
                elif event.key == pygame.K_2:
                    gameloop(5, "Medium")
                elif event.key == pygame.K_3:
                    gameloop(7, "Hard")
                elif event.key == pygame.K_4:
                    gameloop_ai_mode(8, "AI Mode")

welcome()
