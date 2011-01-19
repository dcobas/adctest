from numpy import*
from math import sin, pi
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

print("and now the FFT of it:")
print fft.fft(vec)
