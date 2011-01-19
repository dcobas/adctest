from math import *
from matplotlib import pyplot as plt
from numpy import *

def histo(bits, samples):
    
    #making the histogram of the digital samples of a sinewave#
    c=[]
    d=[]
    c,d=histogram(samples,2**bits)
    plt.hist(samples,2**bits)
    plt.show()
    return c
    






b=input("give number of bits :")

name=raw_input("give me the name of the file :")
f=file(name)
a=[]
for line in f:
    value=int(line)
    a.append(value)

e=[]
e=histo(b,a)
print e[:]
