#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

#include "fpga_regs.h"
#include "adctl_regs.h"

#include "usb_rdma.h"
#include "adc_stuff.h"

int cal_offsets[4] = {-1, -1, -1, -1};

void gpio_set_dir(int pin, int output)
{
	uint32_t ddr = pdma_read(BASE_GPIO + GPIO_REG_DDR);
	if(output) ddr |= (1<<pin); else ddr &= ~(1<<pin);
	pdma_write(BASE_GPIO + GPIO_REG_DDR, ddr);
}

void gpio_set_state(int pin, int state)
{
 if(state)
   pdma_write(BASE_GPIO + GPIO_REG_SODR, (1<<pin));
 else
	 pdma_write(BASE_GPIO + GPIO_REG_CODR, (1<<pin));
}

// I2C master functions

void i2c_init(uint32_t base_addr)
{
  const int prescaler = 200;

	pdma_write(base_addr + I2C_REG_PRER_HI, (prescaler >> 8) & 0xff);
	pdma_write(base_addr + I2C_REG_PRER_LO, prescaler & 0xff);
  pdma_write(base_addr + I2C_REG_CTR, I2C_CTR_EN);
}

uint32_t i2c_wait_busy(uint32_t base_addr)
{
 uint32_t sr;
		do {
		  sr = pdma_read(base_addr + I2C_REG_SR);
		} while(sr & I2C_SR_TIP);
 return sr;
}

void i2c_scan_bus(uint32_t base_addr)
{
  int i, ack;
  uint32_t sr;
  
  for(i=0; i<256; i+=2)
  {
		pdma_write(base_addr + I2C_REG_TXR, i | 1);
		
		pdma_write(base_addr + I2C_REG_CR, I2C_CR_STA | I2C_CR_WR);
		
		sr = i2c_wait_busy(base_addr);
		ack = !(sr & I2C_SR_RXACK);
		
		if(ack)
		{
		  fprintf(stderr,"Device found at address 0x%x\n", i);
	
			pdma_write(base_addr + I2C_REG_TXR, 0);
			pdma_write(base_addr + I2C_REG_CR, I2C_CR_STO | I2C_CR_WR);
		i2c_wait_busy(base_addr);
	
		}
		
	}

}

int i2c_write(uint32_t base_addr, uint8_t dev_addr, uint8_t *data, int length)
{

}

int i2c_read(uint32_t base_addr, uint8_t dev_addr, uint8_t *data, int length)
{

}

// SPI functions

int spi_init()
{
	pdma_write(BASE_SPI + SPI_REG_DIVIDER, 1000);
}

// ADC stuff

int ltc2175_txrx(uint16_t in, uint16_t *out)
{
	pdma_write(BASE_SPI + SPI_REG_CTRL, SPI_CTRL_ASS | SPI_CTRL_CHAR_LEN(16) | SPI_CTRL_TXNEG);
	pdma_write(BASE_SPI + SPI_REG_TX0, in);
	pdma_write(BASE_SPI + SPI_REG_SS, SPI_SS_ADCORE);
	pdma_write(BASE_SPI + SPI_REG_CTRL, SPI_CTRL_ASS | SPI_CTRL_CHAR_LEN(16) | SPI_CTRL_TXNEG | SPI_CTRL_GO_BSY);

  while(pdma_read(BASE_SPI + SPI_REG_CTRL) & SPI_CTRL_GO_BSY);
  
  *out = pdma_read(BASE_SPI +SPI_REG_RX0);
  return 0;
}

uint8_t ltc2175_read_reg(uint8_t reg)
{
 uint16_t rval;
 ltc2175_txrx(0x8000 | (((uint16_t)reg)<<8) | 0xff, &rval);
 return rval & 0xff;
}

void ltc2175_write_reg(uint8_t reg, uint8_t value)
{
 uint16_t rval;
 ltc2175_txrx( (((uint16_t)reg)<<8) | value, &rval);
 
// printf("%x - %x\n", value, ltc2175_read_reg(reg));
}

void ltc2175_init()
{
  ltc2175_write_reg(LTC2175_REG_RESET, LTC2175_RESET);
  ltc2175_write_reg(LTC2175_REG_FMT, 0); 
  ltc2175_write_reg(LTC2175_REG_OUTMODE, LTC2175_OUTMODE_ILVDS_4m5  | LTC2175_OUTMODE_TERMON | LTC2175_OUTMODE_2L_16B); 
//  ltc2175_write_reg(LTC2175_REG_TESTPAT_LSB, 0x02 ); // d1,3,5,7 = 
//  ltc2175_write_reg(LTC2175_REG_TESTPAT_MSB, 0x00 | LTC2175_TESTPAT_MSB_OUTTEST);
}



void adc_record(sample_t *buf, int samples, int pre_trigger)
{
	uint32_t buf_raw[1024];
  uint32_t sta;
  int i = 0, idx = 0;
  
	pdma_write(BASE_ADCORE + ADCORE_IOREGS + ADCTL_REG_CTL, ADCTL_CTL_SAMPLES_W(samples) | ADCTL_CTL_TRIG_CLR);
	pdma_write(BASE_ADCORE + ADCORE_IOREGS + ADCTL_REG_SWTRIG, 0xffffffff);
	
  do {
 	 sta =  pdma_read(BASE_ADCORE + ADCORE_IOREGS + ADCTL_REG_STA);
 	} while (!(sta & ADCTL_STA_DONE));
 	
  int offset = (ADCTL_STA_TRIG_POS_R(sta) - pre_trigger) * 2;
	
	if(offset < 0) offset += 32768;

	int total = (samples+pre_trigger) * 2;
	int tocopy;
  while(total > 0) {

//		fprintf(stderr,"total = %d tocopy = %d\n", total, tocopy);

 	  if(total > 254)
 	 		tocopy = 254;
 	  else
 	 		tocopy = total;
 	 
		 if(offset == 0x8000) offset = 0;
 		if(offset + tocopy > 32768) 
 		  tocopy = 32768 - offset;
 
 
		//printf("copy %d offset %d\n", tocopy, offset);
 		
 		pdma_read_multi(offset, buf_raw, tocopy);
	
	    offset+=tocopy;
		for(i=0;i<tocopy/2;i++)
		{
			buf[idx].ch2 = (buf_raw[2*i] >> 16)>>2;
			buf[idx].ch1 = (buf_raw[2*i] & 0xffff)>>2;
			buf[idx].ch4 = (buf_raw[2*i+1] >> 16)>>2;
			buf[idx].ch3 = (buf_raw[2*i+1] & 0xffff)>>2;
			idx++;
		}
 		total-= tocopy;
  } 
}


static void adc_calibrate_serdes()
{
  sample_t buf[100];
	uint16_t ch3_val, ch4_val;	

// here's how the serdes "calibration" works:

// send a test pattern with D1 bit set to 1 making the LSB of OUTA3 = 1 (so the data output on channel 3 == 0x4). 

  ltc2175_write_reg(LTC2175_REG_TESTPAT_LSB, 0x02 ); // d1,3,5,7 = 
  ltc2175_write_reg(LTC2175_REG_TESTPAT_MSB, 0x00 | LTC2175_TESTPAT_MSB_OUTTEST);
	
  do {

// now, keep shifting the Left-half sedreses by 1 bit until the CH4 measurement is equal to CH3 (so the test pattern bit D1 gets on the same position in both channels)
   	pdma_write(BASE_ADCORE + ADCORE_IOREGS + ADCTL_REG_CTL, ADCTL_CTL_BSLIP_L);
   	
    adc_record(buf, 11, 0);
        
    ch3_val = buf[10].ch3;
    ch4_val = buf[10].ch4;
    
  } while(ch3_val != ch4_val);

// voila!
// ps. needs to be done every time the ADC sampling clock is changed
  ltc2175_write_reg(LTC2175_REG_TESTPAT_MSB, 0x00); // disable pattern generation

}

void adc_set_offset(int channel, int offset)
{
	pdma_write(BASE_SPI + SPI_REG_CTRL, SPI_CTRL_ASS | SPI_CTRL_CHAR_LEN(16) | SPI_CTRL_TXNEG);

    if(cal_offsets[channel - 1] >= 0)
    {
        offset += cal_offsets[channel - 1];
        fprintf(stderr, "SetOffset:%d\n", offset);
    }

	pdma_write(BASE_SPI + SPI_REG_TX0, offset);
	pdma_write(BASE_SPI + SPI_REG_SS, SPI_SS_DAC(channel));
	pdma_write(BASE_SPI + SPI_REG_CTRL, SPI_CTRL_ASS | SPI_CTRL_CHAR_LEN(16) | SPI_CTRL_TXNEG | SPI_CTRL_GO_BSY);

  while(pdma_read(BASE_SPI + SPI_REG_CTRL) & SPI_CTRL_GO_BSY);
}

#define PIN_SSR(channel, ssr) (((ssr-1)+ ((channel-1)*7)))


void adc_set_range(int channel, int range, int term_50ohm)
{
	int swmap[4][7] = {{ 1, 1, 0, 0, 0, 1, 0}, // 100 mV
									   { 1, 0, 0, 0, 1, 0, 0},  // 1V
									   { 1, 0, 1, 0, 0, 0, 1},  // 10V
									   { 0, 0, 0, 0, 0, 0, 1}}; // offset calibration
	int i;


//    fprintf(stderr, "SetRange: ch %d range %d term %d", channel, range, term_50ohm);
    
    

	if(range >= 0 && range <= 3)
	{
		for(i=0;i<7;i++)
		{
			gpio_set_dir(PIN_SSR(channel, i+1), 1);
			gpio_set_state(PIN_SSR(channel, i+1), swmap[range][i]);
	  }
	}
	gpio_set_dir(PIN_SSR(channel, 4), 1);
	gpio_set_state(PIN_SSR(channel, 4), term_50ohm);

}

void adc_record_single(int channel, int *buf, int samples, int pre_trigger)
{
	sample_t tmp[32768];
	int i;
	
	adc_record(tmp, samples, pre_trigger);
	
	for(i=0;i<samples+pre_trigger+1; i++)
	{
		switch(channel)
		{
			case 1: buf[i] = tmp[i].ch1; break;
			case 2: buf[i] = tmp[i].ch2; break;
			case 3: buf[i] = tmp[i].ch3; break;
			case 4: buf[i] = tmp[i].ch4; break;
		}
	}
}


#define PIN_LED_TOP 30
#define PIN_LED_BOT 31
#define PIN_DAC_RST 28
#define PIN_CLK_EN 29



static void adc_calibrate_offset(int channel)
{
    int current_offset = 33000;
    int prev_offset = 32000;
    int buf[10];
    int i;
    int error;
    int prev_error;
    
    adc_set_range(channel, ADC_OFFSET_CAL, 0);
    adc_set_offset(channel, prev_offset);
    adc_record_single(channel, buf, 10, 0);
    prev_error = buf[5] - 8192;

    fprintf(stderr,"Calibrating offset for channel %d\n", channel);
    
    for(i=0;i<128;i++)
    {
//        adc_set_range(channel, ADC_OFFSET_CAL, 0);
        adc_set_offset(channel, current_offset);

        adc_record_single(channel, buf, 10, 0);
        error = buf[5] - 8192;
       
        fprintf(stderr, "Step %d offset %d error %d preverror %d\n", i, current_offset, error, prev_error);
        
        current_offset += 0.03 * (error);
     
        prev_offset = current_offset;
        prev_error = error;
    }

    fprintf(stderr,"Ch3 offset = %d\n", current_offset);
    cal_offsets[channel - 1] = current_offset;
}

int adc_init()
{

 pdma_init();

/* printf("[i2c] initializing bus CLKGEN.\n");
 i2c_init(BASE_I2C_CLKGEN);
 i2c_scan_bus(BASE_I2C_CLKGEN);

 printf("[i2c] initializing bus  IDMEM.\n");
 i2c_init(BASE_I2C_IDMEM);
 i2c_scan_bus(BASE_I2C_IDMEM);
*/

 spi_init();
 ltc2175_init();
 adc_calibrate_serdes();

 gpio_set_dir(PIN_DAC_RST, 1);
 gpio_set_state(PIN_DAC_RST, 1);
 
// adc_calibrate_offset(3);
// adc_calibrate_offset(4);
}


