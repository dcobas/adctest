from math import *
from matplotlib import pyplot as plt
from numpy import *
#################################################################### CREATING THE DISTORTED SINEWAVE #################################################

def make_sinewaveforunipolar (n,sampl_rate,fr,ph,amp,fullsr):
    #produces the values of the sinewave#
    b=[]
    maj=[]
    for i in range (n):
        b.append(fullsr/2.0+amp*sin(2.0*pi*fr*i/sampl_rate+ph*2.0*pi))
       #b.append(fullsr/2+amp*sin(2*pi*fr*i/sampl_rate+ph*2*pi)+0.02*amp*sin(4.44*pi*fr*i/sampl_rate+ph*2*pi)+0.09*amp*sin(6.66*pi*fr*i/sampl_rate+ph*2*pi))
    return b

def make_sinewaveforbipolar (n,sampl_rate,fr,ph,amp,fullsr):
    #produces the values of the sinewave#
    b=[]
    for i in range (n):
        b.append(amp*sin(2.0*pi*fr*i/sampl_rate+ph*2.0*pi))
        #b.append(amp*sin(2.0*pi*fr*i/sampl_rate+ph*2.0*pi)+0.02*amp*sin(4.44*pi*fr*i/sampl_rate+ph*2*pi)+0.09*amp*sin(6.66*pi*fr*i/sampl_rate+ph*2*pi))
    return b

#################################################################### ANALOG TO DIGITAL ################################################################
def adc_transferunipolar(v, fsr, bits):
    
    #MAKING THE TRANSFER FUNCTION FOR UNIPOLAR ADC
    a=2.0**bits
    lsb=float(fsr/a)
    digital=[]
    analog=[]
    for i in range (int(a)):
        b=lsb*i
        analog.append(b)
        digital.append(i)
    
    #PLOTTING THE TRANSFER FUNCTION
    #pl.plot(analog, digital)
    #pl.show()
    #AND NOW THE CORRESPONDENCE!!!
   
    i=0
    if (v>=analog[0]) and (v<=analog[int(math.pow(2,bits)-1)]):
       while i<=a-1:
           if (v>=analog[i]) and (v<analog[i+1]):
               d=(digital[i])
           i=i+1
    elif (v>analog[int(math.pow(2,bits)-1)]) :
        d=( digital[int(math.pow(2,bits)-1)])
    else:
        d=(digital[0])

    return d

def adc_transferbipolar(v, fsr, bits,vfs):
    
    #MAKING THE TRANSFER FUNCTION FOR BIPOLAR ADC
    a=2.0**bits
    lsb=float(fsr/a)
    digital=[]
    analog=[]
    for i in range (int(a)):
        b=-vfs+lsb*i
        analog.append(b)
        digital.append(i)
    
    #PLOTTING THE TRANSFER FUNCTION
    #plt.plot(analog, digital)
    #plt.show()
    #AND NOW THE CORRESPONDENCE!!!
   
    i=0
    if (v>=analog[0]) and (v<=analog[int(math.pow(2,bits)-1)]):
       while i<=a-1:
           if (v>=analog[i]) and (v<analog[i+1]):
               d=(digital[i])
           i=i+1
    elif (v>analog[int(math.pow(2,bits)-1)]) :
        d=( digital[int(math.pow(2,bits)-1)])
    else:
        d=(digital[0])

    return d

#################################################################### MAKING THE HISTOGRAM #############################################################
#def histo(bits, samples):
#    c=[]
#    d=[]
#    c,d=histogram(samples,2**bits)
#    plt.hist(samples,2**bits)
#    plt.show()
#    return c

def histo(bits,samples):
    samples=array(samples)
    c=[]
    for i in range (2**bits):
        c.append(0)
    i=0

    
    for j in range (2**bits):      
        for i in range(samples.size):
            if (samples[i]==j):
                c[j]=c[j]+1

    return c
            

##################################################################### THE INPUTS #######################################################################
#b=input("give number of bits :")
#fsr=input("give me fsr(volts): ")
#a=input("please give amplitude(volts):")
#f=input("please give the sinewave's frequency(Hertz):")
#p=input("please give phase:")
#sr=input("please give sampling rate(Hertz):")
#s=input("please give number of samples:")
#bipolar=input("if the ADC is bipolar then press 1,else press 0 :")
b=8
fsr=10
a=5
f=0.31415164576
p=0
sr=8000
s=100000
bipolar=1

#######################################
fs=fsr/2
    
samples=[]            #making the sinewave's samples
if (bipolar==0):
    samples=make_sinewaveforunipolar(s,sr,f,p,a,fsr)
elif (bipolar==1):
    samples=make_sinewaveforbipolar(s,sr,f,p,a,fsr)
samples=array(samples)
    
dig_samples=[]        #the convertion
if (bipolar==0):
    for i in range (s):
        dig_samples.append(adc_transferunipolar(samples[i], fsr, b))
elif (bipolar==1):
     for i in range (s):
         dig_samples.append(adc_transferbipolar(samples[i], fsr, b, fs))
dig_samples=array(dig_samples)
#to be sure that the frequency of the sinewave and the sampling frequency are not correlated,i need dig_samples to have a lot of different from each other values
e=[]
e=histo(b,dig_samples)
#print ("the number of occurencies per bin are "),e[:]
print ("                                          ")
e=array(e)
ala=0 #this variable shows the number of different values
for i in range (e.size):
	if (e[i]!=0):
		ala=ala+1

h_first=e[0]
last=e.size
h_last=e[last-1]


#########CALCULATING THE ESTIMATED AMPLITUDE########
lsb=fsr/(2.0**b)
print("the lsb is :"),lsb
print ("                                          ")
g=(math.pi/2)
help1=float(s+h_first+h_last)
help2=float((s/help1))
w=float((g*(help2)))
k=float(math.sin(float(w)))
amp=float(fs/k)
print("the  estimated amplitude is "),amp
print ("                                          ")
####################################################

##########CALCULATING THE p(n)######################
p=[]
twobits = 2.0**b
twobits1 = 2.0**(b-1)
pirecip  = 1.0/math.pi
for i in range(1,int(twobits)+1):
    p.append(pirecip*( math.asin(2*fs*(i  -twobits1)/(amp*twobits)) - math.asin(2*fs*(i-1-twobits1)/(amp*twobits)) ))
p=array(p)
print ("                                          ")

##########CALCULATING h(n)theoretical##############
h=[]
for i in range(p.size):
    h.append(p[i]*s)
#print("                                           ")
h=array(h)
#print("the theoretical number of samples is :"),sum(h)
############CALCULATING DNL ERROR###################
dnl=[]
help4=0.0
help5=0.0
#for i in range (1,2**b+-1):
for i in range (0,2**b):
    help4=(e[i]/h[i])
    help5=help4-1.0
    dnl.append(help5)
dnl=array(dnl)
alala=0
for i in range ((2**b)-2):
        	if (dnl[i]!=-1.0):
	        	alala=alala+1   #this variable calculates how many different values dnl vector has
	        	
##print ("T H E  DNL  E R R O R S   A R E   :"),dnl[:]
##########CALCULATING INL ERROR#####################
dnl=dnl[1:dnl.size-2]
inl=[]
for i in range (dnl.size):
    inl.append(0)
for i in range (dnl.size):
    for j in range (i+1):
        inl[i]=inl[i]+dnl[j]
    
print(inl[0])
print (" The maximum deviation of the transfer function is :") ,max(dnl) ,("LSBs.Which means :"), ((max(dnl)/(2**b))*100),("%FSR.") 
####################################################
	            
rang=range(dig_samples.size)
plt.plot(rang,samples,rang,dig_samples)
plt.plot(inl)
plt.plot(dig_samples)
plt.show()
