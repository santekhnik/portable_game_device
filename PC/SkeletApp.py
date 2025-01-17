import pygame
import sys

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
ports = ["COM1", "COM2", "COM3"]
selected_game = 0
games = ["Pong", "Tetris (Coming soon)", "Snake (Coming soon)"]

# Pong game variables
ball_pos = [FRAME_X + GAME_WIDTH * SCALE // 2, FRAME_Y + GAME_HEIGHT * SCALE // 2]
ball_speed = [0.1, 0.1]
paddle_width, paddle_height = 80, 7
paddle_pos = [FRAME_X + GAME_WIDTH * SCALE // 2 - paddle_width // 2, FRAME_Y + GAME_HEIGHT * SCALE - paddle_height - 10]
paddle_speed = 0.5
score = 0

# Game loop
running = True
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
                    if selected_game == 0:  # Pong
                        state = STATE_GAME
                    else:
                        print("Error: Game not implemented")

            elif state == STATE_GAME:
                if event.key == pygame.K_ESCAPE:
                    state = STATE_MENU
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_r:
                    # Restart the game
                    ball_pos = [FRAME_X + GAME_WIDTH * SCALE // 2, FRAME_Y + GAME_HEIGHT * SCALE // 2]
                    ball_speed = [0.05, 0.05]
                    paddle_pos = [FRAME_X + GAME_WIDTH * SCALE // 2 - paddle_width // 2, FRAME_Y + GAME_HEIGHT * SCALE - paddle_height - 10]
                    score = 0

    keys = pygame.key.get_pressed()

    if state == STATE_GAME and not paused:
        # Move paddle
        if keys[pygame.K_LEFT] and paddle_pos[0] > FRAME_X:
            paddle_pos[0] -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_pos[0] < FRAME_X + GAME_WIDTH * SCALE - paddle_width:
            paddle_pos[0] += paddle_speed

        # Update ball position
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]

        # Ball collision with walls
        if ball_pos[0] <= FRAME_X or ball_pos[0] >= FRAME_X + GAME_WIDTH * SCALE:
            ball_speed[0] = -ball_speed[0]
        if ball_pos[1] <= FRAME_Y:
            ball_speed[1] = -ball_speed[1]

        # Ball collision with paddle
        if paddle_pos[1] <= ball_pos[1] <= paddle_pos[1] + paddle_height and \
                paddle_pos[0] <= ball_pos[0] <= paddle_pos[0] + paddle_width:
            ball_speed[1] = -ball_speed[1]
            score += 1

        # Ball goes out of bounds
        if ball_pos[1] > FRAME_Y + GAME_HEIGHT * SCALE:
            print(f"Game Over! Your score: {score}")
            ball_pos = [FRAME_X + GAME_WIDTH * SCALE // 2, FRAME_Y + GAME_HEIGHT * SCALE // 2]
            ball_speed = [0.1, 0.1]
            score = 0

        # Draw game elements
        pygame.draw.rect(screen, WHITE, (paddle_pos[0], paddle_pos[1], paddle_width, paddle_height))
        pygame.draw.circle(screen, WHITE, (int(ball_pos[0]), int(ball_pos[1])), 10)

        # Display score
        score_text = FONT.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw game area
        pygame.draw.rect(screen, WHITE, (FRAME_X, FRAME_Y, GAME_WIDTH * SCALE, GAME_HEIGHT * SCALE), 5)

        # Controls info
        controls = ["ESC - exit", "← - move to the left", "→ - move to the right", "R - restart", "P - pause"]
        for i, control in enumerate(controls):
            control_text = SMALL_FONT.render(control, True, WHITE)
            screen.blit(control_text, (10, SCREEN_HEIGHT - 100 + i * 20))

    elif paused:
        pause_text = FONT.render("Game Paused", True, WHITE)
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2))

    elif state == STATE_CONNECTION:
        # Connection menu
        title = FONT.render("Connection", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        for i, port in enumerate(ports):
            color = WHITE if i == selected_port else GRAY
            port_text = FONT.render(port, True, color)
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