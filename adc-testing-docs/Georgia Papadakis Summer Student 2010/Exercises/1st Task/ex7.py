from math import sin, pi
from sys import argv


def sine_samples(n):
    """Produce a vector of samples of sine in [0..2 pi]"""
    samples = []
    for i in range(n+1):
        samples.append(sin(2*pi*i/n))
    return samples

def print_vector(v):
    for element in v:
        print element

if __name__ == '__main__':      # the usual idiom for a main program

#    samples = input("give a number: ")
#   samples = int(argv[1])
    if len(argv)==1:
      samples = input("give a number: ")
    else:
        samples = int(argv[1])


      
    vec = sine_samples(samples)
    print_vector(vec)

    
 
    
