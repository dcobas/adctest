import Waveform
from Utilities import *
from numpy import *

class SineWaveform(Waveform.Waveform):
    _parameters = {'frequency':('Frequency', 'Frequency of the sinewave, in HZ', 1000, float),
                  'amplitude':('Amplitude', 'Amplitude of the sinewave, in Vpp', 1, float),
                  'dc':('DC Compoment', 'DC component of the sinewave, in Vpp', 1, float)}
                  
    def __init__(self, *args, **kwargs):
        self.parameters = dict(self._parameters)
        
        for i in kwargs: 
            if i in self.parameters.keys():
                self.parameters[i][2] = kwargs[i]
        for i in self.parameters.keys():
            self.__setattr__(i, self.parameters[i][2])
    
    def generate(self, sampleRate, samples, nbits, fsr):
        f = self.frequency
        A = self.amplitude
        C = self.dc
        
        t = arange(samples, dtype=float)/sampleRate
        s = A*sin(2*pi*f*t) +C
        
        lsb = fsr/(2**nbits)
        
        return (s/lsb).astype(int)
