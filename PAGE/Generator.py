import serial
import time
from Configurable import *
from Utilities import *
    
"""This class should manage a generic waveform generator"""
class Generator(object):
    adaptDict = {}
    config = Configurable()
    
    def adapt(self, wave, *args, **kwargs):
        return self.adaptDict[type(wave)](wave, *args, **kwargs)
