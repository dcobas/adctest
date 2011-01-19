from numpy import*
from numpy import bartlett
import matplotlib.pyplot as plt


n=input("the number of samples is :")
d=bartlett(n)
print d[:]

plt.plot(d)
plt.show()

e=fft.fft(d)
f=abs(e)
n=f.size
print n

