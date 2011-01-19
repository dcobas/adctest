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
sep=freq_shift.size
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

#************************************* HARMONICS *********************************************#

position=[]
distortion=[]

if x%2==0 :
    ################## 64 ##########################(x=12)
    for i in range(int(2**(x/2))):
        vector=[]
    ######################### 32 ###################
        for j in range(int(2**((x/2)-1))):
            vector.append(hhalf[j+i*(2**((x/2)-1))])
        vector=array(vector)
        maxh=max(vector)
        for j in range(int(2**((x/2)-1))):
            if vector[j]>=maxh:
               maxh=vector[j]
               position.append(freq_shift[j+i*(2**((x/2)-1))])
               distortion.append(vector[j])
        
else :
    ########################## 128 #################(x=13)
    for i in range(int((2**((x+1)/2)))):
        vector=[]
    ############################ 32 ################
        for j in range(int(2**(((x-1)/2)-1))):
            vector.append(hhalf[j+i*(2**(((x-1)/2)-1))])
        vector=array(vector)
        maxh=max(vector)
        for j in range(int(2**(((x-1)/2)-1))):
            if vector[j]>=maxh:
               maxh=vector[j]
               position.append(freq_shift[j+i*(2**(((x-1)/2)-1))])
               distortion.append(vector[j])

print("THE POSITION OF THE HARMONICS ARE :"),position[:]
                   



plt.plot(freq_shift,hhalf)
plt.title("The FFT of the signal")
plt.xlabel("frequency")
plt.ylabel("dB")
plt.show()













