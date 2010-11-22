import ConfigParser
import string

from wx.lib.pubsub import Publisher as pub

from Signal import Signal
from FFTSignal import FFTSignal

class Model:
    SIGNAL_METHODS = ['INL', 'DNL', 'histogram', 'ideal_histogram']
    FFT_METHODS = ['process_gain', 'harmonic_peaks', 'noise_floor', 'SFDR', 'SINAD', 'THD', 'SNR', 'ENOB']
    INTEGER_METHODS = ['noise_floor', 'SFDR', 'SINAD', 'THD', 'SNR', 'ENOB']

    def __init__(self):
        self.signal = None
        self.fft_signal = None
        self.cache_signal()
        self.cache_fft_signal()
        
    def parse_file(self, path):
      
        self.signal = None
        self.fft_signal = None
      
        try:
            config = ConfigParser.RawConfigParser()
            config.read(path)
            
            nbits = config.getint('SIGNAL', 'nbits')
            rate = config.getint('SIGNAL', 'rate')
            dataString = config.get('SIGNAL', 'data').split('\n')
            data = map(string.atoi, dataString)
        
            self.signal = Signal(nbits, rate, data)
            self.fft_signal = self.signal.FFT(1,1) # FIXME change params here
        
        finally:
            self.cache_signal()
            self.cache_fft_signal()
            pub.sendMessage("SIGNAL CHANGED")
    
    
    def cache_signal(self):
    
        self.data = [] if self.signal is None else self.signal.data
        
        for name in Model.SIGNAL_METHODS:
            attribute = [] if self.signal is None else getattr(self.signal, name)()
            setattr( self, name, attribute)
    
    def cache_fft_signal(self):

        self.fft = [] if self.fft_signal is None else self.fft_signal.fft
        
        for name in Model.FFT_METHODS:
            if self.fft_signal is None:
                attribute = 0 if name in Model.INTEGER_METHODS else []
            else:
                attribute = getattr(self.fft_signal, name)()
            setattr( self, name, attribute )


