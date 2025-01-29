import serial
import time

# Відкриваємо серійний порт
ser = serial.Serial('COM15', 115200, timeout=1)


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
    arr = [1, 0]  # Список байтів для передачі
    arr1 = [2,14,0,0]
    bcc = calculate_bcc(arr)  # Обчислення контрольної суми
    bcc1 = calculate_bcc(arr1)  # Обчислення контрольної суми
    arr.append(bcc)  # Додаємо контрольну суму до масиву
    arr1.append(bcc1)  # Додаємо контрольну суму до масиву

    print("Checksum:", hex(bcc))
    print("Data to send:", [hex(x) for x in arr1])  # Переведемо байти в hex для кращого вигляду

    # Відправляємо перші дані

    I=1
    ser.write(arr1)
    while (I==1):
        time.sleep(0.1)
        print("Response from STM32:", read_response())