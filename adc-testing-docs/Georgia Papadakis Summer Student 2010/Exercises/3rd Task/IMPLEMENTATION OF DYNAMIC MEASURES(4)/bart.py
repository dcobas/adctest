from numpy import*
from numpy import bartlett
import matplotlib.pyplot as plt


n=input("the number of samples is :")
d=bartlett(n)
print d[:]

#plt.plot(d)
#plt.show()

e=abs(fft.fft(d))
e=array(e)
maximum=max(e)
f=e/maximum
g=log10(f)
h=20*g
i=fft.fftshift(h)

plt.plot(i)
plt.show()
