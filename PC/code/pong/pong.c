#include <stdio.h>
#include <string.h>
#include <conio.h> // Для неблокуючого введення
#include <stdlib.h> // Для system()
#include <windows.h> // Для Sleep()


#define SCREEN_WIDTH  20
#define SCREEN_HEIGHT 10
#define PLATFORM_WIDTH 4

int ball_x = 10;  // Центр по X
int ball_y = 3; // Центр по Y
int ball_dx = 1;       // Напрямок руху м'яча по X
int ball_dy = 1;       // Напрямок руху м'яча по Y

int platform_x = 8;    // Позиція платформи
int platform_y = SCREEN_HEIGHT - 2;

char screen[SCREEN_HEIGHT][SCREEN_WIDTH]; // Екран гри

// Оновлення логіки гри
void update_game() {
    // Очищення екрану
    memset(screen, ' ', sizeof(screen));

    // Рух м'яча
    ball_x += ball_dx;
    ball_y += ball_dy;

    // Відбивання м'яча від стін
    if (ball_x <= 1 || ball_x >= SCREEN_WIDTH - 2) {
        ball_dx = -ball_dx;
    }
    if (ball_y <= 1) {
        ball_dy = -ball_dy;
    }

    // Відбивання м'яча від платформи
    if (ball_y == platform_y && ball_x >= platform_x && ball_x < platform_x + PLATFORM_WIDTH) {
        ball_dy = -ball_dy;
    }

    // Програш (м'яч нижче платформи)
    if (ball_y > platform_y) {
        printf("Game Over!\n");
        ball_x = 10;
        ball_y = 3;
        ball_dx = 1;
        ball_dy = 1;
    }

    // Відображення м'яча
    screen[ball_y][ball_x] = 'O';

    // Відображення платформи
    for (int i = 0; i < PLATFORM_WIDTH; i++) {
        screen[platform_y][platform_x + i] = '-';
    }

    // Додавання границь
    for (int x = 0; x < SCREEN_WIDTH; x++) {
        screen[0][x] = '_';           // Верхня границя
    }
    for (int y = 1; y < SCREEN_HEIGHT; y++) {
        screen[y][0] = '|';           // Ліва границя
        screen[y][SCREEN_WIDTH - 1] = '|'; // Права границя
    }
}

// Виведення екрану
void render_screen() {
    system("cls"); // Очистка терміналу на Windows
    for (int y = 0; y < SCREEN_HEIGHT; y++) {
        for (int x = 0; x < SCREEN_WIDTH; x++) {
            printf("%c", screen[y][x]);
        }
        printf("\n");
    }
    printf("Use 'a' to move left, 'd' to move right\n");
}

// Обробка введення
void process_input(char command) {
    if (command == 'a' && platform_x > 1) { // Рух ліворуч, з урахуванням границі
        platform_x = platform_x - 2;
    } else if (command == 'd' && platform_x < SCREEN_WIDTH - PLATFORM_WIDTH - 1) { // Рух праворуч
        platform_x = platform_x + 2;
    }
}

int main() {
    while (1) {
        // Оновлення логіки гри
        update_game();

        // Відображення екрану
        render_screen();

        // Перевірка на введення
        if (_kbhit()) { // Перевіряє, чи є натиснуті клавіші
            char input = _getch();
            process_input(input);
        }

        Sleep(50); // Затримка 50 мс
    }

    return 0;
}
