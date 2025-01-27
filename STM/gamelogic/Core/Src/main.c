/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "stm32f0xx_hal.h"
#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#include "math.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
UART_HandleTypeDef huart1;
DMA_HandleTypeDef hdma_usart1_rx;
DMA_HandleTypeDef hdma_usart1_tx;

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/

void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_DMA_Init(void);
static void MX_USART1_UART_Init(void);

/* USER CODE BEGIN PFP */
int Get_float(float number);
int calculateBCC(uint8_t *data, int length, bool get);
void Check_Protocol();
void game_control(void);
void reset_game(void);
void update_game(void);
void send_game_state(void);
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int SCREEN_WIDTH = 40;
int const SCREEN_HEIGHT = 20;
int PLATFORM_WIDTH = 4;

float ball_x = 8;
float ball_y = 8;
float ball_dx = 0.5;
float ball_dy = 0.5;

float platform_x = 6;
float platform_y = SCREEN_HEIGHT - 4;
bool game_over = 0;
bool paused = 0;  // Paused default status
int game_type = 0;  // 0 - Pong, 1 - Snake
bool connect_req = 0;
bool game_req=0;
bool ISR=0;
bool *ptrPaused = &paused;
uint8_t msg_rx[16];
uint8_t msg_tx[128];


void HAL_UARTEx_RxEventCallback(UART_HandleTypeDef *huart, uint16_t Size){ 
	ISR=1; 
}



//  ----------------------------------------------------------------------- S_MAIN -----------------------------------------------------------------------
int main(void) {
	  HAL_Init();
    SystemClock_Config();
    MX_USART1_UART_Init();

		HAL_UARTEx_ReceiveToIdle_IT(&huart1, msg_rx, 16);
    while (1) {
			
			if(ISR){		
				Check_Protocol();
				ISR=0;
			}
			
			else{
				HAL_UARTEx_ReceiveToIdle_IT(&huart1, msg_rx, 16);
			}
			
      if(!paused) {
        send_game_state();
				update_game();
				HAL_Delay(50);
     }

}

}

// --------------------------------------------------------------------------------------------------------------------------------------------------




// ----------------------------------------------------------------------- S_STM -----------------------------------------------------------------------
/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_USART1;
  PeriphClkInit.Usart1ClockSelection = RCC_USART1CLKSOURCE_PCLK1;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief USART1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART1_UART_Init(void)
{

  /* USER CODE BEGIN USART1_Init 0 */

  /* USER CODE END USART1_Init 0 */

  /* USER CODE BEGIN USART1_Init 1 */

  /* USER CODE END USART1_Init 1 */
  huart1.Instance = USART1;
  huart1.Init.BaudRate = 115200;
  huart1.Init.WordLength = UART_WORDLENGTH_8B;
  huart1.Init.StopBits = UART_STOPBITS_1;
  huart1.Init.Parity = UART_PARITY_NONE;
  huart1.Init.Mode = UART_MODE_TX_RX;
  huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart1.Init.OverSampling = UART_OVERSAMPLING_16;
  huart1.Init.OneBitSampling = UART_ONE_BIT_SAMPLE_DISABLE;
  huart1.AdvancedInit.AdvFeatureInit = UART_ADVFEATURE_NO_INIT;
  if (HAL_UART_Init(&huart1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART1_Init 2 */

  /* USER CODE END USART1_Init 2 */

}

/**
  * Enable DMA controller clock
  */
static void MX_DMA_Init(void)
{

  /* DMA controller clock enable */
  __HAL_RCC_DMA1_CLK_ENABLE();

  /* DMA interrupt init */
  /* DMA1_Channel2_3_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(DMA1_Channel2_3_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(DMA1_Channel2_3_IRQn);

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
/* USER CODE BEGIN MX_GPIO_Init_1 */
/* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOF_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();

/* USER CODE BEGIN MX_GPIO_Init_2 */
/* USER CODE END MX_GPIO_Init_2 */
}



// ---------------------------------------------------------------------------------------------------------------------------------------------------










/* //  ----------------------------------------------------------------------- FUNCTIONS -----------------------------------------------------------------------  */

void Check_Protocol(){ // Protocol --------------------------------------------------------------------------------

	switch((int)msg_rx[0]){
		 
		 
		 
		case(0x01): // MENU SELECT

				if(calculateBCC(msg_rx, 3, 0 ) && !(int)msg_rx[1]){
					// NEED TO MAKE CYCLE FOR LIST OF GAMES (BLALALA BLYLYLYL)
					  connect_req =1; // CONNECT ALLOW
						msg_tx[0]=0x01;
						msg_tx[1]=0x01;
						msg_tx[2]=0x14;
						msg_tx[3]=calculateBCC(msg_tx, 4,1);
			      HAL_UART_Transmit_IT(&huart1, msg_tx, 4);
			      game_req =0;}
				else{
						msg_tx[0]=0x01;
						msg_tx[1]=0xFF;
						msg_tx[2]=0xFF;
						msg_tx[3]=calculateBCC(msg_tx, 4,1);		
						HAL_UART_Transmit(&huart1, msg_tx, 4 , 0xFFFF);}
			break;
		
		case(0x02): // GAME SELECT

		    if(calculateBCC(msg_rx, 5, 0 )){ // CHECK CORRECT BCC	
					
					
					if( !game_req && ( (int)msg_rx[1] == 0x0E) &&( !(int)msg_rx[2] && !(int)msg_rx[3]))  {// PC choosing game (XX-number of game)--------------------------
						msg_tx[0]=0x02;
						msg_tx[1]=0x0E;
						msg_tx[2]=SCREEN_WIDTH;
						msg_tx[3]=SCREEN_HEIGHT;
						msg_tx[4] =calculateBCC(msg_tx, 5,1);	
						HAL_UART_Transmit(&huart1,msg_tx,5,0xFFFF); // NEED REMAKE STM > PC     X_S/Y_S - size of map
					  send_game_state();
					  game_req =1;
					  
						
									 
					}
					else if((int)msg_rx[1] != 0x0E){ // NOT CORRECT GAME 
						msg_tx[0]=0x02;
						msg_tx[1]=0xDD;
						msg_tx[2]=0xFF;
						msg_tx[3]=calculateBCC(msg_tx, 4,1);
			      HAL_UART_Transmit(&huart1, msg_tx, 4 , 0xFFFF);
					}
			
					}
				else {    // BCC ERROR
					
						msg_tx[0]=0x02;
						msg_tx[1]=0xFF;
						msg_tx[2]=0xFF;
						msg_tx[3]=calculateBCC(msg_tx, 4,1);
			      HAL_UART_Transmit(&huart1, msg_tx, 4 , 0xFFFF);				
				}
				
			break;	
		
		
		

		case(0x04):
			game_control();
			//recive control key
			break;
			
			
		

		

	
		break;
 }
}


int Get_float(float number){ // FIXED POINT NUMBER GET _-----------------------------------------------------------
    return ((int)number==number) ?  (( (int)number << 1 ) | 0) : (( (int)number << 1 ) | 1) ;
};



int calculateBCC(uint8_t *data, int length, bool get) {// BCC CALCULATION 1-true 0-false	
	
   int checksum = 0;
	if(!get){
			
    for (int i = 0; i < length-1; i++)
    {
        checksum ^= (int)data[i];
	

				
    }
	
		if(	checksum == data[length-1]){
    return 1;
		}
		else{
			return 0;
		}
	}
	else if(get) {

		  for (int i = 0; i < length-1; i++)
    {
        checksum ^= (int)data[i];
			
    }

	

	
		
	}
		return checksum;
}


void game_control(){ // GET KEY FROM USERS --------------------------------------
		if (msg_rx[1] == 'a' && !paused && platform_x > 1) {
            platform_x -= 1;
			}
		else if ((char)msg_rx[1] == 'd' && !paused && platform_x < SCREEN_WIDTH - PLATFORM_WIDTH - 1) {
            platform_x += 1;
      }
		else if (((char)msg_rx[1] == 'r') && !paused ){
					reset_game();
			}
		else if ((char)msg_rx[1] == 'p'){
					paused = 1; // Toggle pause state
			}
		else if((int)msg_rx[1] ==13){

        paused = 0;

    }			
		else if((int)msg_rx[1] == 33){ // ASCII 033 = ESC
				 msg_tx[0] = 0x01;
				 msg_tx[1] = 0x01;
				 msg_tx[2] = calculateBCC(msg_tx, 3, 1);
				 HAL_UART_Transmit(&huart1, msg_tx, 3 , 0xFFFF);
		     game_req=0;
			}
				 
					 
					msg_tx[0] = 0x03;
					msg_tx[1] = ball_x;
					msg_tx[2] = ball_y;
					msg_tx[3] = platform_x;
					msg_tx[4] = platform_y;
					msg_tx[5] = calculateBCC(msg_tx, 8, 1);

        HAL_UART_Receive_IT(&huart1, msg_rx, 1);
					 
}







void reset_game() { // GAME RESET -----------------------------------------------
    ball_x = 8;
    ball_y = 8;
    platform_x = 6;
    platform_y = SCREEN_HEIGHT - 4;
    game_over = 0;
}



void update_game() { // UPDATE GAME STATE ----------------------------------------
    if (!game_over) {
        ball_x += ball_dx;
        ball_y += ball_dy;

        if (ball_x <= 1 || ball_x >= SCREEN_WIDTH - 2) {
            ball_dx = -ball_dx;
        }
        if (ball_y <= 1) {
            ball_dy = -ball_dy;
        }

        if (ball_y == (platform_y) && ball_x >= platform_x && ball_x < platform_x + PLATFORM_WIDTH) {
            ball_dy = -ball_dy;
        }

        if (ball_y > (platform_y)) {
            game_over = 1;
        }
    } else {
        reset_game();
    }
}





void send_game_state() { // SEND COORDINATES -------------------------------------
    				msg_tx[0]=0x03;
						msg_tx[1]=Get_float(ball_x);
						msg_tx[2]=Get_float(ball_y);
	          msg_tx[3]=platform_x;
	          msg_tx[4]=platform_y;
	          msg_tx[5]=calculateBCC(msg_tx, 6,1);
						HAL_UART_Transmit(&huart1, msg_tx, 6, 0xFFFF);
		       
	        
}











































///* //  ----------------------------------------------------------------------- CONFIGURATION -----------------------------------------------------------------------  


/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
