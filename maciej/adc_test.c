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
 
#define WIDTH 1024
#define HEIGHT 512
#define BPP 4
#define DEPTH 32



double freq_avg = 0;
double rms_avg = 0;
int no=0; 
int w = 0;
double pp_avg = 0;
int cls = 1;
int sig_avg = 0;
int no_sig_avg = 0;
int l = 1;
const PI = 3.14159265359;	
long int base_freq = 100000000;
TTF_Font *fonts;
int y_dB_scale = 1;


double noise_mean=0, noise_power=0;


int e=0;

	double samples[2048] = {
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
};

void my_itoa(int number, char *txt, int digits)
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
		if ((number / temp2) || (++digits > 10))
			marker=1;
		if(marker)
			txt[temp++]=number / temp2 + '0';
		number %= temp2;
		temp2/=10;
	}
	txt[temp]='\0';
}

void my_putpixel(SDL_Surface *screen, int x, int y, Uint8 r, Uint8 g, Uint8 b)
{
    Uint32 *pixmem32;
    Uint32 colour; 
	int y_calc;
	if ((x<0) || (x >= screen->w))
		return;
	if ((y<0) || (y >= screen->h))
		return;
	y_calc = y*screen->pitch/BPP;
    colour = SDL_MapRGB( screen->format, r, g, b );
    pixmem32 = (Uint32*) screen->pixels + y_calc + x;
    *pixmem32 = colour;
}

void my_line(SDL_Surface *screen, int x0, int y0, int x1, int y1, Uint8 r, Uint8 g, Uint8 b)
{
    int dx = x1 - x0;
    int dy = y1 - y0;

    my_putpixel(screen, x0, y0, r, g, b);

    if (abs(dx) > abs(dy)) 
	{          // slope < 1
    	float m = (float) dy / (float) dx;      // compute slope
        float bb = y0 - m*x0;
        dx = (dx < 0) ? -1 : 1;
        while (x0 != x1) 
		{
            x0 += dx;
		    my_putpixel(screen, x0, round(m*x0 + bb), r, g, b);
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
	       my_putpixel(screen, round(m*y0 + bb), y0, r, g, b);
        }
    }
}


void DrawScreen(SDL_Surface* screen, double samples_in[], float scale, int x_scale)
{ 
    int x, x_2, y, y_2, y_calc, i, time_offset, rms_stop; 
	double min = 2, max = -2;
	double rms, freq;
	double zero_level;
	int cycles;	
	double samples_temp[2048];

    if(SDL_MUSTLOCK(screen)) 
    {
		if(SDL_LockSurface(screen) < 0) 
			return;
    }                              

	for (x=0;x<(2048/x_scale);x++)
	{
		for (i=0;i<x_scale;i++)
			samples_temp[x*x_scale+i] = samples_in[x]+(samples_in[x+1]-samples_in[x])*i/x_scale;
	}

	i = 0;
	for(time_offset=0;time_offset<1024;time_offset++)
	{
		if (samples_temp[time_offset] < 0)
			i = 1;

		if ((i == 1) && (samples_temp[time_offset] >= 0))
			break;
	}

	if(time_offset >= 1024)
		time_offset=1023;		


	for (x=0;x<1024;x++)
	{
		if (sig_avg == 0)
		{
			samples[x] = 0;
			no_sig_avg=0;
		}
		
		samples[x] = ((samples[x] * no_sig_avg) + 				
			samples_temp[time_offset + x])/
			(no_sig_avg + 1);		
	}
	no_sig_avg++;

	no++;

	i = 0;
	cycles = 0;
	rms_stop=-1;
	for (x=1023; x>=0; x--)
	{
		if (samples[x] >= 0)
			i = 1;

		if ((i == 1) && (samples[x] < 0))
		{
			cycles++;
			if (cycles==1)
				rms_stop = x;
			i=0;

		}
	}



	zero_level = 0;
	for (i=0;i<=rms_stop;i++)
	{
		zero_level = zero_level + samples[i];
	}
	zero_level = zero_level /(float)(rms_stop);

	float sum=0;
	float temp;
	for (i=0;i<=rms_stop;i++)
	{
		temp = samples[i] - zero_level;
		sum = sum + (temp*temp);
	}
	sum /= (rms_stop+1);
	rms = sqrt(sum);
	
//printing on the screen
	rms_avg += rms;
	pp_avg += max-min;
	freq = (float)cycles * 100000000 / (float)(rms_stop+1);
	freq *= (float)x_scale;	
	freq_avg = freq_avg + freq;  
	//fprintf(stderr, "No:%d, avg pp:%f, RMS:%f, RMS avg:%f, freq:%f, freq avg:%f, zero:%f, cycl:%d, rms_stop:%d\n", no, pp_avg/no, rms, rms_avg/(float)no, freq, freq_avg/(float)no, zero_level, cycles, rms_stop);	
	
	noise_mean=0;
	for (i=0;i<2048;i++)
	{
		noise_mean+=samples_in[i]*8192/2048;
	}
	
	noise_power=0;
	for(i=0;i<2048;i++)
	{
		noise_power += (samples_in[i]*8192-noise_mean) * (samples_in[i]*8192-noise_mean);
	}
	
	noise_power/=2048;
	noise_power=sqrt(noise_power);
	float enob;
	
	enob = (1.76-(20*log10((16384/2/1.42)/noise_power)))/6.02;
	fprintf(stderr, "No:%d, RMS:%f, freq:%f, zero:%f, cycl:%d, rms_stop:%d, noise power:%f, ENOB: %f \n", no, rms, freq, zero_level, cycles, rms_stop, noise_power, enob);


//plotting
	//if (l)
	{
		if (e==0)
		{
			if (cls)
			{
				for(y = 0; y < screen->h; y++ ) 
				{
			   		for(x=0;x<screen->w;x++)
						my_putpixel(screen,x,y,0x00, 0x00, 0x00);		    	
				}
			}


			for (y=64;y<512;y+=64)
			{
				for(i=0;i<1024;i+=2)
					my_putpixel(screen, i,y,0x50,0x50,0x50);
			}

			for (x=64;x<1024;x+=64)
			{
				for(i=0;i<512;i+=2)
					my_putpixel(screen, x,i,0x50,0x50,0x50);
			}



			for(x=0;x<screen->w-1;x++)
			{
				if (min > samples[x])
					min = samples[x];
				if (max < samples[x])
					max = samples[x];	

				y = (samples[x]*scale)+(screen->h/2);
			 	y_2 = (samples[x+1]*scale)+(screen->h/2);
				my_line(screen, x, y, x+1, y_2, 0xFF, 0xFF, 0x00);
			}
		
			for(i=0;i<512;i++)
				my_putpixel(screen, rms_stop,i,0xFF,0,0);

			y = (int)(zero_level*scale)+screen->h/2;
			for(i=0;i<1024;i++)
			{
				my_putpixel(screen, i,y,0,0,0xFF);
			}
		
			y = (int)((rms+zero_level)*scale)+screen->h/2;
			x = (int)((zero_level-rms)*scale)+screen->h/2;
			for (i=0;i<1024;i++)
			{
				my_putpixel(screen,i,y,0xFF,0,0);
				my_putpixel(screen,i,x,0xFF,0,0);
			}
		}	
	
		if (e > 0)
		{
			if (cls)
			{
				for(y = 0; y < screen->h; y++ ) 
				{
			   		for(x=0;x<screen->w;x++)
						my_putpixel(screen,x,y,0x00, 0x00, 0x00);		    	
				}
			}
		

			int N=2048;
			double out[N][2];

			if ((e==1) && (freq>1) && (freq < 50000000) && (l))
			{
				static int x_o=0, y_o=0, xx=0, yy=0 ;
				x_o = xx;		
				xx = freq*1024/50000000;								
				
				y_o = yy;
				yy = -64 * y_dB_scale * log10(rms);
				yy = yy*PI*freq/100000000/sin(PI*freq/100000000);
				//drawing line
				my_line(screen, xx, yy, x_o, y_o, 0xFF, 0xFF, 0x00);	
			}
		                    

			if (e==2)
			{	

				for (i=0;i<N;i++)
				{	
					if (w) 
						samples_in[i] = samples_in[i]  * (1 - cos(PI * 2.0 * (double)i/(N-1) ));
				}

				fftw_plan p;			
				p = fftw_plan_dft_r2c_1d(N, samples_in, (fftw_complex *)out, FFTW_ESTIMATE);
				fftw_execute(p);
				for (i=0;i<1024;i++)
				{                                     
					y = -64 * y_dB_scale * log10(sqrt(out[i][0]*out[i][0] + out[i][1]*out[i][1])/N*2);
					int j=i+1;
					y_2 = -64 * y_dB_scale * log10(sqrt(out[j][0]*out[j][0]+ out[j][1]*out[j][1])/N*2);
									                
					my_line(screen, i, y, j, y_2, 0xFF, 0xFF, 0x00);					
				}
		
				fftw_destroy_plan(p);

				fftw_cleanup();
			}




			for (y=32;y<512;y+=32)
			{
				for(i=0;i<1024;i+=2)
					my_putpixel(screen, i,y,0x50,0x50,0x50);
			}

			int dB = 0;
			char txt[100];		
			char txt2[20];		
			for (y=32 ;y<512;y+= 32)
			{
				if (!(y%(y_dB_scale*32)))
				{
					for(i=0;i<1024;i++)
						my_putpixel(screen, i,y,0xA0,0xA0,0xA0);
				}
				
				dB -= 1000/y_dB_scale;
				my_itoa(dB/100, txt, -1);
				if(y_dB_scale>2)
				{
					my_itoa(-1*(dB-(dB/100*100)), txt2, 2);
					strcat(txt, ".");
					strcat(txt, txt2);
				}							
				strcat(txt, " dB");	
				//fprintf(stderr, txt);				
				SDL_Color clrFg = {255,255,255,0};  // Blue ("Fg" is foreground)
				SDL_Surface *sText = TTF_RenderText_Solid(fonts, txt, clrFg );
   				SDL_Rect rcDest = {950,y-15,0,0};
   				SDL_BlitSurface(sText, NULL, screen, &rcDest );
				SDL_FreeSurface(sText);
			}

			for (x=205;x<1024;x+=205)
			{
				for(i=0;i<512;i+=2)
					my_putpixel(screen, x,i,0x50,0x50,0x50);
			}          


			int temp=1;		
			for (x=205;x<1024;x+=205)
			{
								
				my_itoa(base_freq*(temp)/10/1000000, txt, -1);
				strcat(txt,".");
				my_itoa(((base_freq*temp/10/1000)%1000), txt2, 3);
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









			//	fftw_fprint_plan(p, stderr);


	/*		double temp, temp2;
			double smpl=0;
			double smpl_nxt=0;
			double per;
	

			per = (double)rms_stop - 1/freq*100000000 + 1/((double)cycles);
		
			fprintf(stderr,"%f-",per*rms_stop);

			int smpl_i=0, smpl_nxt_i = 0, per_i=41;

			for (i=0;i<rms_stop;i++)
			{
						
				smpl_nxt = smpl + per;
				while(smpl_nxt>=(rms_stop))
					smpl_nxt-= (rms_stop);




				temp = samples[(int)floor(smpl)];			
				temp2 = samples[(int)ceil(smpl)];			
				temp = temp * (ceil(smpl)-smpl) + temp2 * (smpl-floor(smpl));
				y = temp * scale+screen->h/2;

				temp = samples[(int)floor(smpl_nxt)];			
				temp2 = samples[(int)ceil(smpl_nxt)];			
				temp = temp * (ceil(smpl_nxt) -smpl_nxt) + temp2 * (smpl_nxt-floor(smpl_nxt));
				y_2 = temp * scale+screen->h/2;


				if (y > y_2)
				{
					smpl_nxt=y;
					y = y_2;
					y_2 = smpl_nxt;
				}

				for (;y<=(y_2 - (y_2-y)/2);y++)
					my_putpixel(screen,i,y,0xFF, 0xFF,0);	

				temp = samples[(int)round(smpl)];
	my_putpixel(screen,i,y,0xFF, 0xFF,0);			
	smpl += per;
				while(smpl>=rms_stop)
					smpl-= rms_stop;
				
			}*/

		}
	}

    if(SDL_MUSTLOCK(screen)) 
		SDL_UnlockSurface(screen);

    SDL_Flip(screen); 
}





void my_sighandler(int sig)
{
fprintf(stderr,"jeb....\n");
	SDL_Quit();
exit(-1);
}

main()
{
    int i;
	int N1;
	int range = 0;
    int channel = 4;
    int offset = 32768;
    int nsamples = 2048;
    int buf[2048];
	
	double samples_in[2048];	
	int t = 1;

	
	int x_scale = 1;
	float scale = 256;
    SDL_Surface *screen;
    
    SDL_Event event;             
              
    int keypress = 0;
    int h=0; 

	signal(SIGINT, my_sighandler);
                  
    adc_init();
	i2c_init(BASE_I2C_CLKGEN);	
	i2c_init(BASE_I2C_IDMEM);

	unsigned char temp_char[2];
	temp_char[0] = 0x80;
	i2c_write(BASE_I2C_CLKGEN, 0xAA, 135, temp_char, 1);
	usleep(100000);
	i2c_read(BASE_I2C_CLKGEN, 0xAA, 0x07, temp_char, 2);						
	N1 = ((temp_char[0] & 0x1F) << 2) | ((temp_char[1] >> 6) & 0x03);




    adc_set_offset(channel, offset);
 	adc_set_range(channel, ADC_RANGE_100mV, t);

    if (SDL_Init(SDL_INIT_VIDEO) < 0 ) 
    	return 1;
                               
    if (!(screen = SDL_SetVideoMode(WIDTH, HEIGHT, DEPTH, SDL_HWSURFACE)))
    {
    	SDL_Quit();
        return 1;
    }
    

	if(TTF_Init()!=0) /* 0 sukces, -1 porażka */
	{
		/* Zwracamy błąd, nie udało się zainicjować SDL_ttf */
		fprintf( stderr, "Unable to init SDL_ttf: %s\n",TTF_GetError());
		exit(1);
	}

	/* Pobieramy fonta wielkości 20dpi*/
	fonts=TTF_OpenFont("/usr/share/fonts/truetype/tahoma/Tahoma.TTF", 13);
	if(!fonts)
	{
		fprintf(stderr, "TTF_OpenFont: %s\n", TTF_GetError());
		exit(1);
	}
	


	while (!keypress) 
    {
		
		adc_record_single(channel, buf, nsamples, 0/*int pre_trigger*/);
		
		for(i=0;i<2048;i++)
			samples_in[i]=-1*((float)buf[i]-8192)/8192;
	    
		DrawScreen(screen,samples_in,scale, x_scale);
	
 	   	
        while(SDL_PollEvent(&event)) 
        {      
       		switch (event.type) 
            {
            case SDL_QUIT:
            	keypress = 1;
                break;
            case SDL_KEYDOWN:
				{            
					fprintf(stderr, "--> %d <--",event.key.keysym.scancode);

					if (event.key.keysym.scancode == 27) //range - r
					{
						range++;
						range %= 3;
						if (range == 0)
						 	adc_set_range(channel, ADC_RANGE_100mV, t);
						if (range == 1)
						 	adc_set_range(channel, ADC_RANGE_1V, t);
						if (range == 2)
						 	adc_set_range(channel, ADC_RANGE_10V, t);
					}
					else if (event.key.keysym.scancode == 39) //y-scale - s
					{
						scale *= 2;
						if (scale > 40000)
							scale = 256;
					}
					else if (event.key.keysym.scancode == 111) //offset - up
					{
						offset++;					
					    adc_set_offset(channel, offset);
					}
					else if (event.key.keysym.scancode == 116) //offset - down
					{
						offset--;					
					    adc_set_offset(channel, offset);
					}
					else if (event.key.keysym.scancode == 54) //channel - c
					{
						channel++;
						if (channel == 5)
							channel = 3;					
					}
					else if (event.key.keysym.scancode == 38) //clear avg measurements - a
					{
						freq_avg = 0; 
						rms_avg = 0;
						pp_avg = 0;
						no = 0;	
						noise_power=0;
						noise_mean=0;
					}
					else if (event.key.keysym.scancode == 53) //x-scale - x
					{
						x_scale*=2;
						if (x_scale == 64)
							x_scale = 1;	
					}
					else if (event.key.keysym.scancode == 41) //clearing screen - f
					{
						if (cls)
							cls=0;
						else
							cls=1;						
					}
					else if (event.key.keysym.scancode == 40) //averaging - d
					{
						if (sig_avg)
							sig_avg=0;
						else
							sig_avg=1;		
					}				
					else if (event.key.keysym.scancode == 26) // fft - e
					{
						e++;
						e%=3;						
					}
					else if (event.key.keysym.scancode == 28) //termination - t
					{
						if (t)
							t=0;
						else
							t=1;						
						if (range == 0)
						 	adc_set_range(channel, ADC_RANGE_100mV, t);
						if (range == 1)
						 	adc_set_range(channel, ADC_RANGE_1V, t);
						if (range == 2)
						 	adc_set_range(channel, ADC_RANGE_10V, t);						
					}
					else if (event.key.keysym.scancode == 25) //window - w
					{
						if (w)
							w=0;
						else
							w=1;
					}					
					else if (event.key.keysym.scancode == 58) // temp measurement - m
					{
						float temp = 25;
						
						//i2c_scan_bus(BASE_I2C_CLKGEN);
						//i2c_scan_bus(BASE_I2C_IDMEM);
						//thermometer base addres: 0x90
						
												
						uint8_t temp_char[2];
						
						temp_char[0] = 0x60;
						i2c_write(BASE_I2C_CLKGEN, 0x90, 0x01, temp_char, 1);						
						i2c_read(BASE_I2C_CLKGEN, 0x90, 0x00, temp_char, 2);
						fprintf(stderr, "\ntemperature: %f Celsius degrees\n\n", (float)temp_char[0] + (float)temp_char[1]/256);
						do {
							while(SDL_PollEvent(&event));
						} while (event.type != SDL_KEYDOWN);
						 
					}
					else if ((event.key.keysym.scancode == 59) || (event.key.keysym.scancode == 60)) // freq mod: < >
					{
						uint8_t temp_char[2];
						int N1_temp;						

						
						if (event.key.keysym.scancode == 59)
						{	
							base_freq *= 2;
							if (base_freq > 100000000)
								base_freq = 12500000;
						}
						
						if (event.key.keysym.scancode == 60)
						{	
							base_freq /= 2;
							if (base_freq < 12500000)
								base_freq = 100000000;
						}


						N1_temp = (N1+1) * 100000000/base_freq;

						N1_temp--;

						i2c_read(BASE_I2C_CLKGEN, 0xAA, 0x07, temp_char, 2);
						
						temp_char[0] &= 0xE0;
						temp_char[0] |= N1_temp >> 2;
						temp_char[1] &= 0x3F;
						temp_char[1] |= (N1_temp & 0x03) << 6;
 						
						i2c_write(BASE_I2C_CLKGEN, 0xAA, 0x07, temp_char, 2);						
						fprintf(stderr, "\nfrequency: %ld Hz, %d\n\n", base_freq, N1_temp);
					}
					else if (event.key.keysym.scancode == 65) // pause - spacja
					{
						l++;
						l%=2;
					}
					else if (event.key.keysym.scancode == 34) // write mem - [
					{
						uint8_t temp_char[1];	
								
						for (i=0;i<256;i++)
						{
							temp_char[0] = 255-i;
							i2c_mem_write(0xA4, i, temp_char, 1);
							usleep(1000);
						}
						fprintf(stderr, "\n256 bytes written.\n");
					}
					else if (event.key.keysym.scancode == 35) // read mem - ]
					{
						uint8_t temp_char[1] = {'D'};	
						for (i=0;i<256;i++)
						{
							i2c_mem_read(0xA4, i, temp_char, 1);
							fprintf(stderr, "data: %c\n", temp_char[0]);
						}
							
					}
					else if (event.key.keysym.scancode == 29) // dB scale change - y
					{
						y_dB_scale *=2;
						if (y_dB_scale > 16)
							y_dB_scale = 1;							
					}
					else
					{
						keypress = 1;
					}

                	break;
	            }
			}
        }
		 
    }
    SDL_Quit();
	TTF_CloseFont(fonts);    
	return 0;
}
