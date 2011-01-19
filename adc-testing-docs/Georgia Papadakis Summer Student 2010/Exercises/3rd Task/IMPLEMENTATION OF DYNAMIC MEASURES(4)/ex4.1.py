from math import *
from numpy import *
from matplotlib import pyplot as plt


name=raw_input("give me the name of the file :")
f=open(name)
a=[]
for line in f:
    value=int(line)
    a.append(value)

b=fft.fft(a)
c=abs(b)

#n=b.size
#c=abs(b)
#h=[]
#i=[]
#h,i=histogram(c,n)
#plt.hist(c,n)
#plt.show()





