from numpy import*
from math import *
import matplotlib.pyplot as plt

##############################MAKING THE SINEWAVE######################
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

###############################MAKING THE TRANSFER FUNCTION###########
def adc_transfer(v, fsr, bits,num_of_samples):
    
    #MAKING THE TRANSFER FUNCTION
    c=2**bits
    a=float(2**bits)
    lsb=(fsr/a)
    print("the LSB is"),lsb
    digital=[]
    analog=[]
    for i in range (c):
        b=lsb*i
        analog.append(b)
        digital.append(i)
    
    #PLOTTING THE TRANSFER FUNCTION
    #pl.plot(analog, digital)
    #pl.show()
    
    #AND NOW THE CORRESPONDANCE!!!
    vdig=[]
    for j in range(num_of_samples):
       i=0
       if (v[j]>=analog[0]) and (v[j]<=analog[int(math.pow(2,bits)-1)]):    #if the value given is in tha full scale range#
          while i<c:
              if (v[j]>=analog[i]) and (v[j]<analog[i+1]):
                  flag=digital[i]
                  vdig.append(flag)
                  
              i=i+1
       elif (v[j]>analog[int(math.pow(2,bits)-1)]) :
           vdig.append(digital[int(math.pow(2,bits)-1)])
           
       else:
           vdig.append(digital[0])

    return vdig[:]
            


a=input("please give amplitude:")
f=input("please give the sinewave's frequency:")
p=input("please give phase:")
sr=input("please give sampling rate:")
s=input("please give number of samples:")
vector=argument(s,sr,f,p)
print ("these are the values of the sinewave")
sine=make_sinewave(s,vector,a)
print sine[:]


############################################################################

full_scale_range=input("GIVE ME THE FULL SCALE RANGE: ")
num_of_bits=input("GIVE ME THE NUMBER OF BITS: ")

        
digital_value=adc_transfer(sine,full_scale_range,num_of_bits,s)
print ("THE DIGITAL VALUE CORRESPONDING TO THE ANALOG IS :"),digital_value[:]


####################DNL AND INL ERRORS####################################


##########MAKING THE HISTOGRAM##################
def histo(bits, samples):
    
    c=[]
    d=[]
    c,d=histogram(samples,2**bits)
    plt.hist(samples,2**bits)
#   plt.show()
    return c
    

b=num_of_bits

a=[]
for i in range (s):
    value=digital_value[i]
    a.append(value)
    

#########CALCULATE THE NUMBER OF SAMPLES###########
a=array(a)
mt=s

###################################################

e=[]
e=histo(b,a)
print ("the number of occurencies per bin are "),e[:]
h_first=e[0]
last=int(2**b-1)
h_last=e[last]


#########CALCULATING THE ESTIMATED AMPLITUDE########
fsr=full_scale_range
g=(math.pi/2)
help1=float(mt+h_first+h_last)
help=(mt/help1)
w=(g*(help))
k=float(math.sin(w))
amp=float(fsr/k)
####################################################

##########CALCULATING THE p(n)######################
p=[]              
print("the amplitude is "),amp
for i in range(2**b):
    twobits = 2**b
    twobits1 = 2**(b-1)
    pirecip  = 1/math.pi
    p.append(pirecip * (math.asin(fsr*(i  -twobits1)/(amp*twobits))
                       -math.asin(fsr*(i-1-twobits1)/(amp*twobits))))

print p[:]
####################################################

h=p*mt
inl=0
############CALCULATING DNL ERROR###################
dnl=[]
for i in range (2**b):
    dnl.append(e[i]/h[i]-1)
    inl=inl+dnl[i]

print ("T H E  DNL  E R R O R S   A R E   :"),dnl[:]
####################################################                        
print ("T H E  INL  E R R O R S   A R E   :"),inl



