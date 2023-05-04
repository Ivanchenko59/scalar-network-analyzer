/*
 * device.c
 *
 *  Created on: May 4, 2023
 *      Author: ivanc
 */

#include "stm32f0xx_hal.h"
#include "device.h"
#include "usbd_cdc_if.h"
#include "si5351.h"

#define ADC_BUFFER_SIZE 10

extern ADC_HandleTypeDef hadc;

uint32_t freq = 0;
uint32_t adc_buffer[10];
uint8_t usb_receive_buffer[64];
uint8_t usb_transmit_buffer[8];
volatile uint8_t adc_data_ready = 0;
volatile uint8_t usb_data_ready = 0;

uint8_t command_identifier = 0;
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc)
{
	adc_data_ready = 1;
}


void usb_command_parser(void)
{
	if (usb_data_ready)
	{
		command_identifier = usb_receive_buffer[0];
		switch (command_identifier)
		{
			case GET_FIRMWARE:
				get_firmware();
				break;

			case SET_FREQ:
				sscanf((char*)usb_receive_buffer, "%*[^;];%lu", &freq);
				set_frequency(freq);
				break;

			case READ_DATA:

				break;

			case MEASURE_AT_FREQ:
				sscanf((char*)usb_receive_buffer, "%*[^;];%lu", &freq);
				uint16_t adc_data = measure_at_freq(freq);
				sprintf((char*)usb_transmit_buffer, "%u\n", adc_data);
				break;

			case MEASURE_IN_RANGE:

				break;

			case CALIBRATE_SI5351_FREQ:

				break;

			case STOP_GEN:

				break;

			case FIND_FILTER_MAXIMUM:

				break;

			default:
				break;
		}
		CDC_Transmit_FS((unsigned char*)usb_transmit_buffer, strlen((char*)usb_transmit_buffer));
		usb_data_ready = 0;
	}
}


void get_firmware(void)
{
	CDC_Transmit_FS((unsigned char*)FIRMWARE_VERSION, strlen(FIRMWARE_VERSION));
}

void set_frequency(uint32_t freq)
{
	if (freq < TRIPLE_FREQ)
	{
		si5351_SetupCLK0(freq, SI5351_DRIVE_STRENGTH_2MA);
		si5351_SetupCLK2(freq+IF_FREQ, SI5351_DRIVE_STRENGTH_2MA);
	}
	else
	{
		si5351_SetupCLK0(freq/3, SI5351_DRIVE_STRENGTH_4MA);
		si5351_SetupCLK2((freq+IF_FREQ)/3, SI5351_DRIVE_STRENGTH_4MA);
	}
}


uint16_t read_adc_data(void)
{
	HAL_ADC_Start_DMA(&hadc, (uint32_t*)adc_buffer, ADC_BUFFER_SIZE);
	while (!adc_data_ready) {}
	adc_data_ready = 0;

	uint32_t adc_sum = 0;
	for (int i = 0; i < ADC_BUFFER_SIZE; ++i) {
		adc_sum += adc_buffer[i];
	}

	return (uint16_t)(adc_sum / ADC_BUFFER_SIZE);
}

uint16_t measure_at_freq(uint32_t freq)
{
	set_frequency(freq);
	HAL_Delay(10);	//wait until frequency will be stable
	uint16_t adc_result = read_adc_data();
	return adc_result;
}

void measure_in_range(void)
{

}


void stop_generator(void)
{
	si5351_SetupCLK0(0, SI5351_DRIVE_STRENGTH_2MA);
	si5351_SetupCLK2(0, SI5351_DRIVE_STRENGTH_2MA);
}
