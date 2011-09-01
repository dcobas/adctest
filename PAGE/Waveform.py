from numpy import array
from Item import *

"""This class represent a generic waveform."""
class Waveform(Item):
    def get(self, what):
        """Get an attribute value. Supports Pyro4."""
        return self.__getattribute__(what)
    
    def set(self, what, how):
        """Set an attribute value. Supports Pyro4."""
        self.__setattr__(what, how)
    
    """A waveform must provide this method. 
    Create a numeric array which represents the wave."""
    def generate(self, nbits, frequency, samples, fsr):
        return array([])

    def __init__(self, *args, **kwargs):
        Item.__init__(self, *args, **kwargs)
    
    def getType(self):
        return type(self)
        
