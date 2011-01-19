/*      SAM7Sisp - alternatywny bootloader dla mikrokontrolerów AT91SAM7

        (c) Tomasz Wlostowski 2006

        This program is free software; you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation; either version 2 of the License, or
        (at your option) any later version.
*/


#include <stdio.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/ioctl.h>
#include <asm/ioctls.h>
#include <string.h>
#include <termios.h>
#include <fcntl.h>

#include <inttypes.h>

static int serial_fd;

void serial_set_dtr(int s) // pin 4
{
    unsigned int v;
    if (serial_fd<0) return;
    ioctl(serial_fd,TIOCMGET,&v);
    if (s) v|=TIOCM_DTR; else v&=~TIOCM_DTR;
    ioctl(serial_fd,TIOCMSET,&v);
}

void serial_set_rts(int s) // pin 4
{
    unsigned int v;
    if (serial_fd<0) return;
    ioctl(serial_fd,TIOCMGET,&v);
    if (s) v|=TIOCM_RTS; else v&=~TIOCM_RTS;
    ioctl(serial_fd,TIOCMSET,&v);
}

int serial_open(char *dev_name, int speed)
{
    struct termios t;
    int fd;
    int spd;

    switch(speed)
    {

	case 921600: spd=B921600; break;
	case 230400: spd=B230400; break;
	case 460800: spd=B460800; break;
	case 115200: spd=B115200; break;
	case 57600: spd=B57600; break;
	case 38400: spd=B38400; break;
	case 19200: spd=B19200; break;
	case 9600: spd=B9600; break;
	default: return -2;
    }
    
    fd = open (dev_name, O_RDWR | O_NONBLOCK);

    if(fd<0) return -1;


    tcgetattr (fd, &t);
    t.c_iflag = IGNBRK | IGNPAR;
    t.c_oflag = t.c_lflag = t.c_line = 0;
    t.c_cflag = CSTOPB | CS8 | CREAD |  CLOCAL | HUPCL | spd;
    tcsetattr (fd, TCSAFLUSH, &t);

    serial_fd = fd;
    return 0;
}

void serial_close()
{
    close(serial_fd);
}

int serial_write(char *data, int len)
{
    return write(serial_fd, data, len);
}


int serial_read(char *data, int len)
{
    int nbytes=0;
    while(len)
    {
			if(read(serial_fd, data, 1)==1) { len--;data++; nbytes++; }
    }

    return nbytes;
};


uint64_t get_tics()
{
 struct timezone tz = {0,0};
 struct timeval tv;
 
 gettimeofday(&tv, &tz);
 
 return (uint64_t)tv.tv_sec * 1000000ULL + (uint64_t) tv.tv_usec;
}

int serial_read_timeout(char *data, int len, int timeout)
{
    int nbytes=0;

		 uint64_t tstart = get_tics();

    while(len)
    {
 
			if(read(serial_fd, data, 1)==1) { len--;data++; nbytes++; tstart = get_tics(); }
    
   	if(get_tics() - tstart > (uint64_t) timeout) return -1;
    }
    
    

    return nbytes;
};



void serial_write_byte(unsigned char b)
{
    write (serial_fd,&b,1);
}

unsigned char serial_read_byte()
{
    unsigned char b;
    serial_read(&b,1);
//    fprintf(stderr,"%02x ", b);
    return b;

}

int serial_data_avail()
{
    fd_set set;
    struct timeval tv;
    
    FD_ZERO(&set);
    FD_SET(serial_fd,&set);
    
    tv.tv_sec = 0;
    tv.tv_usec = 0;
    
    return select(serial_fd+1, &set, NULL, NULL, &tv)>0;
}

unsigned int sys_get_clock_usec()
{
    struct timezone tz={0,0};
    struct timeval tv;

    gettimeofday(&tv,&tz);
    
    return tv.tv_usec + tv.tv_sec * 1000000;    
}

void sys_delay(int msecs)
{
    usleep(msecs*1000);
}

void serial_purge()
{
  while(serial_data_avail()) serial_read_byte();
}