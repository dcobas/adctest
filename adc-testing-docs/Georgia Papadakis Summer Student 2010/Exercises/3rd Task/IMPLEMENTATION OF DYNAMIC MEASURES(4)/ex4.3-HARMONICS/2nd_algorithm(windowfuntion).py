from math  import *
from numpy import *
from matplotlib import pyplot as plt

##################### OPEN THE FILE ###################################

name=raw_input("GIVE ME THE NAME OF THE FILE:")
f=open(name)
a=[]
for line in f:
    value=int(line)
    a.append(value)
    
#################### MAKING THE FFT ###################################
    
a=a-mean(a)
a=array(a)
asize=a.size
x=log2(asize)
print ("SIZE OF a IS: "),asize
print ("THE SIZE OF a EQUALS TO:  2 TO THE "),x
b=abs(fft.fft(a))
maxb=max(b)
d=b/maxb
e=log10(d)
f=20*e
h=fft.fftshift(f)
m=h.size


################ I 'LL MAKE A COUPLE:VECTOR h AND VECTOR freq #################################

freq=[]
for i in range (m):
    freq.append(-50000000+i*100000000/m)

######## I'LL MAKE ANOTHER COUPLE:Vector hhalfh AND VECTOR freq_shift ##########################
    
hhalf=[]
freq_shift=[]
for i in range(m/2,m):
    freq_shift.append(freq[i])
    hhalf.append(h[i])
hhalf=array(hhalf)
freq_shift=array(freq_shift)
ser=hhalf.size
print ("SIZE OF hhalf IS:"),ser

########## FINDING THE POSITION OF THE MAXMUM OF hhalf=>EXPECTING THE INPUT FREQUENCY #########

for i in range (ser):
    maximum=hhalf[i]
    for j in range (ser):
        if hhalf[j]>maximum:
            maximum=hhalf[j]
            sinefreq=freq_shift[j]
print("the frequency of the sinewave is "),sinefreq    
print("maximum of hhalf is "),maximum  

#************************************************************************HARMONICS**********************************************************************************

#############WINDOW FUNCTION################
nbart=asize/2
d=hamming(nbart)
print d[:]


#e=abs(fft.fft(d))
#e=array(e)
#maximum=max(e)
#f=e/maximum
#g=log10(f)
#h=20*g
#i=fft.fftshift(h)
#plt.plot(i)
#plt.show()
gerog=a[0:(asize/2)]
print ("size of gerog is:"),gerog.size
gerog=array(gerog)
d=array(d)
mult=d*gerog
mult=array(mult)
mult1=abs(fft.fft(mult))
maxmult1=max(mult1)
mult2=mult1/maxmult1
mult3=log10(mult2)
mult4=20*mult3
mult5=fft.fftshift(mult4)
multsize=mult5.size


freq_shift1=[]
for i in range (gerog.size):
    freq_shift1.append(-50000000+i*100000000/nbart)


freq_shift1=array(freq_shift1)
plt.plot(freq_shift1,mult5)
plt.title("The FFT of the signal")
plt.xlabel("frequency")
plt.ylabel("dB")
plt.show()



