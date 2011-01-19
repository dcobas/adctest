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
print ("freq_shift is :"),freq_shift
########## FINDING THE POSITION OF THE MAXMUM OF hhalf=>EXPECTING THE INPUT FREQUENCY #########

for i in range (ser):
    maximum=hhalf[i]
    for j in range (ser):
        if hhalf[j]>maximum:
            maximum=hhalf[j]
            sinefreq=freq_shift[j]
print("the frequency of the sinewave is "),sinefreq    
print("maximum of hhalf is "),maximum  

#*****************************************************************************HARMONICS**************************************************************
position=[]
distortion=[]
for i in range (ser):
#I TRY TO FIND THE POSITION OF THE HARMONICS BY SEARCHING IN freq_shift VEVTOR FOR FREQUENCIES CLOSE TO THE:f=n*sinefreq #    
    if (freq_shift[i]%sinefreq==0) :#if you find a harmonic

        if x%2==0 :
            magnitude=[]
            helpfreq=[]
            for j in range (int(-2**(((x-2)/2)-1)),int(2**(((x-2)/2)-1))):
                magnitude.append(hhalf[i+j])
                helpfreq.append(freq_shift[i+j])
            magnitude=array(magnitude)
            helpfreq=array(helpfreq)
            maxmag=max(magnitude)
            sizemag=magnitude.size
            for w in range(sizemag):
                if magnitude[w]>=maxmag:
                   maxmag=magnitude[w]
                   position.append(helpfreq[w])
                   distortion.append(magnitude[w])

        else:
            magnitude=[]
            helpfreq=[]
            for j in range(int(-2**(((x-3)/2)-1)),int(2**(((x-3)/2)-1))): #(if doubled sampling frequency is used)
                 magnitude.append(hhalf[i+j])
                 helpfreq.append(freq_shift[i+j])
            magnitude=array(magnitude)
            helpfreq=array(helpfreq)
            maxmag=max(magnitude)
            sizemag=magnitude.size
            for w in range(sizemag):
                if magnitude[w]>=maxmag:
                   maxmag=magnitude[w]
                   position.append(helpfreq[w])
                   distortion.append(magnitude[w])

print ("The position vector is:"),position[:]
print ("The distortion vector is:"),distortion[:]

distortion=array(distortion)
distsize=distortion.size
position=array(position)
meandistortion=mean(distortion)
print("the mean value of distort is :"),meandistortion


##################
realdistortion=[]
realposition=[]
for i in range(distsize):
    if distortion[i]>=meandistortion:
         realdistortion.append(distortion[i])
         realposition.append(position[i])

print("the REAL position of distortion is: "),realposition[:]

print("the REAL distortion is: "),realdistortion[:]























########
plt.plot(freq_shift,hhalf)
plt.title("The FFT of the signal")
plt.xlabel("frequency")
plt.ylabel("dB")
plt.show()

