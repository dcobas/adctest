/*      SAM7Sisp - alternatywny bootloader dla mikrokontrolerów AT91SAM7

        (c) Tomasz Wlostowski 2006

        This program is free software; you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation; either version 2 of the License, or
        (at your option) any later version.
*/


#ifndef __SERIAL_H
#define __SERIAL_H

int serial_open(char *dev_name, int speed);
void serial_close();
void serial_set_dtr(int s);
void serial_set_rts(int s);
int serial_read(char *data, int len);
int serial_write(char *data, int len);
void serial_write_byte(unsigned char b);
unsigned char serial_read_byte();
int serial_data_avail();
int serial_read_timeout(char *data, int len, int timeout);

void sys_delay(int msecs);
unsigned int sys_get_clock_usec();

#endif
