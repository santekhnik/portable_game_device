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


# Основна програма
if __name__ == "__main__":
    while True:
        try:
            # Введення числа
            user_input = input("Введіть число (може бути цілим або дробовим) або 'exit' для виходу: ")
            if user_input.lower() == "exit":
                print("Завершення програми.")
                break

            # Перетворення введення на число
            value = float(user_input)

            # Кодування числа
            encoded_value = encode_value(value)
            print(f"Вхідне число: {value} -> Закодоване: {bin(encoded_value)}")

            # Розшифрування числа
            decoded_value = decode_value(encoded_value)
            print(f"Закодоване: {bin(encoded_value)} -> Декодоване: {decoded_value}")

        except ValueError:
            print("Помилка: введіть коректне число або 'exit' для виходу.")
