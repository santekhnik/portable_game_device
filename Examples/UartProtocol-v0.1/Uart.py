import serial
import time

# Відкриваємо серійний порт
ser = serial.Serial('COM16', 115200, timeout=1)


def calculate_bcc(data):
    checksum = 0
    for value in data:
        checksum ^= value
    return checksum


def send(arr):
    # Відправляємо дані на STM32
    ser.write(arr)
    time.sleep(0.5)  # Чекаємо, поки STM32 обробить запит


def read_response():
    # Перевіряємо, чи є дані для читання
    if ser.in_waiting > 0:
        response = ser.read(ser.in_waiting)  # Читаємо всі доступні байти
        return response
    return None


if __name__ == "__main__":
    arr = [1, 6]  # Список байтів для передачі
    bcc = calculate_bcc(arr)  # Обчислення контрольної суми
    arr.append(bcc)  # Додаємо контрольну суму до масиву

    print("Checksum:", hex(bcc))
    print("Data to send:", [hex(x) for x in arr])  # Переведемо байти в hex для кращого вигляду

    # Відправляємо перші дані


    while True:
        print("Response from STM32:", read_response())
        ser.write(arr)
        time.sleep(0.5)

        time.sleep(0.1)  # Затримка перед наступною перевіркою
