import serial
import time
import pygame
import serial.tools.list_ports
import os

font_path = os.path.join("./", "MinecraftTen-VGORe.ttf")

# Ініціалізація Pygame
pygame.init()
pygame.mixer.init()
menu_music = pygame.mixer.Sound("music_menu.mp3")  # Завантаження файлу
game_music = pygame.mixer.Sound("game_music.mp3")  # Завантаження файлу
WIDTH, HEIGHT = 320, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Selection")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = (0, 196, 156)
PLATFORM_COLOR = (118, 0, 196)
FONT = pygame.font.Font(font_path, 36)
FONT2 = pygame.font.Font(font_path, 22)
FONT3 = pygame.font.Font(font_path, 15)
pause = 0
height = 0
width = 0


def init_serial(port, baudrate=115200):
    try:
        return serial.Serial(port, baudrate, timeout=5)
    except serial.SerialException as e:
        show_error_message(f"Serial Error: {e}")
        return None


def calculate_bcc(data):
    """Обчислює контрольну суму (BCC) як XOR всіх байтів."""
    bcc = 0
    for byte in data:
        bcc ^= byte
    return bcc


def encode_value(value: float) -> int:
    """
    Кодує число згідно з протоколом.
    Якщо число ціле, зсуваємо вліво на 1.
    Якщо дробове, зсуваємо вліво на 1 та додаємо 1.

    :param value: вхідне число (ціле або дробове).
    :return: закодоване число у вигляді цілого значення.
    """
    # Перевіряємо, чи число дробове
    is_fractional = value % 1 != 0

    # Зсув вліво на 1
    encoded_value = int(value) << 1

    # Додаємо 1, якщо число дробове
    if is_fractional:
        encoded_value += 1

    return encoded_value


def decode_value(encoded_value: int) -> float:
    """
        Розшифровує отримане значення за протоколом.

        Якщо молодший біт 1, значення дробове, додаємо 0.5 після зсуву вправо.
        Якщо молодший біт 0, значення ціле.

        :param encoded_value: закодоване значення у вигляді цілого числа (0–255).
        :return: декодоване число (ціле або дробове).
        """
    # Перевіряємо молодший біт
    is_fractional = encoded_value & 1

    # Зміщуємо вправо на 1
    decoded_value = encoded_value >> 1

    # Додаємо 0.5, якщо число дробове
    if is_fractional:
        return decoded_value + 0.5
    else:
        return float(decoded_value)


def show_error_message(message, ser=None):
    """Відображає віконце з повідомленням про помилку."""
    error_screen = pygame.Surface((WIDTH, HEIGHT))
    error_screen.fill(BLACK)
    lines = message.split("\n")  # Розбиваємо текст за \n

    while True:
        error_screen.fill(BLACK)

        for i, line in enumerate(lines):
            error_text = FONT.render(line, True, WHITE)
            error_text_rect = error_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20 + i * 30))
            error_screen.blit(error_text, error_text_rect)

        ok_text = FONT.render("OK", True, WHITE)
        ok_text_rect = ok_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        error_screen.blit(ok_text, ok_text_rect)

        screen.blit(error_screen, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if ser:
                    menu_music.stop()
                    game_music.stop()
                    ser.close()
                menu_music.stop()
                game_music.stop()
                main()


def select_com_port():
    selected_index = 0
    while True:
        ports = serial.tools.list_ports.comports()
        if not ports:
            show_error_message("No COM ports\nfound!")
            return None

        screen.fill(BLACK)
        text = FONT.render("Select COM Port:", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, 30))
        screen.blit(text, text_rect)

        for idx, port in enumerate(ports):
            color = WHITE
            port_text = FONT.render(f"{idx + 1}: {port.device}", True, color)
            port_text_rect = port_text.get_rect(center=(WIDTH // 2, 80 + idx * 40))
            screen.blit(port_text, port_text_rect)
            if idx == selected_index:
                pygame.draw.line(screen, WHITE, (port_text_rect.left, port_text_rect.bottom),
                                 (port_text_rect.right, port_text_rect.bottom), 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    selected_index = (selected_index + 1) % len(ports)
                elif event.key == pygame.K_w:
                    selected_index = (selected_index - 1) % len(ports)
                elif event.key == pygame.K_RETURN:
                    com_port = ports[selected_index].device
                    try:
                        ser = init_serial(com_port)
                        if ser is None:
                            continue

                        packet = bytes([0x01, 0x00])
                        packet += bytes([calculate_bcc(packet)])
                        ser.write(packet)
                        time.sleep(0.1)
                        response = ser.read(ser.in_waiting)

                        if response and response[:2] == b'\x01\xff\xff':
                            show_error_message("Incorrect Start BCC!\nRetrying...", ser)
                            continue

                        if len(response) >= 3:
                            num_games = int(response[1])
                            print(f"Number of games available: {num_games}")
                            return com_port
                        else:
                            show_error_message("Failed to get\ngame data!", ser)
                            continue
                    except serial.SerialException:
                        show_error_message("Invalid\nCOM Port\nSelected!", ser)
                        return None


def select_game(ser):
    options = ["Pong"]
    selected_index = 0

    while True:
        screen.fill(BLACK)
        text = FONT.render("Select Game:", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, 30))
        screen.blit(text, text_rect)

        for idx, option in enumerate(options):
            option_text = FONT.render(f"{idx + 1}: {option}", True, WHITE)
            option_text_rect = option_text.get_rect(center=(WIDTH // 2, 80 + idx * 50))
            screen.blit(option_text, option_text_rect)
            if idx == selected_index:
                pygame.draw.line(screen, WHITE, (option_text_rect.left, option_text_rect.bottom),
                                 (option_text_rect.right, option_text_rect.bottom), 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_w:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    while True:
                        global width
                        global height
                        BCC = calculate_bcc([0x02, 14, 0, 0])
                        packet = bytes([0x02, 14, 0, 0, BCC])
                        ser.write(packet)
                        time.sleep(0.1)
                        response = ser.read(ser.in_waiting)

                        if len(response) >= 4 and response[0] == 0x02:
                            width = response[2]
                            height = response[3]
                            print(width, height)
                            if response[1:3] == b'\xff\xff':
                                show_error_message("Incorrect BCC!\nRetrying...", ser)
                                continue
                            elif response[1:3] == b'\xdd\xff':
                                show_error_message("Invalid game selection!\nTry again.", ser)
                                continue
                            else:
                                global pause
                                pause = 1
                                return width, height
                        else:
                            show_error_message("Failed to receive\nvalid game data!", ser)
                            continue


def send_initial_command(ser):
    key_value = 13
    BCC = calculate_bcc([0x04, key_value])
    packet = bytes([0x04, key_value, BCC])
    global pause
    pause = 0
    ser.write(packet)
    print("Sent initial command: ", packet)
    response = ser.read(ser.in_waiting)
    print(response)
    time.sleep(0.1)


def receive_game_data(ser, packet_size=8):
    global pause  # Якщо змінна pause глобальна, потрібно її явно вказати

    while True:
        if pause:
            time.sleep(0.1)  # Робимо коротку паузу, щоб не перевантажувати процесор
            continue
        packet = ser.read(packet_size)

        if not packet:
            show_error_message("No data incoming", ser)
            return
        if len(packet) != packet_size:
            continue

        print(packet)
        ball_x = decode_value(packet[1])
        ball_y = decode_value(packet[2])

        if packet[0] == 0x03:
            data_bytes = packet[1:-1]
            BCC = packet[-1]

            if calculate_bcc(packet[:-1]) == BCC:
                platform = data_bytes[2]
                ball = [ball_x, ball_y]
                score = packet[5]
                best_score = packet[6]
                print("coords:", ball, platform, "\n" "score:", score, "\n""best score: ", best_score)
                return ball, platform, score, best_score


def draw_game(ball, platform, score, best_score):
    screen.fill(BLACK)
    global width
    global height
    # Розміри ігрового поля як пропорція від розмірів екрану

    game_width = (width * 16) * 0.9
    game_height = (height * 16) * 0.9

    # Розрахунок зсуву для центрованого поля
    offset_x = (WIDTH - game_width) // 2
    offset_y = (HEIGHT - game_height) // 2

    # Товщина ліній ігрового поля
    border_thickness = max(3, min(WIDTH, HEIGHT) // 200)

    # Малюємо рамки навколо ігрового поля
    pygame.draw.line(screen, WHITE, (offset_x + 52, offset_y + 45), ((offset_x + game_width) - 52, offset_y + 45),
                     border_thickness)  # Верхня лінія
    pygame.draw.line(screen, WHITE, (offset_x + 52, offset_y + 45), (offset_x + 52, (offset_y + game_height) - 150),
                     border_thickness)  # Ліва лінія
    pygame.draw.line(screen, WHITE, ((offset_x + game_width) - 52, offset_y + 45),
                     ((offset_x + game_width) - 52, (offset_y + game_height) - 150), border_thickness)  # Права лінія
    pygame.draw.line(screen, WHITE, (offset_x + 52, (offset_y + game_height) - 150),
                     ((offset_x + game_width) - 52, (offset_y + game_height) - 150), border_thickness)  # Нижня лінія

    # Малюємо м'яч
    ball_size = max(10, min(WIDTH, HEIGHT) // 50)  # Динамічний розмір м'яча
    ball_x = offset_x + (game_width - ball_size * len(ball)) // 6 + ball[0] * ball_size
    ball_y = offset_y + (game_height - ball_size * len(ball)) // 15 + ball[1] * ball_size
    pygame.draw.rect(screen, WHITE, (ball_x, ball_y, ball_size, ball_size))

    # Малюємо платформу
    platform_width = ball_size  # Ширина сегмента платформи відповідає розміру м'яча
    platform_height = int(ball_size * 0.8)  # Висота платформи трохи менша за її ширинуф
    platform_y_position = offset_y + (
                game_height - platform_height) // 2 + game_height - platform_height - border_thickness  # Позиція платформи

    for i in range(5):  # Платформа з 4-х сегментів6
        pygame.draw.rect(screen, WHITE, (
        (((platform * 9) + 3) + i * 10) + 70, platform_y_position - 443, platform_width, platform_height))

    # Додаємо текст під ігровим полем
    text = FONT2.render("Controls:", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, 480))
    screen.blit(text, text_rect)
    text = FONT2.render("Space - start game", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, 500))
    screen.blit(text, text_rect)
    text = FONT2.render("A - left", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, 520))
    screen.blit(text, text_rect)
    text = FONT2.render("D - right", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, 540))
    screen.blit(text, text_rect)
    text = FONT2.render("P - pause", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, 560))
    screen.blit(text, text_rect)
    text = FONT2.render("R - restart", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, 580))
    screen.blit(text, text_rect)
    text = FONT2.render("ESC - Exit", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, 600))
    screen.blit(text, text_rect)
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, 33))
    screen.blit(score_text, score_rect)
    best_score_text = FONT3.render(f"Best score: {best_score}", True, WHITE)
    best_score_rect = score_text.get_rect(center=((WIDTH // 2) + 20, 70))
    screen.blit(best_score_text, best_score_rect)
    pygame.display.flip()


def main():
    global pause

    menu_music.play(loops=-1)
    com_port = select_com_port()
    if not com_port:
        return
    try:
        ser = init_serial(com_port)
    except serial.SerialException:
        show_error_message("Invalid\nCOM Port\nSelected!", ser)
        return
    try:
        game = select_game(ser)
    except serial.SerialException:
        menu_music.stop()
        game_music.stop()
        main()
    if game:
        menu_music.stop()
        game_music.play(loops=-1)
        send_initial_command(ser)  # Відправка першої команди для старту гри
        while True:
            try:
                data = receive_game_data(ser)
            except serial.SerialException:
                game_music.stop()
                menu_music.stop()
                main()
            if data:
                draw_game(*data)
            pause = 1
            BCC = calculate_bcc([0x04, 160])
            packet = bytes([0x04, 160, BCC])
            ser.write(packet)
            while True:
                if pause == 0:
                    try:
                        data = receive_game_data(ser)
                    except serial.SerialException:
                        game_music.stop()
                        menu_music.stop()
                        main()
                if data:
                    draw_game(*data)
                keys = pygame.key.get_pressed()
                key_value = None
                if keys[pygame.K_a]:
                    key_value = 141
                elif keys[pygame.K_d]:
                    key_value = 144
                elif keys[pygame.K_r]:
                    BCC = calculate_bcc([0x04, 162])
                    packet = bytes([0x04, 162, BCC])
                    ser.write(packet)
                    time.sleep(0.1)
                    pause = 1
                elif keys[pygame.K_p]:  # Керування паузою
                    key_value = 160
                    pause = 1 if pause == 0 else 0
                    print(f"Pause: {pause}")
                elif keys[pygame.K_SPACE]:
                    key_value = 13
                elif keys[pygame.K_ESCAPE]:
                    BCC = calculate_bcc([0x04, 162])
                    packet = bytes([0x04, 162, BCC])
                    ser.write(packet)
                    BCC = calculate_bcc([0x04, 33])
                    packet = bytes([0x04, 33, BCC])
                    ser.write(packet)
                    ser.close()
                    menu_music.stop()
                    game_music.stop()
                    main()
                if key_value is not None:
                    BCC = calculate_bcc([0x04, key_value])
                    packet = bytes([0x04, key_value, BCC])
                    ser.write(packet)
                    print(packet)

                time.sleep(0.01)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        ser.close()
                        return
                # Під час паузи чекаємо на натискання `SPACE`
                while pause:
                    game_music.stop()
                    time.sleep(0.1)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            ser.close()
                            return
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            game_music.play(loops=-1)
                            BCC = calculate_bcc([0x04, 13])
                            packet = bytes([0x04, 13, BCC])
                            ser.write(packet)
                            pause = 0
                            print("Game Resumed!")
                            break  # Виходимо з циклу після відновлення гри
                    clock.tick(30)

    pygame.quit()
    ser.close()


if __name__ == "__main__":
    main()