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
            self.data = self.fulldata
        
        self.precalculateAll()
    
    def report(self):
        for i in self.items():
            print "%s: %s" % (i[0], i[1] % i[2])
    
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
        
        return output    
    
    def precalculateAll(self):
        """Calculate all the parameters. Can (and should!) be overridden."""
        return 

