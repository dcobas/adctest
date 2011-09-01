import Waveform
from Utilities import *
from numpy import *

import Pyro4
import Pyro4.util
import sys
import commands
def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:      
        a, b = b, a % b
    return a

def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)
def frac(x, n):
    AA = 0
    BB = 1
    A  = 1
    B  = 0
    for i in range(n):
        a = int(math.floor(x))
        
        try:
            x = 1/(x-a)
            AA, A = A, AA + a * A
            BB, B = B, BB + a * B
        except:
            return
        
        yield (x, a, A, B,)
                
class TTWaveform(Waveform.Waveform):
    def get(self, what):
        return self.__getattribute__(what)
    
    def set(self, what, how):
        self.__setattr__(what, how)
    
    _parameters = {'frequency':['Frequency (1)', 'Frequency of the first sinewave, in HZ', float(5e6), float],
                   'ratio':['Ratio', 'Ratio between the frequency of the second sinewave and the one', 6./5., float],
                   'amplitude':['Amplitude', 'Amplitude of each sinewave, in Vpp', 1., float],
                   'dc':['DC Compoment', 'DC component of the whole waveform, in Vpp', 0., float]}
                  
    def __init__(self, *args, **kwargs):
        Waveform.Waveform.__init__(self, *args, **kwargs)
    
    def generate(self, sampleRate, samples, nbits, fsr):
        f1, f2 = self.frequency, self.frequency * self.ratio
        A = self.amplitude
        C = self.dc
        
        t = arange(samples, dtype=float)/sampleRate
        s = A*sin(2*pi*f1*t) +A*sin(2*pi*f2*t) +C
        
        lsb = fsr/(2**nbits)
        
        return (s/lsb).astype(int)
        
    def generatePeriod(self, nbits, samples, fsr):
        A = self.amplitude
        C = self.dc
        # r1, r2 = list(frac(self.ratio, 7))[-1][2:]
        
        # print r1, r2
        #print 'Samples:', samples*self.ratio*r2
        
        freq = 2./(self.ratio -1.)
        
        t = arange(samples*freq, dtype=float)/samples
        s = A*sin(2*pi*t) +A*sin(2*pi*self.ratio*t) +C
        
        lsb = fsr/(2**nbits)
        
        return (s/lsb).astype(int), self.frequency/freq
    
    def scale(self, factor):
        """Multiply the frequency by factor"""
        self.frequency *= factor
        
        return self

name = 'Two Tones Waveform'
target = TTWaveform


def launch():
    g = target()
    hn = commands.getoutput('hostname')
    
    daemon = Pyro4.Daemon(host = hn)
    
    myUri = daemon.register(g)
    
    ns=Pyro4.locateNS()
    ns.register("TTSine", myUri)
    daemon.requestLoop()

if __name__ == '__main__':
    launch()
    
