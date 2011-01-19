CC=gcc
OBJS=usb_rdma.o adc_stuff.o serial_linux.o adc_test_modified.o
OUTPUT=adc_test
OUTPUT_SO=libadc.so
CFLAGS_SDL=$(shell sdl-config --cflags) $(shell pkg-config --cflags fftw3)  -lSDL_ttf
LDFLAGS_SDL=$(shell sdl-config --libs) $(shell pkg-config --libs fftw3) -lSDL_ttf

CFLAGS = $(CFLAGS_SDL) -fPIC
LDFLAGS = $(LDFLAGS_SDL)

all:	$(OBJS) adc_test.o
		${CC} -o $(OUTPUT) $(OBJS) $(LDFLAGS)
		${CC} -shared -o $(OUTPUT_SO) $(OBJS)

clean:
		rm -f $(OBJS) $(OUTPUT)
