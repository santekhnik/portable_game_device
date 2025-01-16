#include "stm32f4xx_hal.h"
#include <string.h> // Для роботи зі строками

#define SCREEN_WIDTH  20
#define SCREEN_HEIGHT 10
#define PLATFORM_WIDTH 4

UART_HandleTypeDef huart2; // UART2 для виводу

int ball_x = 10;  // Початкова позиція м'яча по X
int ball_y = 8;   // Початкова позиція м'яча по Y
int ball_dx = 1;  // Напрямок руху м'яча по X
int ball_dy = 1;  // Напрямок руху м'яча по Y

int platform_x = 8; // Позиція платформи
int platform_y = SCREEN_HEIGHT - 2;

char screen[SCREEN_HEIGHT][SCREEN_WIDTH]; // Екран гри
char uart_buffer[128]; // Буфер для виводу через UART

// Ініціалізація UART
void UART_Init(void) {
    __HAL_RCC_USART2_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();

    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_2 | GPIO_PIN_3; // PA2 - TX, PA3 - RX
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF7_USART2;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    huart2.Instance = USART2;
    huart2.Init.BaudRate = 115200;
    huart2.Init.WordLength = UART_WORDLENGTH_8B;
    huart2.Init.StopBits = UART_STOPBITS_1;
    huart2.Init.Parity = UART_PARITY_NONE;
    huart2.Init.Mode = UART_MODE_TX_RX;
    huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    HAL_UART_Init(&huart2);
}

// Функція для виводу тексту через UART
void UART_SendString(char *str) {
    HAL_UART_Transmit(&huart2, (uint8_t *)str, strlen(str), HAL_MAX_DELAY);
}

// Оновлення логіки гри
void update_game() {
    memset(screen, ' ', sizeof(screen));

    ball_x += ball_dx;
    ball_y += ball_dy;

    if (ball_x <= 1 || ball_x >= SCREEN_WIDTH - 2) {
        ball_dx = -ball_dx;
    }
    if (ball_y <= 1) {
        ball_dy = -ball_dy;
    }

    if (ball_y == platform_y && ball_x >= platform_x && ball_x < platform_x + PLATFORM_WIDTH) {
        ball_dy = -ball_dy;
    }

    if (ball_y > platform_y) {
        sprintf(uart_buffer, "Game Over!\n");
        UART_SendString(uart_buffer);
        ball_x = 10;
        ball_y = 8;
        ball_dx = 1;
        ball_dy = 1;
    }

    screen[ball_y][ball_x] = 'O';

    for (int i = 0; i < PLATFORM_WIDTH; i++) {
        screen[platform_y][platform_x + i] = '=';
    }

    for (int x = 0; x < SCREEN_WIDTH; x++) {
        screen[0][x] = '_';
    }
    for (int y = 1; y < SCREEN_HEIGHT; y++) {
        screen[y][0] = '|';
        screen[y][SCREEN_WIDTH - 1] = '|';
    }
}

// Виведення екрану через UART
void render_screen() {
    sprintf(uart_buffer, "\033[H\033[J"); // Очистка терміналу
    UART_SendString(uart_buffer);

    for (int y = 0; y < SCREEN_HEIGHT; y++) {
        for (int x = 0; x < SCREEN_WIDTH; x++) {
            sprintf(uart_buffer, "%c", screen[y][x]);
            UART_SendString(uart_buffer);
        }
        UART_SendString("\n");
    }
    UART_SendString("Use 'a' to move left, 'd' to move right\n");
}

// Обробка введення
void process_input(char command) {
    if (command == 'a' && platform_x > 1) {
        platform_x -= 2;
    } else if (command == 'd' && platform_x < SCREEN_WIDTH - PLATFORM_WIDTH - 1) {
        platform_x += 2;
    }
}

int main(void) {
    HAL_Init();
    SystemClock_Config();
    UART_Init();

    char input;
    while (1) {
        update_game();
        render_screen();

        if (HAL_UART_Receive(&huart2, (uint8_t *)&input, 1, 100) == HAL_OK) {
            process_input(input);
        }

        HAL_Delay(100);
    }
}
