__author__ = "Federico Asara"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Federico Asara", "Juan David Gonzalez Cobas"]
__license__ = "GPL2"
__version__ = "1.0.0"
__maintainer__ = "Federico Asara"
__email__ = "federico.asara@gmail.com"
__status__ = "Production"

from Utilities import *
from Item import *

"""This class manages a generic ADC.
Please implement all its methods when you are subclassing it. In particular,
you must provide a way to select the sampling frequency among a list of them, a 
property with the number of bits and a function that reads data from the ADC."""
class ADC(Item):
    def get(self, what):
        """Get an attribute value. Supports Pyro4."""
        return self.__getattribute__(what)
    
    def set(self, what, how):
        """Set an attribute value. Supports Pyro4."""
        self.__setattr__(what, how)
        
    def clockFrequency():
        doc = "Clock frequency used by the ADC."
        def fget(self): return 0
        def fset(self, value): return 
        
        return locals()
    
    @Property
    def clockFrequencies():
        doc = "Clock frequencies, in a tuple."
        def fget(self): return tuple()
        def fset(self, value): return 
        
        return locals()
    
    @Property
    def nrBits():
        doc = "Number of bits of the device."
        def fget(self): return 0
        
        return locals()
    
    def readEvent(self, samples):
        '''Read an event of size 'samples' from the ADC. Uses self.segment
        and self.channel to select the missing parameters.'''
        return []
     
    def __init__(self, *args, **kwargs):
        Item.__init__(self, *args, **kwargs)
    
