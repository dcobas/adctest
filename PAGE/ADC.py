from Utilities import *

from Item import *

"""This class manages a generic waveform generator."""
class ADC(Item):
    def get(self, what):
        """Get an attribute value. Supports Pyro4."""
        return self.__getattribute__(what)
    
    def set(self, what, how):
        """Set an attribute value. Supports Pyro4."""
        self.__setattr__(what, how)
        
    def clockFrequency():
        doc = "Clock frequency used by the ADC"
        def fget(self): return 0
        def fset(self, value): return 
        
        return locals()
    
    @Property
    def clockFrequencies():
        doc = "Clock frequencies"
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
    
