
import serial
import json
import time
import pygame
import serial.tools.list_ports
import os

font_path = os.path.join("./", "MinecraftTen-VGORe.ttf")

# Ініціалізація Pygame
pygame.init()
WIDTH, HEIGHT = 320, 640
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

    pygame.draw.line(screen, WHITE, (0, 0), (WIDTH, 0), 30)  # Верхня лінія
    pygame.draw.line(screen, WHITE, (0, 0), (0, HEIGHT), 40)  # Ліва лінія
    pygame.draw.line(screen, WHITE, (WIDTH - 10, 0), (WIDTH - 10, HEIGHT), 25)  # Права лінія

    # Малюємо м'яч
    ball_size = 20  # Розмір квадрата
    pygame.draw.rect(screen, WHITE, (ball[0] * ball_size, ball[1] * ball_size, ball_size, ball_size))

    # Малюємо платформу
    for i in range(4):
        platform_y_position = HEIGHT - 60  # Позиція платформи на 30 пікселів вище нижнього краю
        pygame.draw.rect(screen, WHITE, (platform[0] * 20 + i * 20, platform_y_position, 20, 10))

    pygame.display.flip()


def select_com_port():
    ports = serial.tools.list_ports.comports()
    if not ports:
        return None

    selected_index = 0

    while True:
        # Очищення екрану
        screen.fill(BLACK)

        # Малювання заголовка
        text = FONT.render("Select COM Port:", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, 30))
        screen.blit(text, text_rect)

        # Малювання списку портів
        for idx, port in enumerate(ports):
            color = WHITE
            port_text = FONT.render(f"{idx + 1}: {port.device}", True, color)
            port_text_rect = port_text.get_rect(center=(WIDTH // 2, 80 + idx * 40))
            screen.blit(port_text, port_text_rect)

            # Додаємо підкреслення лише для вибраного пункту
            if idx == selected_index:
                pygame.draw.line(
                    screen,
                    (255, 255, 255),  # Синій колір підкреслення
                    (port_text_rect.left, port_text_rect.bottom - 3),
                    (port_text_rect.right, port_text_rect.bottom - 3),
                    2,
                )

        pygame.display.flip()

        # Обробка подій
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

def show_error_message(message):
    """Відображає віконце з повідомленням про помилку."""
    error_screen = pygame.Surface((WIDTH, HEIGHT))
    error_screen.fill(BLACK)

    # Текст повідомлення
    error_text = FONT.render(message, True, WHITE)
    error_text_rect = error_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Кнопка "OK"
    ok_text = FONT.render("OK", True, WHITE)
    ok_text_rect = ok_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    while True:
        error_screen.fill(BLACK)
        error_screen.blit(error_text, error_text_rect)
        error_screen.blit(ok_text, ok_text_rect)
        screen.blit(error_screen, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Перевіряємо, чи натиснута кнопка "OK"
                if ok_text_rect.collidepoint(event.pos):
                    return


def select_game(ser):
    options = ["Pong"]
    selected_index = 0

    while True:
        # Очищення екрану
        screen.fill(BLACK)

        # Малювання заголовка
        text = FONT.render("Select Game:", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, 30))
        screen.blit(text, text_rect)

        # Малювання списку ігор
        for idx, option in enumerate(options):
            color = WHITE
            option_text = FONT.render(f"{idx + 1}: {option}", True, color)
            option_text_rect = option_text.get_rect(center=(WIDTH // 2, 80 + idx * 50))
            screen.blit(option_text, option_text_rect)

            # Додаємо підкреслення лише для вибраного пункту
            if idx == selected_index:
                pygame.draw.line(
                    screen,
                    (255, 255, 255),  # Синій колір підкреслення
                    (option_text_rect.left, option_text_rect.bottom - 3),
                    (option_text_rect.right, option_text_rect.bottom - 3),
                    2,
                )

        pygame.display.flip()

        # Обробка подій
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
    try:
        ser = init_serial(com_port)
    except serial.SerialException:
        show_error_message("Invalid COM Port Selected!")
        return

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