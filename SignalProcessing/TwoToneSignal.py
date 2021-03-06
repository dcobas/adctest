__author__ = "Federico Asara"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Federico Asara", "Juan David Gonzalez Cobas"]
__license__ = "GPL2"
__version__ = "1.0.0"
__maintainer__ = "Federico Asara"
__email__ = "federico.asara@gmail.com"
__status__ = "Production"

from Signal import *

def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:      
        a, b = b, a % b
    return a

def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)

class TwoToneSignal(Signal):
    """A class that represent a time-domain sampled signal with two sinusoids
    with similiar frequenciess. 
    """
    m1 = 0
    m2 = 0
    tow1 = 0.
    tow2 = 0.
    
    def __init__(self, nbits = 0, rate = 1, data = []):
        """initialize a signal object

        nbits: bit width of the sample values
        rate: sampling rate of sample production
        data: an array of samples (usually nbits-long words, stored in
              a numpy array)
        """
        super(TwoToneSignal, self).__init__(nbits, rate, data)
        
    
    def items(self):
        output = super(TwoToneSignal, self).items()
        
        output.append(('Peak 1 at', "%d bin", self.m1))
        output.append(('Peak 2 at', "%d bin", self.m2))
        output.append(('Guess for wave 1', "%f Hz", self.tow1/2./pi))
        output.append(('Guess for wave 2', "%f Hz", self.tow2/2./pi))
        
        output.append(('Sine 1 frequency', "%f Hz", self.w1/2./pi))
        output.append(('Sine 1 A', "%f", self.a1))
        output.append(('Sine 1 B', "%f", self.b1))
        output.append(('Sine 1 amplitude', "%f", self.amplitude1))
        output.append(('Sine 1 phase', "%f", self.phase1))
        output.append(('Sine 2 frequency', "%f Hz", self.w2/2./pi))
        output.append(('Sine 2 A', "%f", self.a2))
        output.append(('Sine 2 B', "%f", self.b2))
        output.append(('Sine 2 amplitude', "%f", self.amplitude2))
        output.append(('Sine 2 phase', "%f", self.phase2))
        
        output.append(('DC component', "%f", self.c0))
        
        output.append(('IMD', "%f dBc", self.imd))
        
        return output    
    
    def toi(self, x):
        return self.nsamples*x/2/pi/self.rate
    
    def precalculateAll(self):
        """Evaluates all the parameters of the signal, and also call the
        precalculate method for each window function we know."""
        
        # ok, compute the FFT
        ff = abs(fft.fft(self.fulldata))
        lbnd = max(ff) * 10e-12
        self.fft = ff = where(ff < lbnd, 10e-12, ff) 
        
        hff = ff[:len(ff)/2]
        
        self.lfft = lff = 10*log10(ff)
        
        self.m1 = m1 = argmax(hff); 
        self.m2 = m2 = argmax(hstack([hff[:m1-1], array([0, 0, 0]), hff[m1+2:]]))
        
        self.tow1 = tow1 = 2*pi*self.rate*float(m1)/self.nsamples
        self.tow2 = tow2 = 2*pi*self.rate*float(m2)/self.nsamples
        
        (self.w1, self.a1, self.b1), (self.w2, self.a2, self.b2), self.c0 = \
            Sinefit.doubleSinefit4matrix(self.fulldata, self.rate**-1, tow1, tow2)
        
        self.amplitude1 = hypot(self.a1, self.b1)
        self.amplitude2 = hypot(self.a2, self.b2)
        self.phase1 = arctan2(self.b1, self.a1)
        self.phase2 = arctan2(self.b2, self.a2)
        
        # cut right now
        N1 = floor(0.5 + 2*pi*self.rate/self.w1)
        N2 = floor(0.5 + 2*pi*self.rate/self.w2)
        N0 = lcm(N1, N2)
        
        N = self.nsamples -(self.nsamples%N0)
        
        if N0 % 2:
            print N0, 'is odd'
            while ((N/N1 -N/N2) % 2) == 1:
                print (N/N1 -N/N2), 'is odd'
                N -= N0
        else:
            print N0, 'is even'
        
        ff = abs(fft.fft(self.fulldata))
        lbnd = max(ff) * 10e-12
        self.fft = ff = where(ff < lbnd, 10e-12, ff) 
        
        hff = ff[:len(ff)/2]
        
        self.lfft = lff = 10*log10(ff)
        
        self.m1 = m1 = argmax(hff); 
        self.m2 = m2 = argmax(hstack([hff[:m1-1], array([0, 0, 0]), hff[m1+2:]]))
        
        self.tow1 = tow1 = 2*pi*self.rate*float(m1)/self.nsamples
        self.tow2 = tow2 = 2*pi*self.rate*float(m2)/self.nsamples
        
        (self.w1, self.a1, self.b1), (self.w2, self.a2, self.b2), self.c0 = \
            Sinefit.doubleSinefit4matrix(self.fulldata, self.rate**-1, tow1, tow2)
        
        self.amplitude1 = hypot(self.a1, self.b1)
        self.amplitude2 = hypot(self.a2, self.b2)
        self.phase1 = arctan2(self.b1, self.a1)
        self.phase2 = arctan2(self.b2, self.a2)
        
        delta = abs(self.w1 - self.w2)
        
        i1 = min([self.w1, self.w2]) - delta
        i2 = max([self.w1, self.w2]) + delta
        
        temp1, temp2 = self.toi(self.w1), self.toi(self.w2)
        fw1, fw2 = max(self.fft[temp1-1:temp1+2]), max(self.fft[temp2-1:temp2+2])
        
        temp1, temp2 = self.toi(i1), self.toi(i2)
        fi1, fi2 = max(self.fft[temp1-1:temp1+2]), max(self.fft[temp2-1:temp2+2])
        
        print fw1, fw2
        print fi1, fi2
        meaningful = hypot(fw1, fw2)
        interferences = hypot(fi1, fi2)
        
        self.imd = 10*log10(meaningful/interferences)
        

