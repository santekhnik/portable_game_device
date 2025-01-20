import pygame
import sys
import random
import serial.tools.list_ports
import time

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 750
GAME_WIDTH, GAME_HEIGHT = 20, 40
SCALE = 15
FRAME_X, FRAME_Y = SCREEN_WIDTH // 2 - GAME_WIDTH * SCALE // 2, SCREEN_HEIGHT // 2 - GAME_HEIGHT * SCALE // 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Font setup
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 24)
SMALL_FONT = pygame.font.SysFont("Arial", 16)

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("NeDoGameBoy")

# Game states
STATE_CONNECTION = 0
STATE_MENU = 1
STATE_GAME = 2

# Initial state
state = STATE_CONNECTION
paused = False

# Variables
selected_port = 0
port_list = []
ports = serial.tools.list_ports.comports()
for port in ports:
    port_list.append(port.device)
selected_game = 0
games = ["Pong", "Tetris (Coming soon)", "Snake"]

# Define the structure of a game
class Game:
    def __init__(self, name):
        self.name = name

    def start(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

# Define the Pong game as a subclass of Game
class Pong(Game):
    def __init__(self):
        super().__init__("Pong")
        self.ball_pos = [FRAME_X + GAME_WIDTH * SCALE // 2, FRAME_Y + GAME_HEIGHT * SCALE // 2]
        self.ball_speed = [0.1, 0.1]
        self.paddle_width, self.paddle_height = 80, 7
        self.paddle_pos = [FRAME_X + GAME_WIDTH * SCALE // 2 - self.paddle_width // 2, FRAME_Y + GAME_HEIGHT * SCALE - self.paddle_height - 10]
        self.paddle_speed = 0.5
        self.score = 0

    def start(self):
        self.ball_pos = [FRAME_X + GAME_WIDTH * SCALE // 2, FRAME_Y + GAME_HEIGHT * SCALE // 2]
        self.ball_speed = [0.1, 0.1]
        self.paddle_pos = [FRAME_X + GAME_WIDTH * SCALE // 2 - self.paddle_width // 2, FRAME_Y + GAME_HEIGHT * SCALE - self.paddle_height - 10]
        self.score = 0

    def update(self, keys):
        # Move paddle
        if keys[pygame.K_LEFT] and self.paddle_pos[0] > FRAME_X:
            self.paddle_pos[0] -= self.paddle_speed
        if keys[pygame.K_RIGHT] and self.paddle_pos[0] < FRAME_X + GAME_WIDTH * SCALE - self.paddle_width:
            self.paddle_pos[0] += self.paddle_speed

        # Update ball position
        self.ball_pos[0] += self.ball_speed[0]
        self.ball_pos[1] += self.ball_speed[1]

        # Ball collision with walls
        if self.ball_pos[0] <= FRAME_X or self.ball_pos[0] >= FRAME_X + GAME_WIDTH * SCALE:
            self.ball_speed[0] = -self.ball_speed[0]
        if self.ball_pos[1] <= FRAME_Y:
            self.ball_speed[1] = -self.ball_speed[1]

        # Ball collision with paddle
        if self.paddle_pos[1] <= self.ball_pos[1] <= self.paddle_pos[1] + self.paddle_height and \
                self.paddle_pos[0] <= self.ball_pos[0] <= self.paddle_pos[0] + self.paddle_width:
            self.ball_speed[1] = -self.ball_speed[1]
            self.score += 1

        # Ball goes out of bounds
        if self.ball_pos[1] > FRAME_Y + GAME_HEIGHT * SCALE:
            print(f"Game Over! Your score: {self.score}")
            self.start()

    def draw(self):
        # Draw paddle and ball
        pygame.draw.rect(screen, WHITE, (self.paddle_pos[0], self.paddle_pos[1], self.paddle_width, self.paddle_height))
        pygame.draw.circle(screen, WHITE, (int(self.ball_pos[0]), int(self.ball_pos[1])), 10)

        # Display score
        score_text = FONT.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Controls info
        controls = ["ESC - exit", "← - move to the left", "→ - move to the right", "R - restart", "P - pause"]
        for i, control in enumerate(controls):
            control_text = SMALL_FONT.render(control, True, WHITE)
            screen.blit(control_text, (10, SCREEN_HEIGHT - 100 + i * 20))

        # Draw game area
        pygame.draw.rect(screen, WHITE, (FRAME_X, FRAME_Y, GAME_WIDTH * SCALE, GAME_HEIGHT * SCALE), 5)

# Define the Snake game as a subclass of Game
class Snake(Game):
    def __init__(self):
        super().__init__("Snake")
        self.snake_pos = [[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]]
        self.snake_dir = [0, -SCALE]  # Moving up initially
        self.food_pos = [random.randrange(FRAME_X, FRAME_X + GAME_WIDTH * SCALE, SCALE),
                         random.randrange(FRAME_Y, FRAME_Y + GAME_HEIGHT * SCALE, SCALE)]
        self.food_spawn = True
        self.score = 0
        self.last_move_time = time.time()
        self.move_interval = 0.1  # Interval between moves in seconds

    def start(self):
        self.snake_pos = [[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]]
        self.snake_dir = [0, -SCALE]
        self.food_pos = [random.randrange(FRAME_X, FRAME_X + GAME_WIDTH * SCALE, SCALE),
                         random.randrange(FRAME_Y, FRAME_Y + GAME_HEIGHT * SCALE, SCALE)]
        self.food_spawn = True
        self.score = 0
        self.last_move_time = time.time()

    def update(self, keys):
        current_time = time.time()
        if current_time - self.last_move_time >= self.move_interval:
            # Control the snake's direction
            if keys[pygame.K_LEFT]:
                self.snake_dir = [-SCALE, 0]
            elif keys[pygame.K_RIGHT]:
                self.snake_dir = [SCALE, 0]
            elif keys[pygame.K_UP]:
                self.snake_dir = [0, -SCALE]
            elif keys[pygame.K_DOWN]:
                self.snake_dir = [0, SCALE]

            # Move snake
            new_head = [self.snake_pos[0][0] + self.snake_dir[0], self.snake_pos[0][1] + self.snake_dir[1]]
            self.snake_pos.insert(0, new_head)

            # Check if snake eats food
            if new_head == self.food_pos:
                self.food_spawn = False
                self.score += 1
            else:
                self.snake_pos.pop()

            # Spawn new food if needed
            if not self.food_spawn:
                self.food_pos = [random.randrange(FRAME_X, FRAME_X + GAME_WIDTH * SCALE, SCALE),
                                 random.randrange(FRAME_Y, FRAME_Y + GAME_HEIGHT * SCALE, SCALE)]
                self.food_spawn = True

            # Check if snake hits the walls or itself
            if new_head[0] < FRAME_X or new_head[0] >= FRAME_X + GAME_WIDTH * SCALE or \
                    new_head[1] < FRAME_Y or new_head[1] >= FRAME_Y + GAME_HEIGHT * SCALE or \
                    new_head in self.snake_pos[1:]:
                print(f"Game Over! Your score: {self.score}")
                self.start()

            self.last_move_time = current_time

    def draw(self):
        # Draw the snake
        for segment in self.snake_pos:
            pygame.draw.rect(screen, WHITE, pygame.Rect(segment[0], segment[1], SCALE, SCALE))

        # Draw the food
        pygame.draw.rect(screen, RED, pygame.Rect(self.food_pos[0], self.food_pos[1], SCALE, SCALE))

        # Display score
        score_text = FONT.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Controls info
        controls = ["ESC - exit", "← - move left", "→ - move right", "↑ - move up", "↓ - move down", "R - restart", "P - pause"]
        for i, control in enumerate(controls):
            control_text = SMALL_FONT.render(control, True, WHITE)
            screen.blit(control_text, (10, SCREEN_HEIGHT - 100 + i * 20))

        # Draw game area
        pygame.draw.rect(screen, WHITE, (FRAME_X, FRAME_Y, GAME_WIDTH * SCALE, GAME_HEIGHT * SCALE), 5)

# Game loop
running = True
games_dict = {
    0: Pong(),
    2: Snake(),
    # You can add other games like Tetris here
}

current_game = None
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if state == STATE_CONNECTION:
                if event.key == pygame.K_UP:
                    selected_port = (selected_port - 1) % len(ports)
                elif event.key == pygame.K_DOWN:
                    selected_port = (selected_port + 1) % len(ports)
                elif event.key == pygame.K_RETURN:
                    state = STATE_MENU

            elif state == STATE_MENU:
                if event.key == pygame.K_UP:
                    selected_game = (selected_game - 1) % len(games)
                elif event.key == pygame.K_DOWN:
                    selected_game = (selected_game + 1) % len(games)
                elif event.key == pygame.K_RETURN:
                    current_game = games_dict.get(selected_game)
                    if current_game:
                        current_game.start()
                        state = STATE_GAME
                    else:
                        print("Error: Game not implemented")

            elif state == STATE_GAME:
                if event.key == pygame.K_ESCAPE:
                    state = STATE_MENU
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_r:
                    current_game.start()

    keys = pygame.key.get_pressed()

    if state == STATE_GAME and current_game and not paused:
        current_game.update(keys)
        current_game.draw()

    elif paused:
        pause_text = FONT.render("Game Paused", True, WHITE)
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2))

    elif state == STATE_CONNECTION:
        # Connection menu
        title = FONT.render("Connection", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        for i, port in enumerate(ports):
            color = WHITE if i == selected_port else GRAY
            port_text = FONT.render(", ".join(port_list), True, color)
            screen.blit(port_text, (SCREEN_WIDTH // 2 - port_text.get_width() // 2, 150 + i * 40))

    elif state == STATE_MENU:
        # Game selection menu
        title = FONT.render("NeDoGameBoy", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        for i, game in enumerate(games):
            color = WHITE if i == selected_game else GRAY
            game_text = FONT.render(game, True, color)
            screen.blit(game_text, (SCREEN_WIDTH // 2 - game_text.get_width() // 2, 150 + i * 40))

    pygame.display.flip()

pygame.quit()
sys.exit()