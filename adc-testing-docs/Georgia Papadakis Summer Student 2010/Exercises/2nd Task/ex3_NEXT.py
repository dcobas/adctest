from numpy import*
from math import sin, pi
import matplotlib.pyplot as pl


def argument(n,sampl_rate,fr,ph):
    #produce a vector of the arguments of the sinewave#
    arg=[]
    for i in range(n):
        arg.append(2*pi*fr*i/sampl_rate+ph*2*pi)
    return arg
    

def make_sinewave (n,v,amp):
    #produces the values if the sinewave#
    b=[]
    for i in range (n):
        b.append(amp*sin(v[i]))
    return b             
        


a=input("please give amplitude:")
f=input("please give the sinewave's frequency:")
p=input("please give phase(rad):")
sr=input("please give sampling rate:")
s=input("please give number of samples:")

vector=argument(s,sr,f,p)

print("these are the arguments of the sinewave")

print vector[:]
    
print ("these are the values of the sinewave")

sine=make_sinewave(s,vector,a)
sine=array(sine)

print sine[:]

b=array(random.random(s)-1)

print ("this is the noise") 

print b[:]

c=array(b+sine)
print("the sum of the sinewave and the noise is:")
print c[:]

#SNR calculation#
sine_rss=0
noise_rss=0

for i in range (s):
    sine_rss=sine_rss+sine[i]*sine[i]
    noise_rss=noise_rss+b[i]*b[i]

SNR=sine_rss/noise_rss
print ("the SNR is" ) ,10*log10(SNR)

#creation of the plot#
g=range(s)

pl.plot(g, c)
pl.show()
