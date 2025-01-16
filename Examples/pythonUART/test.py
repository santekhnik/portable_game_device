import serial
import time

# Відкриваємо серійний порт
ser = serial.Serial('COM5', 115200, timeout=1)

# Функція для відправлення пароля та отримання відповіді
def send_password(password):
    # Відправляємо пароль
    ser.write(password.encode())
    time.sleep(0.5)  # Чекаємо, поки STM32 обробить запит
    # Читаємо відповідь
    response = ser.read(100)  # Читаємо до 100 байтів
    return response.decode()

# Основний цикл
if __name__ == '__main__':
    password = input("Enter the password: ")
    response = send_password(password)
    print("Response from STM32:", response)

    # Закриваємо серійний порт
    ser.close()
