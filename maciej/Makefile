CC=gcc

COMMON_OBJS=usb_rdma.o adc_stuff.o serial_linux.o
OBJS=adc_test.o $(COMMON_OBJS)
MODOBJS=adc_test_modified.o $(COMMON_OBJS)

CFLAGS_SDL=$(shell sdl-config --cflags) $(shell pkg-config --cflags fftw3)  -lSDL_ttf
LDFLAGS_SDL=$(shell sdl-config --libs) $(shell pkg-config --libs fftw3) -lSDL_ttf

CFLAGS = $(CFLAGS_SDL) -fPIC
LDFLAGS = $(LDFLAGS_SDL)

TARGETS = adc_test adc_test_modified libadc.so

all:	$(TARGETS)

libadc.so: $(OBJS)
		${CC} -shared -o $(OUTPUT_SO) $(OBJS)
adc_test: $(OBJS)
		${CC} -o $@ $(OBJS) $(LDFLAGS)
adc_test_modified: $(MODOBJS)
		${CC} -o $@ $(MODOBJS) $(LDFLAGS)
clean:
		rm -f $(OBJS) $(MODOBJS) $(TARGETS)

