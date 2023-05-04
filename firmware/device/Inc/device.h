/*
 * device.h
 *
 *  Created on: May 4, 2023
 *      Author: ivanc
 */

#ifndef DEVICE_H_
#define DEVICE_H_

#define FIRMWARE_VERSION   	"v1.0"
#define IF_FREQ   			455000
#define TRIPLE_FREQ   		145000000

enum device_command {
	NONE = 0x0,
	GET_FIRMWARE = 0x10,
    SET_FREQ = 0x20,
    READ_DATA = 0x30,
    MEASURE_AT_FREQ = 0x40,
	MEASURE_IN_RANGE = 0x50,
    CALIBRATE_SI5351_FREQ = 0x60,
    STOP_GEN = 0x70,
    FIND_FILTER_MAXIMUM = 0x80
};
void usb_command_parser(void);
void get_firmware(void);
void set_frequency(uint32_t freq);
uint16_t read_adc_data(void);
uint16_t measure_at_freq(uint32_t freq);
void measure_in_range(void);
void stop_generator(void);


#endif /* DEVICE_H_ */
