import serial
import json
import time
import keyboard
import serial.tools.list_ports


def init_serial(port, baudrate=115200):
    return serial.Serial(port, baudrate, timeout=1)


def receive_game_data(ser):
    try:
        line = ser.readline().decode("utf-8").strip()  # Читаємо рядок

        if line:
            return json.loads(line)  # Парсимо JSON
    except (json.JSONDecodeError, UnicodeDecodeError):
        return print("Receiving error")
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


def show_menu():
    print("Select a game:")
    print("1 - Pong")
    print("2 - Snake")
    print("Press '1' or '2' to select the game.")
    print("Press 'q' to quit.")


def list_com_ports():
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No serial ports found.")
        return None
    print("Select a COM port:")
    for idx, port in enumerate(ports, 1):
        print(f"{idx} - {port.device}")

    while True:
        try:
            choice = int(input("Enter the number of the COM port: "))
            if 1 <= choice <= len(ports):
                return ports[choice - 1].device
            else:
                print("Invalid choice. Please select a valid port number.")
        except ValueError:
            print("Please enter a valid number.")


def main():
    com_port = list_com_ports()
    if not com_port:
        return

    ser = init_serial(com_port)

    while True:
        show_menu()  # Показуємо меню
        while True:
            if keyboard.is_pressed('1'):  # Вибір гри "Понг"
                command = '1'
                ser.write(command.encode())
                print("You selected Pong!")
                break
            elif keyboard.is_pressed('2'):  # Вибір гри "Змійка"
                command = '2'
                ser.write(command.encode())
                print("You selected Snake!")
                break
            elif keyboard.is_pressed('q'):  # Вихід з меню
                print("Quitting...")
                ser.write('q'.encode())
                return
            time.sleep(0.1)  # Затримка для перевірки вводу

        # Основний цикл гри
        while True:
            data = receive_game_data(ser)  # Отримуємо координати з STM32
            if data:
                ball = data["ball"]
                platform = data["platform"]
                draw_game(ball, platform)  # Малюємо гру

            # Керування гравцем
            if keyboard.is_pressed('a'):
                command = 'a'
                ser.write(command.encode())
            elif keyboard.is_pressed('d'):
                command = 'd'
                ser.write(command.encode())
            elif keyboard.is_pressed('r'):
                command = 'r'
                ser.write(command.encode())
            elif keyboard.is_pressed('p'):
                command = 'p'
                ser.write(command.encode())
            time.sleep(0.05)  # Маленька пауза для плавної гри


if __name__ == "__main__":
    main()
