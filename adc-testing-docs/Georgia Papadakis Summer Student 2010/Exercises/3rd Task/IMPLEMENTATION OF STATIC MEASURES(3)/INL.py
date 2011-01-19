from math import *
from matplotlib import pyplot as plt
from numpy import *

##########MAKING THE HISTOGRAM##################
def histo(bits, samples):
    
    c=[]
    d=[]
    c,d=histogram(samples,2**bits)
    plt.hist(samples,2**bits)
#   plt.show()
    return c
    

b=input("give number of bits :")
name=raw_input("give me the name of the file :")
f=open(name)
a=[]
for line in f:
    value=int(line)
    a.append(value)
    

#########CALCULATE THE NUMBER OF SAMPLES###########
a=array(a)
mt=a.size
print ("number of samples is"),mt
###################################################

e=[]
e=histo(b,a)
print ("the number of occurencies per bin are "),e[:]
h_first=e[0]
last=int(2**b-1)
h_last=e[last]


#########CALCULATING THE ESTIMATED AMPLITUDE########
fsr=input("give me fsr: ")
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
