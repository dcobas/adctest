from numpy import*
from math import sin, pi, atan
import matplotlib.pyplot as p

def sine_samples(n):
    """Produce a vector of samples of sine in [0..2 pi]"""
    samples = []
    for i in range(n):
        samples.append(sin(2*pi*i/n))
    return samples

x=input("give number of samples :")
vec=sine_samples(x)

for element in vec:
   print element

b=fft.fft(vec)
print("now i'll show you the FFT of it")
print(b)
c=atan(b[0].imag/b[0].real)
d=atan(b[x-1].imag/b[x-1].real)
print("modulus of the first harmonic:")
print(abs(b[0]))
print("argument of the first harmonic:")
print(c)
print("modulus of the last harmonic:")
print(abs(b[x-1]))
print("argument of the last harmonic:")
print(d)

#if you put x=9 it gives you d=1.57079632679 but my calculator gives d=1.431169...so,where is the mistake?
