from math  import *
from numpy import *
from matplotlib import pyplot as plt

##################### OPEN THE FILE ###########################################################
num_of_bits=input("GIVE ME THE NUMBER OF BITS :")
real_amplit=input("GIVE ME THE INPUT AMPLITUDE :")                #(I NEED both real_amplit AND full_scale_amplitud 
full_scale_amplitude=input("GIVE ME THE FULLSCALE AMPLITUDE :")   # IN ORDER TO MEASURE ENOB )
name=raw_input("GIVE ME THE NAME OF THE FILE:")
f=open(name)
a=[]
for line in f:
    value=int(line)
    a.append(value)

#################### MAKING THE FFT ###########################################################
a=a-mean(a)
a=array(a)
asize=a.size
x=log2(asize)
print ("NUMBER OF SAMPLES ARE(-SIZE OF a IS) : "),asize
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

######## I'LL MAKE ANOTHER COUPLE:Vector hhalfh AND VECTOR freq_shift #########################
    
hhalf=[]
freq_shift=[]
for i in range(m/2,m):
    freq_shift.append(freq[i])
    hhalf.append(h[i])
hhalf=array(hhalf)
freq_shift=array(freq_shift)
ser=hhalf.size
print ("SIZE OF hhalf IS:"),ser
########## SEARCH FOR THE POSITION OF THE MAXMUM OF hhalf=>EXPECTING THE INPUT FREQUENCY #########

for i in range (ser):
    maximum=hhalf[i]
    for j in range (ser):
        if hhalf[j]>maximum:
            maximum=hhalf[j]
            sinefreq=freq_shift[j]
print("the frequency of the sinewave is "),sinefreq    
print("maximum of hhalf is "),maximum  


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
for i in range (gerog.size):
    if freq_shift1[i]==0:
        flag=i
fourievector=mult5[flag:multsize]
freqvector=freq_shift1[flag:multsize]    #the distance between two elements of freqvector is 2fs/M and not fs/M. -(THE SAME HAPPENS FOR freq_shift1[])
###
#helpvect=mult2[flag:multsize]

################################################ CALCULATION OF THE DISTORTION WHEN THERE IS ALSO PROCESS GAIN SO THE HARMONICS ARE A LITTLE SPREAD ############################################################################

############################################################# THE ARRAYS THAT ARE GOING TO BE USED ARE: fourievector and freqvector ############################################################################################
position=[]
distortion=[]
for i in range (fourievector.size):
    
#I TRY TO FIND THE POSITION OF THE HARMONICS BY SEARCHING IN freq_shift VECTOR FOR FREQUENCIES CLOSE TO THE:f=n*sinefreq #
    
    if (freqvector[i]%sinefreq==0) :#if you find a harmonic                            
        if x%2==0 :                                            
           magnitude=[]                                                                 
           helpfreq=[]
           if i>=2**(((x-2)/2)-1) and i<=fourievector.size-2**(((x-2)/2)-1)-1:
                  for j in range (int(-2**(((x-2)/2)-1)),int(2**(((x-2)/2)-1))):
                      magnitude.append(fourievector[i+j])
                      helpfreq.append(freqvector[i+j])
                     
           elif  i<2**(((x-2)/2)-1):
               for j in range (0,int(i+2**(((x-2)/2)-1))):
                   magnitude.append(fourievector[j])
                   helpfreq.append(freqvector[j])
                   
           else:
               for j in range (int(i-2**(((x-2)/2)-1)),fourievector.size):
                   magnitude.append(fourievector[j])
                   helpfreq.append(freqvector[j])
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
            for j in range(int(-2**(((x-3)/2)-1)),int(2**(((x-3)/2)-1))): 
                 magnitude.append(fourievector[i+j])
                 helpfreq.append(freqvector[i+j])
            magnitude=array(magnitude)
            helpfreq=array(helpfreq)
            maxmag=max(magnitude)
            sizemag=magnitude.size
            for w in range(sizemag):
                if magnitude[w]>=maxmag:
                   maxmag=magnitude[w]
                   position.append(helpfreq[w])
                   distortion.append(magnitude[w])



############################################# I ASSUMED THAT WHEN THERE IS A SIGNAL LEACAGE,ONLY THE HIGHEST PEAK IS A HARMONIC AND THE REST OF THE PEAKS ARE NOTHING,NOT EVEN NOISE ###################

distortion=array(distortion)
distsize=distortion.size
position=array(position)
meandistortion=mean(distortion)

realdistortion=[]
realposition=[]
noise1=[]
for i in range(distsize):
    if (distortion[i]>=meandistortion) and (position[i]>sinefreq):
         realdistortion.append(distortion[i])
         realposition.append(position[i])


         
#*********************************************************** C A L C U L A T I O N  O F  N O I S E ==> SNR *********************************************************************************************
for i in range (ser):
    if hhalf[i]<meandistortion:
        noise1.append(hhalf[i])


noise1=array(noise1)
noisesize=noise1.size
noise2=[]
for i in range(noisesize):
    if noise1[i]>-140.0:
        noise2.append(noise1[i])

print ("THE NOISE FLOOR IS :"),mean(noise2)
snr=maximum-mean(noise2)-10*log10(asize/2)    # there is also the process gain:10*log10(asize/2) #
snr_theoret=6.02*num_of_bits+1.76
print("******************************* SNR ********************************************")
print ("SNR IS (quick and dirty) :" ),snr
print ("SNRtheoretical IS :"),snr_theoret
#*********************************************************************************************************************************************************************************************************





#****************************************************************   C A L C U L A T I O N  O F  D I S T O R T I O N ==> THD ******************************************************************************
print("******************************* THD*********************************************")
print("the REAL position of distortion is: "),realposition[:]

print("the REAL distortion is: "),realdistortion[:]
realposition=array(realposition)
realdistortion=array(realdistortion)
thd1=[]

for i in range (realdistortion.size):
    thd1.append(realdistortion[i]/20.0)
thd1=array(thd1)
thd2=thd1*2
thd2=array(thd2)
thd3=10**(thd2)
thd4=0
for i in range (realdistortion.size-1):
    if thd3[i]!=1 :
        thd4=thd4+thd3[i]
thd=10*log10(thd4)
print ("THD IS :"),thd
#********************************************************************************************************************************************************************************************************




#*********************************************************************************************** C A L C U L A T I O N  O F SINAD *************************************************************************
print("**************************** SINAD ***********************************************")
sinad1=-(snr)/10.0
sinad2=10**(sinad1)
sinad3=-abs(thd)/10.0
sinad4=10**(sinad3)
sinad5=sinad2+sinad4
sinad=-10*log10(sinad5)
print("SINAD IS :"),sinad
#************************************************************************************************************************************************************************************************************




#****************************************************************************************** C A L C U L A T I O N  O F  ENOB ********************************************************************************
print("**************************** ENOB ************************************************")
factor=20*log10(full_scale_amplitude/real_amplit)
enob=(sinad-1.76+factor)/6.02
print ("ENOB IS :"),enob
#*************************************************************************************************************************************************************************************************************


#******************************************************************************************** PLOTTING *******************************************************************************************************
freqvector=array(freqvector)
fourievector=array(fourievector)
plt.plot(freqvector,fourievector)
plt.title("The FFT of the signal")
plt.xlabel("frequency")
plt.ylabel("dB")
plt.show()
