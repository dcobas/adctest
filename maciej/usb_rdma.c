// Poor man's RDMA-over-USB driver
// T.W. 2010

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

#include "serial.h"
#include "usb_rdma.h"

#define SERIAL_DEV "/dev/ttyUSB0"
#define SERIAL_SPEED 460800 //230400


static void pdma_resync()
{
  const uint8_t sync_reply[] = {0xca, 0xfe, 0xba, 0xbe};
	uint8_t buf[4];

 serial_write_byte(0xde);
 serial_write_byte(0xad);
 serial_write_byte(0xbe);
 serial_write_byte(0xef);

  
  for(;;)
	{
//	 usleep(100000); 
	 if(serial_read_timeout(buf, 4, 100000) > 0)
	 {
		 if(!memcmp(buf, sync_reply, 4)) break;
	 } else fprintf(stderr, ".");
	} 


}

int pdma_init()
{
	
  if(serial_open(SERIAL_DEV, SERIAL_SPEED) < 0) return -1;
  
  serial_set_rts(0);
  serial_set_rts(1);
  
  usleep(10000);

	pdma_resync();
  fprintf(stderr,"Synchronization OK!\n");
}

int pdma_write(uint32_t addr, uint32_t data)
{
  const uint8_t ack[] = {0x55, 0xaa, 0xbf, 0x2f};
 uint8_t buf[4];
 uint32_t request = 0x80000000 | ((addr & 0x7fffff) << 8) | 1;

// fprintf(stderr,"write: %x %x rq %x\n", addr, data, request);
 
 for(;;)
 {
 	 serial_write_byte((request >> 24) & 0xff);
	 serial_write_byte((request >> 16) & 0xff);
	 serial_write_byte((request >> 8) & 0xff);
	 serial_write_byte((request >> 0) & 0xff);

	 serial_write_byte((data >> 24) & 0xff);
	 serial_write_byte((data >> 16) & 0xff);
	 serial_write_byte((data >> 8) & 0xff);
	 serial_write_byte((data >> 0) & 0xff);
		if(serial_read_timeout(buf, 4, 10000) < 0 || memcmp(buf, ack, 4))
			pdma_resync();
	  else
  	  break;
  }
}

uint32_t pdma_read(uint32_t addr)
{
 uint32_t request = ((addr & 0x7fffff) << 8) | 1;
 uint8_t buf[4];

// fprintf(stderr,"read: %x\n", addr);

for(;;)
{

 serial_write_byte((request >> 24) & 0xff);
 serial_write_byte((request >> 16) & 0xff);
 serial_write_byte((request >> 8) & 0xff);
 serial_write_byte((request >> 0) & 0xff);

 if(serial_read_timeout(buf, 4, 10000)!=4)
   pdma_resync();
 else
   break;
 }
 
 
 return ((uint32_t)buf[0] << 24) |
				((uint32_t)buf[1] << 16) |
				((uint32_t)buf[2] << 8) |
				((uint32_t)buf[3]);
}

int pdma_read_multi(uint32_t addr, uint32_t *data, int length)
{
 uint32_t request = ((addr & 0x7fffff) << 8) | length;
 uint8_t buf[4];
 int l;
 
// fprintf(stderr, "read_multi %x %d\n", addr, length);

 for(;;)
 {
   l= length;


   serial_write_byte((request >> 24) & 0xff);
   serial_write_byte((request >> 16) & 0xff);
   serial_write_byte((request >> 8) & 0xff);
   serial_write_byte((request >> 0) & 0xff);

	 while(length--)
	 {

		  if(serial_read_timeout(buf, 4, 10000) != 4)
		  {
        pdma_resync();
        break;
		  }
 *data++ = ((uint32_t)buf[0] << 24) |
				((uint32_t)buf[1] << 16) |
				((uint32_t)buf[2] << 8) |
				((uint32_t)buf[3]);

	  }
	  break;
	}
}
