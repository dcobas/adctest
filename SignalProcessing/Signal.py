# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Federico Asara"
__date__ ="$Jul 11, 2011 2:39:38 PM$"
__doc__= """This module offers the Signal class, which simply store the output
signal of an ADC, fed with a sinewave, with some other useful informations. 
It is also capable to reverse incoherent sampling, in order to get more accurate
results - if needed. It also removes the DC component.
Other classes may inherit from this one to expand the signal."""

from Utilities import *
from numpy import *
import Sinefit 

class Signal(object):
    """A class that represent a time-domain sampled sinewave. 
    Evaluate a small number of parameters, find the sine frequency and 
    eventually correct sampling incoherency.
    """

    def __init__(self, nbits = 0, rate = 1, data = []):
        """Initialize a signal object

        nbits: bit width of the sample values
        rate: sampling rate of sample production
        data: an array of samples (usually nbits-long words, stored in
              a numpy array)
        """
        
        self.nbits = nbits
        self.rate = rate
        
        # convert data into an array of float, if needed, and store it in 
        # self.fulldata so it`s available to other methods
        self.fulldata = data = array(data, dtype=float)
        self.fullnsamples = len(data)
        self.data = self.fulldata
        self.nsamples = len(data)
        
        if self.fullnsamples > 0:
            # remove DC component
            self.fulldata -= (max(self.fulldata) +min(self.fulldata))/2.
            
            # calculate the |fft|
            self.fulldft = abs(fft.fft(self.fulldata))
            
            # useful names
            N = len(data)
            fdft = self.fulldft
            
            # index of the biggest peak
            first = 1. + argmax(fdft[1:N/2])
            
            # index of the biggest peak nearest to `first`
            # can only be first +-1. 
            second = first + (argmax(fdft[first-1:first+2:2])*2) -1
            ratio = (fdft[second] / fdft[first])
            
            # save first in self
            self.first = first
            
            # self.beta quantifies the sampling incoherency, defining the 
            # fraction of a period sampled in excess.
            self.beta =  N/pi * arctan(sin(pi/N)/(cos(pi/N)+1./ratio))
            
            # the position the peak between first and second
            self.w0index = first+ self.beta   
            
            # sampling frequency
            freqSample = 2 * pi * self.rate
            
            # initial frequency guess
            w0 = freqSample * float(self.w0index)/self.nsamples
            print "Frequency initial guess ->", w0 
            
            # fit the sine 
            self.w0, self.A, self.B, self.C  = Sinefit.sinefit4(data, 1.0/rate, w0, 1e-7)
            print "Frequency fit ->", self.w0
            
            # limit data removing incoherency
            self.w0index = self.w0 /freqSample * self.nsamples
            self.limit = floor(0.5 + N*int(self.w0index)/self.w0index)
            self.data = data[:self.limit]
            self.nsamples = len(self.data)  
            print "limit is:", self.limit
        
        self.precalculateAll()
    
    def items(self):
        """Create a list of tuples that describes the signal. 
        
        A tuple holds three values:
        0. description;
        1. format string for [2], can include units and such;
        2. value to show.
        
        Returns such list of tuples."""
        output = []
        
        output.append(('Number of bits', '%d b', self.nbits))
        output.append(('Sampling rate', '%.2f Hz', self.rate))
        output.append(('Number of samples', "%d samples", self.nsamples))
        output.append(('Peak at', "%f", self.w0index))
        output.append(('Input frequency', "%.6f Hz", self.w0/2/pi))
        output.append(('Beta', "%f", self.beta))
        
        return output    
    
    def precalculateAll(self):
        """Calculate all the parameters. Can (and should!) be overridden."""
        return 

