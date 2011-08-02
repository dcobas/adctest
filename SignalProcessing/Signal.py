# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Federico Asara"
__date__ ="$Jul 11, 2011 2:39:38 PM$"
__doc__= """This module offers the Signal class, which simple store the output
signal of an ADC with some other useful informations. """

from Utilities import *
from numpy import *
import Sinefit 

class Signal(object):
    """A class that represent a time-domain sampled signal.
    """

    def __init__(self, nbits = 0, rate = 1, data = []):
        """initialize a signal object

        nbits: bit width of the sample values
        rate: sampling rate of sample production
        data: an array of samples (usually nbits-long words, stored in
              a numpy array)
        """
        self.nbits = nbits
        self.rate = rate
        self.fulldata = data =  array(data, dtype=float)
        self.fullnsamples = len(data)
        self.data = self.fulldata
        self.nsamples = len(data)
        
        # remove DC component
        if self.fullnsamples > 0:
            self.fulldata -= (max(self.fulldata) +min(self.fulldata))/2.
        
            self.fulldft = abs(fft.fft(self.fulldata))
            
            # useful names
            N = len(data)
            fdft = self.fulldft
            
            first = 1. + argmax(fdft[1:N/2])
            second = first + (argmax(fdft[first-1:first+2:2])*2) -1
            ratio = (fdft[second] / fdft[first])
            
            self.first = first
            self.beta =  N/pi * arctan(sin(pi/N)/(cos(pi/N)+1./ratio))
            self.w0index = first+ self.beta   
            
            freqSample = 2 * pi * self.rate
            w0 = freqSample * float(self.w0index)/self.nsamples
            print "Frequency initial guess ->", w0 
            
            self.w0, self.A, self.B, self.C  = Sinefit.sinefit4(data, 1.0/rate, w0, 1e-7)
            print "Frequency fit ->", self.w0
            
            # limit data
            self.w0index = self.w0 /freqSample * self.nsamples
            self.limit = floor(0.5 + N*int(self.w0index)/self.w0index)
            self.data = data[:self.limit]
            self.nsamples = len(self.data)  
            print "limit is:", self.limit
        
        self.precalculateAll()
    
    def items(self):
        """Create a list of tuples that describes the signal. 
        
        The structure of a tuple is"""
        output = []
        
        output.append(('Number of bits', '%d b', self.nbits))
        output.append(('Sampling rate', '%.2f Hz', self.rate))
        output.append(('Number of samples', "%d samples", self.nsamples))
        output.append(('Peak at', "%f", self.w0index))
        output.append(('Input frequency', "%.6f Hz", self.w0/2/pi))
        output.append(('Beta', "%f", self.beta))
        
        return output    
    
    def precalculateAll(self):
        return 

