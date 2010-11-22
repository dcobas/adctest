import ConfigParser
import string

from wx.lib.pubsub import Publisher as pub

from Signal import Signal
from FFTSignal import FFTSignal

class Model:
    def __init__(self):
        self.signal = None
        self.fftSignal = None
        
    def ParseFile(self, path):
      
        self.signal = None
        self.fftSignal = None
      
        config = ConfigParser.RawConfigParser()
        config.read(path)
        
        nbits = config.getint('SIGNAL', 'nbits')
        rate = config.getint('SIGNAL', 'rate')
        dataString = config.get('SIGNAL', 'data').split('\n')
        data = map(string.atoi, dataString)
        
        self.signal = Signal(nbits, rate, data)
        self.fftSignal = self.signal.FFT(1,1) # FIXME change params here
        
        pub.sendMessage("SIGNAL CHANGED")
     
    def GetData(self):
        if self.signal is None:
            return []
        else:
            return self.signal.data
     
     

