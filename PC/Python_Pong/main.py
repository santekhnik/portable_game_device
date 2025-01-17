import serial
import json
import time
import keyboard

def init_serial(port="COM5", baudrate=115200):
    return serial.Serial(port, baudrate, timeout=1)

def receive_game_data(ser):
    try:
        line = ser.readline().decode("utf-8").strip()  # Читаємо рядок

        if line:
            return json.loads(line)  # Парсимо JSON
    except (json.JSONDecodeError, UnicodeDecodeError):
        return print("Resiving error")
    return None


def draw_game(ball, platform):
    screen = [[' ' for _ in range(21)] for _ in range(11)]  # Порожнє поле

    # Малюємо межі
    for x in range(21):
        screen[0][x] = '_'  # Верхня межа
    for y in range(11):
        screen[y][0] = '|'  # Ліва межа
        screen[y][20] = '|'  # Права межа

    # Малюємо м'яч
    screen[ball[1]][ball[0]] = 'O'

    # Малюємо платформу
    for i in range(4):
        screen[9][platform[0] + i] = '-'

    # Виводимо поле
    print("\033[H", end="")  # Очищення консолі
    for row in screen:
        print("".join(row))
    print("Use 'a' to move left, 'd' to move right")


def main():
    ser = init_serial()

    while True:
        data = receive_game_data(ser)  # Отримуємо координати з STM32
        if data:
            ball = data["ball"]
            platform = data["platform"]
            draw_game(ball, platform)  # Малюємо гру
        if keyboard.is_pressed('a'):
            command = 'a'
            ser.write(command.encode())
        if keyboard.is_pressed('d'):
            command = 'd'
            ser.write(command.encode())
        time.sleep(0.05)  # Маленька пауза для плавної гри


if __name__ == "__main__":
    main()