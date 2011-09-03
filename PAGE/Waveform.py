__author__ = "Federico Asara"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Federico Asara", "Juan David Gonzalez Cobas"]
__license__ = "GPL2"
__version__ = "1.0.0"
__maintainer__ = "Federico Asara"
__email__ = "federico.asara@gmail.com"
__status__ = "Production"

from numpy import array
from Item import *

"""This class represent a generic waveform.
You must implement the generate and generatePeriod methods in order to subclass
this. Refer to their docstrings."""
class Waveform(Item):
    def get(self, what):
        """Get an attribute value. Supports Pyro4."""
        return self.__getattribute__(what)
    
    def set(self, what, how):
        """Set an attribute value. Supports Pyro4."""
        self.__setattr__(what, how)
    
    def generate(self, nbits, frequency, samples, fsr):
        """A waveform must provide this method. 
        Create a numeric array which represents the wave."""
        return array([])
    
    def generatePeriod(self, nbits, samples, fsr):
        """A waveform must provide this method. 
        Create a numeric array which represents a period of the wave."""
        return array([])

    def __init__(self, *args, **kwargs):
        Item.__init__(self, *args, **kwargs)
    
    def getType(self):
        return type(self)
        
