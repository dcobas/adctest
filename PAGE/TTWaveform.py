import Waveform
from Utilities import *
from numpy import *

import Pyro4
import Pyro4.util
import sys
import commands

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
    
