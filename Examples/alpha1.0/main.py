import serial
import json
import time
import pygame
import serial.tools.list_ports
import os

font_path = os.path.join("./", "MinecraftTen-VGORe.ttf")

# Ініціалізація Pygame
pygame.init()
WIDTH, HEIGHT = 820, 420
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Selection")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = (0, 196, 156)
PLATFORM_COLOR = (118, 0, 196)
FONT = pygame.font.Font(font_path, 36)


def init_serial(port, baudrate=115200):
    return serial.Serial(port, baudrate, timeout=1)


def receive_game_data(ser):
    try:
        line = ser.readline().decode("utf-8").strip()
        if line:
            return json.loads(line)
    except (json.JSONDecodeError, UnicodeDecodeError):
        print("Receiving error")
    return None


def draw_game(ball, platform):
    screen.fill(BLACK)

    # Малюємо м'яч
    ball_size = 20  # Розмір квадрата
    pygame.draw.rect(screen, WHITE, (ball[0] * ball_size, ball[1] * ball_size, ball_size, ball_size))

    # Малюємо платформу
    for i in range(4):
        platform_y_position = HEIGHT - 40  # Позиція платформи на 30 пікселів вище нижнього краю
        pygame.draw.rect(screen, WHITE, (platform[0] * 20 + i * 20, platform_y_position, 20, 10))

    pygame.display.flip()


def select_com_port():
    ports = serial.tools.list_ports.comports()
    if not ports:
        return None

    selected_index = 0

    while True:
        screen.fill(BLACK)
        text = FONT.render("Select COM Port:", True, WHITE)
        screen.blit(text, (10, 10))

        for idx, port in enumerate(ports):
            color = (0, 0, 255) if idx == selected_index else BLACK
            port_text = FONT.render(f"{idx + 1}: {port.device}", True, WHITE)
            screen.blit(port_text, (10, 50 + idx * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(ports)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(ports)
                elif event.key == pygame.K_RETURN:
                    return ports[selected_index].device


def select_game(ser):
    options = ["Pong"]
    selected_index = 0

    while True:
        screen.fill(BLACK)
        text = FONT.render("Select Game:", True, WHITE)
        screen.blit(text, (10, 10))

        for idx, option in enumerate(options):
            color = (0, 0, 255) if idx == selected_index else BLACK
            option_text = FONT.render(f"{idx + 1}: {option}", True, WHITE)
            screen.blit(option_text, (10, 50 + idx * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    ser.write(str(selected_index + 1).encode())
                    return options[selected_index]


def main():
    com_port = select_com_port()
    if not com_port:
        return
    ser = init_serial(com_port)

    game = select_game(ser)
    if not game:
        return

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        data = receive_game_data(ser)
        if data:
            ball = data["ball"]
            platform = data["platform"]
            draw_game(ball, platform)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            ser.write(b'a')
        elif keys[pygame.K_d]:
            ser.write(b'd')
        elif keys[pygame.K_r]:
            ser.write(b'r')
        elif keys[pygame.K_p]:
            ser.write(b'p')

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
