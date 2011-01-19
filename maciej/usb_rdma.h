// Poor man's RDMA-over-USB driver, designed to work with Xilinx SP605 kit connected to the PC via USB serial port.

#ifndef __USB_RDMA_H
#define __USB_RDMA_H


// initializes the interface.
int pdma_init();

// performs single 32-bit write on wishbone bus
int pdma_write(uint32_t addr, uint32_t data);

// single wb 32-bit read
uint32_t pdma_read(uint32_t addr);

// multiple (length times) 32-bit withbone reads
int pdma_read_multi(uint32_t addr, uint32_t *data, int length);

#endif

