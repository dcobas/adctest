from math import *
from matplotlib import pyplot as plt
from numpy import *


name=raw_input("give me the name of the file :")
f=file(name)
a=[]
b=[]
i=0
for line in f:
    value=int(line)
    a.append(value)
    b.append(i)
    i=i+1

plt.plot(b,a)
plt.show()
