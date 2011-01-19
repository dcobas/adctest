#ifndef __FPGA_REGS_H
#define __FPGA_REGS_H

#define BASE_ADCORE 0x0
#define BASE_I2C_CLKGEN 0x20000
#define BASE_I2C_IDMEM 0x40000
#define BASE_SPI  0x60000
#define BASE_GPIO  0x80000

#define ADCORE_IOREGS 0x10000
#define ADCORE_MEM 0x0

#define GPIO_REG_CODR 0x0
#define GPIO_REG_SODR 0x1
#define GPIO_REG_PSR 0x3
#define GPIO_REG_DDR 0x2

#define I2C_REG_PRER_LO 0
#define I2C_REG_PRER_HI 1
#define I2C_REG_CTR 2
#define I2C_REG_TXR 3
#define I2C_REG_RXR 3
#define I2C_REG_CR 4
#define I2C_REG_SR 4

#define I2C_CTR_EN 0x80
#define I2C_CTR_IEN 0x40

#define I2C_CR_STA 0x80
#define I2C_CR_STO 0x40
#define I2C_CR_RD 0x20
#define I2C_CR_WR 0x10
#define I2C_CR_ACK 0x8
#define I2C_CR_IACK 0x1

#define I2C_SR_RXACK 0x80
#define I2C_SR_BUSY 0x40
#define I2C_SR_AL 0x20
#define I2C_SR_TIP 0x2
#define I2C_SR_IF 0x1

#define SPI_REG_RX0 0
#define SPI_REG_RX1 4
#define SPI_REG_RX2 8
#define SPI_REG_RX3 12
#define SPI_REG_TX0 0
#define SPI_REG_TX1 4
#define SPI_REG_TX2 8
#define SPI_REG_TX3 12

#define SPI_REG_CTRL 16
#define SPI_REG_DIVIDER 20
#define SPI_REG_SS 24

#define SPI_CTRL_ASS (1<<13)
#define SPI_CTRL_IE (1<<12)
#define SPI_CTRL_LSB (1<<11)
#define SPI_CTRL_TXNEG (1<<10)
#define SPI_CTRL_RXNEG (1<<9)
#define SPI_CTRL_GO_BSY (1<<8)
#define SPI_CTRL_CHAR_LEN(x) ((x) & 0x7f)

#define SPI_SS_ADCORE (1<<0)
#define SPI_SS_DAC(x) (1<<(x))

#define LTC2175_REG_RESET 0x0
#define LTC2175_REG_FMT 0x1
#define LTC2175_REG_OUTMODE 0x2
#define LTC2175_REG_TESTPAT_MSB 0x3
#define LTC2175_REG_TESTPAT_LSB 0x4

#define LTC2175_RESET (1<<7)

#define LTC2175_FMT_DCSOFF (1<<7)
#define LTC2175_FMT_RAND (1<<6)
#define LTC2175_FMT_TWOSCOMP (1<<5)
#define LTC2175_FMT_SLEEP (1<<4)
#define LTC2175_FMT_NAP4 (1<<3)
#define LTC2175_FMT_NAP3 (1<<2)
#define LTC2175_FMT_NAP2 (1<<1)
#define LTC2175_FMT_NAP1 (1<<0)

#define LTC2175_OUTMODE_ILVDS_3m5  (0 << 5)
#define LTC2175_OUTMODE_ILVDS_4m0  (1 << 5)
#define LTC2175_OUTMODE_ILVDS_4m5  (2 << 5)
#define LTC2175_OUTMODE_ILVDS_3m0  (4 << 5)
#define LTC2175_OUTMODE_ILVDS_2m5  (5 << 5)
#define LTC2175_OUTMODE_ILVDS_2m1  (6 << 5)
#define LTC2175_OUTMODE_ILVDS_1m75 (7 << 5)

#define LTC2175_OUTMODE_TERMON (1<<4)
#define LTC2175_OUTMODE_OUTOFF (1<<3)

#define LTC2175_OUTMODE_2L_16B (0 << 0)
#define LTC2175_OUTMODE_2L_14B (1 << 0)
#define LTC2175_OUTMODE_2L_12B (2 << 0)

#define LTC2175_OUTMODE_1L_16B (5 << 0)
#define LTC2175_OUTMODE_1L_14B (6 << 0)
#define LTC2175_OUTMODE_1L_12B (7 << 0)

#define LTC2175_TESTPAT_MSB_OUTTEST (1<<7)



#endif

