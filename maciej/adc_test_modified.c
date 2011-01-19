#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

#include <complex.h>
#include <signal.h>

#include "adc_stuff.h"
#include "fpga_regs.h"
#include <SDL.h>
#include <SDL_ttf.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <fftw3.h>
 
#define SCREEN_LEGEND_X_MAX 1250
#define SCREEN_LEGEND_X_MIN 1024
#define SCREEN_MEAS_Y_MIN 512
#define SCREEN_MEAS_Y_MAX 600
#define SCREEN_PLOT_X_MAX 1023
#define SCREEN_PLOT_Y_MAX 511
#define SCREEN_BPP 4
#define SCREEN_DEPTH 32
#define PI 3.14159265359
#define NSAMPLES 2048

struct measurements
{
	//double samples_fft[NSAMPLES/2];
	double samples_time[NSAMPLES/2]; 	//samples to display in oscillocope mode, half of the all measured samples
	int cycles;							//number of signal periods in samples_time table
	int no;								//measurement number
	int no_sig_avg;						//number of measurements taken for averaging
	int rms_stop;						//number of samples taken to the RMS measurement (last zero-crossing)
	float rms;							//RMS value of the periodic signal
	float rms_sum;						//sum of RMSes - you've got to divide it by no_sig_avg to get the average RMS value
	float freq;							//frequency of the periodic signal
	float freq_sum;						//the same as in case of freq_sum
	float zero_level;					//DC value of the signal in the range of -1 ... +1
	float noise_mean;					//actually the same as above, but given in the range -8192...+8192
	float noise_power;					//noise power given in bits
	float enob;							//equivalent number of bits
	double samples_in[NSAMPLES];		//samples in the range of -1 ... +1
	double fft_out[NSAMPLES/2];
	float temperature;
	float snr;
} meas;

struct parameters
{
	enum ADC_range {R_100mV=0, R_1V, R_10V} 
		adc_range;						//adc sensitivity
	
	int adc_offset; 					//0.... 65535, 32767 means 0 V
	int adc_channel; 					//3, 4

	enum DISP_mode {DISP_OSC=0, DISP_FFT, DISP_RMS, DISP_EQUIV} 
		disp_mode;						//oscilloscope, FFT, RMS
	
	int adc_50ohm;						//termination
	int x_scale;						//needed for magnifying in time domain, normally 1, 2, 4, 8... if magnified
	int y_scale_time;					//needed for magnifying in voltage domain, normally 256, 512, 1024 etc, if magnified
	int do_sig_avg;						//0 / 1 - enabling or disabling the signal averaging
	int cls;							//for disabling screen clearing
	int w;								//for enabling signal windowing (only for FFT)
	
	int base_freq;						//sampling speed
	int N1;								//the factor that is necessary to be stored - related to the crystal generator
	int y_dB_scale;						//magnifying factor for the FFT and RMS measurements
	int l;								//if 1, then refreshing screen is disabled
	int do_temp_meas;	
	int show_lines ;
} params;



void itoa(int number, char *txt, int min_no_of_digits)
{
	int temp = 0;
	int temp2 = 1000000000;	
	int marker=0;
	
	if (number < 0)
	{
		number = -number;
		txt[temp++] = '-';
	}
 
	while(temp2)
	{
		if ((number / temp2) || (++min_no_of_digits > 10))
			marker=1;
		if(marker)
			txt[temp++]=number / temp2 + '0';
		number %= temp2;
		temp2/=10;
	}
	txt[temp]='\0';
}


void putpixel(SDL_Surface *screen, int x, int y, Uint8 r, Uint8 g, Uint8 b)
{
	Uint32 *pixmem32;
	Uint32 colour; 
	int y_calc;
	if ((x<0) || (x >= screen->w))
		return;
	if ((y<0) || (y >= screen->h))
		return;
	y_calc = y*screen->pitch/SCREEN_BPP;
	colour = SDL_MapRGB( screen->format, r, g, b );
	pixmem32 = (Uint32*) screen->pixels + y_calc + x;
	*pixmem32 = colour;
}

void line(SDL_Surface *screen, int x0, int y0, int x1, int y1, Uint8 r, Uint8 g, Uint8 b)
{
	int dx = x1 - x0;
	int dy = y1 - y0;

	putpixel(screen, x0, y0, r, g, b);

	if (abs(dx) > abs(dy)) 
	{          // slope < 1
		float m = (float) dy / (float) dx;      // compute slope
		float bb = y0 - m*x0;
		dx = (dx < 0) ? -1 : 1;
		while (x0 != x1) 
		{
			x0 += dx;
			putpixel(screen, x0, round(m*x0 + bb), r, g, b);
		}
	} 
	else if (dy != 0) 
	{                              // slope >= 1
		float m = (float) dx / (float) dy;      // compute slope
		float bb = x0 - m*y0;
		dy = (dy < 0) ? -1 : 1;
		while (y0 != y1) 
		{
		   y0 += dy;
		   putpixel(screen, round(m*y0 + bb), y0, r, g, b);
		}
	}
}


int sighandler(int sig)
{
	fprintf(stderr,"crash....\n");
	SDL_Quit();
	exit(-1);
}

int SDL_init(SDL_Surface **screen, TTF_Font **fonts)
{
	signal(SIGINT, (__sighandler_t)sighandler);

	if (SDL_Init(SDL_INIT_VIDEO) < 0 ) 
		return 1;
							   
	if (!(*screen = SDL_SetVideoMode(SCREEN_LEGEND_X_MAX, SCREEN_MEAS_Y_MAX, SCREEN_DEPTH, SDL_HWSURFACE)))
	{
		SDL_Quit();
		return 1;
	}

	if(TTF_Init()!=0) /* 0 success, -1 failed */
	{
		fprintf( stderr, "Unable to init SDL_ttf: %s\n",TTF_GetError());
		return 1;
	}

	*fonts=TTF_OpenFont("/usr/share/fonts/truetype/tahoma/Tahoma.TTF", 13 /*font size */);
	if(!(*fonts))
	{
		fprintf(stderr, "TTF_OpenFont: %s\n", TTF_GetError());
		return 1 ;
	}	
	return 0;
}


void SDL_txt(SDL_Surface* screen, TTF_Font *fonts, char *txt, int x, int y,  Uint8 r, Uint8 g, Uint8 b)
{
	SDL_Color clrFg = {r, g, b, 0};  // Blue ("Fg" is foreground)
	SDL_Surface *sText = TTF_RenderText_Solid(fonts, txt, clrFg );
	SDL_Rect rcDest = {x, y, 0 ,0};
	SDL_BlitSurface(sText, NULL, screen, &rcDest );
	SDL_FreeSurface(sText);
}


void init()
{
	params.adc_range  = R_100mV;
	params.adc_offset = 32768;
	params.adc_channel = 4;
	params.adc_50ohm = 1;
	params.disp_mode = DISP_OSC;
	params.x_scale = 1;
	params.do_sig_avg = 0;
	params.y_scale_time = 256;
	params.cls = 1;
	params.base_freq = 100000000;
	params.w = 1;

	params.y_dB_scale = 1;
	params.l = 0;
	params.show_lines =1;
	
	
	adc_init();
	i2c_init(BASE_I2C_CLKGEN);	
	i2c_init(BASE_I2C_IDMEM);
	
	adc_set_offset(4, params.adc_offset);
	adc_set_offset(3, params.adc_offset);
	adc_set_range(params.adc_channel, R_100mV, params.adc_50ohm);
	
	char temp_char[2];
	temp_char[0] = 0x80;
	i2c_write(BASE_I2C_CLKGEN, 0xAA, 135, temp_char, 1);
	usleep(10000);
	i2c_read(BASE_I2C_CLKGEN, 0xAA, 0x07, temp_char, 2);						
	params.N1 = ((temp_char[0] & 0x1F) << 2) | ((temp_char[1] >> 6) & 0x03);
	

	meas.no_sig_avg = 0;
	meas.no = 0;
	meas.rms_stop=0;
	meas.cycles = 0;
	meas.rms = 0;
	meas.rms_sum = 0;
	meas.freq = 0;
	meas.freq_sum = 0;
	meas.zero_level = 0;
	meas.noise_mean = 0;
	meas.noise_power = 0;
	meas.enob = 0;
	meas.temperature = 0;
}


void input_data_meas(int *buf)
{
	int i;
	int x;
	int time_offset = 0;
	float samples_temp[NSAMPLES];
	
	for (i=0;i<NSAMPLES;i++)
		meas.samples_in[i] = ((float)buf[i]-8192)/8192;
	
	for (x=0;x<(NSAMPLES/params.x_scale);x++)
	{
		for (i=0;i<params.x_scale;i++)
			samples_temp[x*params.x_scale+i] = meas.samples_in[x]+(meas.samples_in[x+1]-meas.samples_in[x])*i/params.x_scale;
	}
	
	i = 0;
	for(time_offset=0;time_offset< (NSAMPLES/2);time_offset++)
	{
		if (samples_temp[time_offset] < 0)
			i = 1;

		if ((i == 1) && (samples_temp[time_offset] >= 0))
			break;
	}

	if(time_offset >= (NSAMPLES/2))
		time_offset=NSAMPLES/2-1;		


	for (x=0;x<(NSAMPLES/2);x++)
	{
		if (params.do_sig_avg == 0)
		{
			meas.samples_time[x] = 0;
			meas.no_sig_avg=0;
		}
		
		meas.samples_time[x] = ((meas.samples_time[x] * meas.no_sig_avg) + samples_temp[time_offset + x])/(meas.no_sig_avg + 1);		
	}
	meas.no++;
	meas.no_sig_avg++;

	i = 0;
	meas.cycles = 0;
	meas.rms_stop=-1;
	for (x=(NSAMPLES/2-1); x>=0; x--)
	{
		if (meas.samples_time[x] >= 0)
			i = 1;

		if ((i == 1) && (meas.samples_time[x] < 0))
		{
			meas.cycles++;
			if (meas.cycles==1)
				meas.rms_stop = x;
			i=0;

		}
	}
	
	meas.zero_level = 0;
	
	for (i=0;i<= meas.rms_stop;i++)
		meas.zero_level = meas.zero_level + meas.samples_time[i];

	meas.zero_level = meas.zero_level /(float)(meas.rms_stop);

	float sum=0;
	float temp;
	for (i=0;i<= meas.rms_stop;i++)
	{
		temp = meas.samples_time[i] - meas.zero_level;
		sum = sum + (temp*temp);
	}
	sum /= (meas.rms_stop+1);
	meas.rms = sqrt(sum);
	
	meas.rms_sum += meas.rms;
	meas.freq = (float)(meas.cycles) * params.base_freq / (float)(meas.rms_stop+1);
	meas.freq *= (float)(params.x_scale);	
	meas.freq_sum = meas.freq_sum + meas.freq;  

	meas.noise_mean=0;
	for (i=0;i<2048;i++)
	{
		meas.noise_mean += meas.samples_in[i]*8192/2048;
	}
	
	meas.noise_power=0;
	for(i=0;i<NSAMPLES;i++)
	{
		meas.noise_power += (meas.samples_in[i]*8192-meas.noise_mean) * (meas.samples_in[i]*8192-meas.noise_mean);
	}
	
	meas.noise_power/=NSAMPLES;
	meas.noise_power=sqrt(meas.noise_power);
	meas.enob = (1.76-(20*log10((16384/2/1.42)/meas.noise_power)))/6.02;
	meas.snr = meas.enob * 6.02 - 1.76;
	fprintf(stderr, "No:%d, RMS:%f, freq:%f, zero:%f, cycl:%d, rms_stop:%d, noise power:%f, ENOB: %f , SNR: %f\n", meas.no, meas.rms, meas.freq, meas.zero_level, meas.cycles, meas.rms_stop, meas.noise_power, meas.enob, meas.snr);
	
	
	//temperature
	if (params.do_temp_meas)
	{
		uint8_t temp_char[2];
		temp_char[0] = 0x60;
		i2c_write(BASE_I2C_CLKGEN, 0x90, 0x01, temp_char, 1);						
		i2c_read(BASE_I2C_CLKGEN, 0x90, 0x00, temp_char, 2);
		meas.temperature = (float)temp_char[0] + (float)temp_char[1]/256;
	}

	//FFT
	int y, y_2;
	double out[NSAMPLES][2];
	for (i=0;i<NSAMPLES;i++)
	{	
		if (params.w) 
			meas.samples_in[i] = meas.samples_in[i]  * (1 - cos(PI * 2.0 * (double)i/(NSAMPLES-1) ));
	}

	fftw_plan p;			
	p = fftw_plan_dft_r2c_1d(NSAMPLES, meas.samples_in, (__complex__*)out, FFTW_ESTIMATE);
	fftw_execute(p);
	
	for (i=0;i<(NSAMPLES/2);i++)
	{	
		if (!params.do_sig_avg)
			meas.fft_out[i] = 0;

		y = -64 * params.y_dB_scale * log10(sqrt(out[i][0]*out[i][0] + out[i][1]*out[i][1])/NSAMPLES*2);
		
		meas.fft_out[i] = ((meas.fft_out[i] * (meas.no_sig_avg-1/*increased previously*/)) + y)/(meas.no_sig_avg);
	}
	
	fftw_destroy_plan(p);
	fftw_cleanup();	
}


void draw_screen(SDL_Surface* screen)
{
	if (params.cls)
	{
		int x;
		int y;
		
		for(y = 0; y <= SCREEN_PLOT_Y_MAX; y++ ) 
		{
			for(x=0;x <= SCREEN_PLOT_X_MAX;x++)
				putpixel(screen,x,y,0x00, 0x00, 0x00);		    	
		}
	}	
	
	line(screen, SCREEN_PLOT_X_MAX+1, 0, SCREEN_PLOT_X_MAX+1, SCREEN_PLOT_Y_MAX+1, 0xFF, 0xFF, 0xFF);
	line(screen, 0, SCREEN_PLOT_Y_MAX+1, SCREEN_PLOT_X_MAX+1, SCREEN_PLOT_Y_MAX+1, 0xFF, 0xFF, 0xFF);
	
	if (params.disp_mode == DISP_OSC)
	{
		int x;
		int y, y_2;
		int i;
				
		for(x=0;x<SCREEN_PLOT_X_MAX;x++)
		{
			y = (meas.samples_time[x]*params.y_scale_time)+( (SCREEN_PLOT_Y_MAX+1) /2);
			y_2 = (meas.samples_time[x+1]*params.y_scale_time)+( (SCREEN_PLOT_Y_MAX+1) /2);
			line(screen, x, y, x+1, y_2, 0xFF, 0xFF, 0x00);
		}
	}
	
	
	if (params.disp_mode == DISP_FFT)
	{
		int i, y, y_2;
		for (i=0;i<NSAMPLES/2-1;i++)
		{                                     
			y = meas.fft_out[i];
			y_2 = meas.fft_out[i+1];
			line(screen, i, y, i+1, y_2, 0xFF, 0xFF, 0x00);					
		}
	}
	
	
	
	if (params.disp_mode == DISP_RMS)
	{
		if((meas.freq > 0) && (meas.freq < 1000000000))
		{
			static int x_o=0, y_o=0, xx=0, yy=0 ;
			x_o = xx;		
			xx = meas.freq*SCREEN_PLOT_X_MAX/(params.base_freq/2);								
			
			y_o = yy;
			yy = -64 * params.y_dB_scale * log10(meas.rms);
			//reverse sinc correction
			yy = yy*PI*meas.freq/params.base_freq/sin(PI*meas.freq/params.base_freq);
			//drawing line
			line(screen, xx, yy, x_o, y_o, 0xFF, 0xFF, 0x00);	
		}
	}
}


void draw_axis(SDL_Surface* screen, TTF_Font *fonts)
{
	int y, x, i;
	
	if  ((params.disp_mode == DISP_OSC) || (params.disp_mode == DISP_EQUIV))
	{
		for (y=64;y<(SCREEN_PLOT_Y_MAX+1);y+=64)
		{
			for(i=0;i<(SCREEN_PLOT_X_MAX+1);i+=2)
				putpixel(screen, i,y,0x50,0x50,0x50);
		}

		for (x=64;x<(SCREEN_PLOT_X_MAX+1);x+=64)
		{
		for(i=0;i<(SCREEN_PLOT_Y_MAX+1);i+=2)
				putpixel(screen, x,i,0x50,0x50,0x50);
		}

		if (params.show_lines)
		{
			if (params.disp_mode == DISP_OSC)
				line(screen, meas.rms_stop,0, meas.rms_stop, SCREEN_PLOT_Y_MAX+1,0xE0,0,0);

			y = (int)(meas.zero_level*params.y_scale_time)+(SCREEN_PLOT_Y_MAX+1)/2;
			line(screen, 0, y, SCREEN_PLOT_X_MAX+1,y,0,0,0xFF);
	
			y = (int)((meas.rms+meas.zero_level)*params.y_scale_time)+(SCREEN_PLOT_Y_MAX+1)/2;
			x = (int)((meas.zero_level-meas.rms)*params.y_scale_time)+(SCREEN_PLOT_Y_MAX+1)/2;
			for (i=0;i<(SCREEN_PLOT_X_MAX+1);i++)
			{
				putpixel(screen,i,y,0xE0,0,0);
				putpixel(screen,i,x,0xE0,0,0);
			}
		}
		
		float temp ;
		char txt[100], txt2[100];
		for (i=0; i<=SCREEN_PLOT_X_MAX; i+=(SCREEN_PLOT_X_MAX+1)/4)
		{
			temp = 1 / (float)params.base_freq / (float)params.x_scale * (float)i * 1000000;
			sprintf(txt, "%.2f us", temp);
			SDL_txt(screen, fonts, txt, i+2, SCREEN_PLOT_Y_MAX - 20, 0xFF, 0xFF, 0xFF);
			line(screen, i, 0, i, SCREEN_PLOT_Y_MAX, 0x80, 0x80, 0x80);
		}
		
		return;
	}



	int dB = 0;
	char txt[100];		
	char txt2[20];


	for (y=32;y<(SCREEN_PLOT_Y_MAX+1);y+=32)
	{
		for(i=0;i<(SCREEN_PLOT_X_MAX+1);i+=2)
			putpixel(screen, i,y,0x50,0x50,0x50);
	}
			
	for (y=32 ;y<(SCREEN_PLOT_Y_MAX+1);y+= 32)
	{
		if (!(y%(params.y_dB_scale*32)))
		{
			for(i=0;i<(SCREEN_PLOT_X_MAX+1);i++)
				putpixel(screen, i,y,0xA0,0xA0,0xA0);
		}
		
		dB -= 1000/params.y_dB_scale;
		itoa(dB/100, txt, -1);
		if(params.y_dB_scale>2)
		{
			itoa(-1*(dB-(dB/100*100)), txt2, 2);
			strcat(txt, ".");
			strcat(txt, txt2);
		}							
		strcat(txt, " dB");	
		//fprintf(stderr, txt);				
		SDL_Color clrFg = {255,255,255,0};  // Blue ("Fg" is foreground)
		SDL_Surface *sText = TTF_RenderText_Solid(fonts, txt, clrFg );
		SDL_Rect rcDest = {SCREEN_PLOT_X_MAX-60,y-15,0,0};
		SDL_BlitSurface(sText, NULL, screen, &rcDest );
		SDL_FreeSurface(sText);
	}

	for (x=205;x<(SCREEN_PLOT_X_MAX+1);x+=205)
	{
		for(i=0;i<512;i+=2)
			putpixel(screen, x,i,0x50,0x50,0x50);
	}          


	int temp=1;		
	for (x=205;x<(SCREEN_PLOT_X_MAX+1);x+=205)
	{
						
		itoa(params.base_freq*(temp)/10/1000000, txt, -1);
		strcat(txt,".");
		itoa(((params.base_freq*temp/10/1000)%1000), txt2, 3);
		strcat(txt,txt2);							
		strcat(txt, " MHz");
		temp++;	
		//fprintf(stderr, txt);				
		SDL_Color clrFg = {255,255,255,0};  // Blue ("Fg" is foreground)
		SDL_Surface *sText = TTF_RenderText_Solid(fonts, txt, clrFg );
		SDL_Rect rcDest = {x,490,0,0};
		SDL_BlitSurface(sText, NULL, screen, &rcDest );
		SDL_FreeSurface(sText);				
	}
}



void draw_legend(SDL_Surface* screen, TTF_Font *fonts)
{
	int x;
	int y;
	int i;
	int position = 0;
	char txt[100];
	char txt2[100];
	
	for(y = 0; y <= SCREEN_PLOT_Y_MAX; y++ ) 
	{
		for(x=SCREEN_LEGEND_X_MIN+1; x <= SCREEN_LEGEND_X_MAX;x++)
		putpixel(screen,x,y,0x00, 0x00, 0x00);		    	
	}
	
	
	strcpy(txt, "r       - ADC range:  ");
	if (params.adc_range == 0)
		strcat(txt, " 100 mV");
	if (params.adc_range == 1)
		strcat(txt, " 1 V");
	if (params.adc_range == 2)
		strcat(txt, " 10 V");
	SDL_txt(screen, fonts, txt, SCREEN_LEGEND_X_MIN + 5, position, 0xFF, 0xFF, 0xFF);
	
	strcpy(txt, "c       - ADC channel:  ");
	itoa(params.adc_channel, txt2, 1);
	strcat(txt, txt2);
	SDL_txt(screen, fonts, txt, SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);

	strcpy(txt, "s       - oscilloscope Y multiplier:  ");
	itoa(params.y_scale_time/256, txt2, 1);
	strcat(txt, txt2);
	SDL_txt(screen, fonts, txt, SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	float temp=0.1;
	if (params.adc_range == 1)
		temp = 1;
	if (params.adc_range == 2)
		temp = 10;
	temp = temp * 256 / params.y_scale_time;
		
	if (temp >= 0.1)
		sprintf(txt, "          full scale Y range:  %.3f V", temp);
	else
		sprintf(txt, "          full scale Y range:  %.3f mV", temp*1000);
	SDL_txt(screen, fonts, txt, SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	
	sprintf(txt, "up / down      - offset, +/- 1 bit", params.adc_offset);
	SDL_txt(screen, fonts, txt, SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	sprintf(txt, "left / right      - offset, +/- 100 bits   ", params.adc_offset);
	SDL_txt(screen, fonts, txt, SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	sprintf(txt, "          value: %d bits  %.4f V", params.adc_offset, ((float)params.adc_offset-32767)/32768*5);
	SDL_txt(screen, fonts, txt, SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	
	
	SDL_txt(screen, fonts, "a      - clear average ", SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);

	sprintf(txt, "x       - oscilloscope X multiplier:  %d", params.x_scale);
	SDL_txt(screen, fonts, txt, SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);	
	
	strcpy(txt, "f       - clearing screen:  ");
	if (params.cls == 0)
		strcat(txt, "no");
	else
		strcat(txt, "yes");
	SDL_txt(screen, fonts, txt, SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	
	strcpy(txt, "d       - signal averaging: ");
	if (params.do_sig_avg == 0)
		strcat(txt, "no");
	else
		strcat(txt, "yes");
	SDL_txt(screen, fonts, txt, SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	
	strcpy(txt, "l       - oscilloscope: show lines - ");
	if (params.show_lines == 0)
		strcat(txt, "no");
	else
		strcat(txt, "yes");
	SDL_txt(screen, fonts, txt, SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);

	

	SDL_txt(screen, fonts, "a       - clear avg. measurements ", SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	
	strcpy(txt, "e       - mode:  ");
	if (params.disp_mode == 0)
		strcat(txt, "oscilloscope");
	if (params.disp_mode == 1)
		strcat(txt, "FFT");
	if (params.disp_mode == 2)
		strcat(txt, "RMS @ frequency");
	if (params.disp_mode == 3)
		strcat(txt, "equivalent time base");
	
	SDL_txt(screen, fonts, txt, SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	
	strcpy(txt, "t       - input temination:  ");
	if (params.adc_50ohm == 0)
		strcat(txt, "off");
	else
		strcat(txt, "50 Ohm");
	SDL_txt(screen, fonts, txt, SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	
	strcpy(txt, "w       - FFT window:  ");
	if (params.w == 0)
		strcat(txt, "rectangular");
	else
		strcat(txt, "Hann");
	SDL_txt(screen, fonts, txt, SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	
	strcpy(txt, "m       - temperature meas.:  ");
	if (params.do_temp_meas == 0)
		strcat(txt, "no");
	else
		strcat(txt, "yes");
	SDL_txt(screen, fonts, txt, SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	
	sprintf(txt, "         readout:  %.3f C deg.", meas.temperature);
	SDL_txt(screen, fonts, txt, SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);

	sprintf(txt, "< >    - sampling freq:  %.1f MHz", (float)params.base_freq/1000000);
	SDL_txt(screen, fonts, txt, SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	
	strcpy(txt, "space  - displaying:  ");
	if (params.l == 0)
		strcat(txt, "normal");
	else
		strcat(txt, "stopped");
	SDL_txt(screen, fonts, txt, SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	
	SDL_txt(screen, fonts, "[       - I2C memory write ", SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	
	SDL_txt(screen, fonts, "]       - I2C memory write ", SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	
	SDL_txt(screen, fonts, "y       - FFT & RMS: dB scale change ", SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	
	
	SDL_txt(screen, fonts, "For sensible noise power and ENOB" , SCREEN_LEGEND_X_MIN + 5, position+=40, 0xFF, 0xFF, 0xFF);
	SDL_txt(screen, fonts, "measurements, input should be", SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	SDL_txt(screen, fonts, "disconnected or wired to the ground.", SCREEN_LEGEND_X_MIN + 5, position+=20, 0xFF, 0xFF, 0xFF);
	
	

}


void draw_meas(SDL_Surface* screen, TTF_Font *fonts)
{
	int x;
	int y;
	int i;
	
	for(y = SCREEN_MEAS_Y_MIN+1; y <= SCREEN_MEAS_Y_MAX; y++ ) 
	{
		for(x=0; x <= SCREEN_PLOT_X_MAX;x++)
		putpixel(screen,x,y,0x00, 0x00, 0x00);		    	
	}
}


int key_check(int key)
{
	if (key == 27) //range - r
	{
		params.adc_range++;
		params.adc_range %= 3;
		if (params.adc_range == 0)
			adc_set_range(params.adc_channel, ADC_RANGE_100mV, params.adc_50ohm);
		if (params.adc_range == 1)
			adc_set_range(params.adc_channel, ADC_RANGE_1V, params.adc_50ohm);
		if (params.adc_range == 2)
			adc_set_range(params.adc_channel, ADC_RANGE_10V, params.adc_50ohm);
		
		return 0;
	}
	
	
	if (key == 39) //y-scale - s
	{
		params.y_scale_time *= 2;
		if (params.y_scale_time > 40000)
			params.y_scale_time = 256;
		
		return 0;
	}
	
	
	if (key == 111) //offset - up
	{
		params.adc_offset++;					
		adc_set_offset(params.adc_channel, params.adc_offset);
		
		return 0;
	}
	
	
	if (key == 116) //offset - down
	{
		params.adc_offset--;					
		adc_set_offset(params.adc_channel, params.adc_offset);
		
		return 0;
	}
	
	if (key == 113) //offset - left -100 bits
	{
		params.adc_offset-=100;					
		adc_set_offset(params.adc_channel, params.adc_offset);
		
		return 0;
	}
	
	
	if (key == 114) //offset - right +100 bits
	{
		params.adc_offset+=100;					
		adc_set_offset(params.adc_channel, params.adc_offset);
		
		return 0;
	}
	
	if (key == 54) //channel - c
	{
		params.adc_channel++;
		if (params.adc_channel == 5)
			params.adc_channel = 3;					
		
		return 0;
	}
	
	
	if (key == 38) //clear avg measurements - a
	{
		meas.freq_sum = 0; 
		meas.rms_sum = 0;
		meas.no = 0;	
		meas.noise_power=0;
		meas.noise_mean=0;
		
		return 0;
	}
	
	
	if (key == 53) //x-scale - x
	{
		params.x_scale*=2;
		if (params.x_scale == 128)
			params.x_scale = 1;

		return 0;
	}
	
	
	if (key == 41) //clearing screen - f
	{
		if (params.cls)
			params.cls=0;
		else
			params.cls=1;

		return 0;
	}
	
	if (key == 40) //averaging - d
	{
		if (params.do_sig_avg)
			params.do_sig_avg=0;
		else
			params.do_sig_avg=1;

		return 0;
	}				
	
	
	if (key == 26) // oscilloscope / FFT / RMS - e
	{
		params.disp_mode++;
		params.disp_mode%=3;

		return 0;
	}
	
	
	if (key == 28) //termination - t
	{
		if (params.adc_50ohm)
			params.adc_50ohm=0;
		else
			params.adc_50ohm=1;						
		if (params.adc_range == 0)
			adc_set_range(params.adc_channel, ADC_RANGE_100mV, params.adc_50ohm);
		if (params.adc_range == 1)
			adc_set_range(params.adc_channel, ADC_RANGE_1V, params.adc_50ohm);
		if (params.adc_range == 2)
			adc_set_range(params.adc_channel, ADC_RANGE_10V, params.adc_50ohm);

		return 0;
	}
	
	
	if (key == 25) //window (rectangular / HANN) - w
	{
		params.w = (++(params.w)) % 2;
		
		return 0;
	}					
	
	if (key == 58) // temp measurement - m
	{
		params.do_temp_meas++;
		params.do_temp_meas %=2;
		return 0; 
	}
		
	if ((key == 59) || (key == 60)) // freq mod: < >
	{
		uint8_t temp_char[2];
		int N1_temp;						

		
		if (key == 60)
		{	
			params.base_freq *= 2;
			if (params.base_freq > 100000000)
				params.base_freq = 12500000;
		}
		
		if (key == 59)
		{	
			params.base_freq /= 2;
			if (params.base_freq < 12500000)
				params.base_freq = 100000000;
		}

		N1_temp = (params.N1+1) * 100000000/params.base_freq;
		N1_temp--;
		i2c_read(BASE_I2C_CLKGEN, 0xAA, 0x07, temp_char, 2);
		temp_char[0] &= 0xE0;
		temp_char[0] |= N1_temp >> 2;
		temp_char[1] &= 0x3F;
		temp_char[1] |= (N1_temp & 0x03) << 6;
		
		i2c_write(BASE_I2C_CLKGEN, 0xAA, 0x07, temp_char, 2);						
		fprintf(stderr, "\nfrequency: %d Hz, %d\n\n", params.base_freq, N1_temp);
		return 0;
	}
	
	if (key == 65) // pause - space
	{
		params.l++;
		params.l%=2;
		return 0;
	}
	
	if (key == 34) // write mem - [
	{
		int i;
		uint8_t temp_char[1];	
		for (i=0;i<256;i++)
		{
			temp_char[0] = 255-i;
			i2c_mem_write(0xA4, i, temp_char, 1);
			usleep(1000);
		}
		fprintf(stderr, "\n256 bytes written.\n");
		return 0;
	}
	
	
	if (key == 35) // read mem - ]
	{
		int i;
		uint8_t temp_char[1] = {'D'};	
		for (i=0;i<256;i++)
		{
			i2c_mem_read(0xA4, i, temp_char, 1);
			fprintf(stderr, "data: %d\n", temp_char[0]);
		}
		return 0;	
	}
	
	
	if (key == 29) // dB scale change - y
	{
		params.y_dB_scale *=2;
		if (params.y_dB_scale > 16)
			params.y_dB_scale = 1;		
		return 0;
	}


	if (key == 46) // oscilloscope - show lines
	{
		params.show_lines++;
		params.show_lines %=2;
		return 0;
	}
	
	return 1;
}


main()
{
	SDL_Surface *screen;
	SDL_Event event;     
	TTF_Font *fonts;
	int buf[NSAMPLES];
	int keypress = 0;

	init();
	if (SDL_init(&screen, &fonts))
		return 1;


	while (!keypress) 
	{
		adc_record_single(params.adc_channel, buf, NSAMPLES, 0/*int pre_trigger*/);

		if(SDL_MUSTLOCK(screen)) 
		{
			if(SDL_LockSurface(screen) < 0) 
				return;
		}
		
		input_data_meas(buf);
		draw_screen(screen);
		draw_axis(screen, fonts);
		draw_legend(screen, fonts);
		draw_meas(screen, fonts);


		if(SDL_MUSTLOCK(screen)) 
			SDL_UnlockSurface(screen);
		SDL_Flip(screen); 		
		
		while(SDL_PollEvent(&event)) 
		{      
			switch (event.type) 
			{
			case SDL_QUIT:
				keypress = 1;
				break;
			case SDL_KEYDOWN:
				if (key_check(event.key.keysym.scancode))  //if 0, key has changed settings, otherwise exit
				{
					keypress = 1;
					fprintf(stderr, "\n%d\n", event.key.keysym.scancode);
				}
				break;
			}
		}
	}

	SDL_Quit();
	TTF_CloseFont(fonts);    
	return 0;
}
