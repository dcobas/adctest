from Utilities import *

from Item import *

"""This class manages a generic waveform generator."""
class Generator(Item):
    def get(self, what):
        """Get an attribute value. Supports Pyro4."""
        return self.__getattribute__(what)
    
    def set(self, what, how):
        """Set an attribute value. Supports Pyro4."""
        self.__setattr__(what, how)
        
    # this dictionary is used to map data types into function which can
    # translate such type of data into something the generator can understand.
    adaptDict = {}
    
    def adaptKeys(self):
        """Returns all data types supported."""
        return self.adaptDict.keys()
    
    def adapt(self, wave, *args, **kwargs):
        """Adapt a wave to the generator"""
        return self.adaptDict[type(wave)](wave, *args, **kwargs)
    
    def __init__(self, *args, **kwargs):
        Item.__init__(self, *args, **kwargs)
    
