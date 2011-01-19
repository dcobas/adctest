#ifndef __ADC_STUFF_H
#define __ADC_STUFF_H

#include <inttypes.h>

typedef struct  {
 int ch1, ch2, ch3, ch4;
} sample_t;

#define ADC_RANGE_100mV 0
#define ADC_RANGE_1V 	  1
#define ADC_RANGE_10V 	2
#define ADC_OFFSET_CAL  3


void adc_record(sample_t *buf, int samples, int pre_trigger);
void adc_set_offset(int channel, int offset);
void adc_set_range(int channel, int range, int term_50ohm);
int adc_init();

#endif
