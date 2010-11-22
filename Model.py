import ConfigParser
import string

from wx.lib.pubsub import Publisher as pub

from Signal import Signal
from FFTSignal import FFTSignal

class Model:
    FFT_METHODS = ['process_gain', 'harmonic_peaks', 'noise_floor', 'SFDR', 'SINAD', 'THD', 'SNR', 'ENOB']
    INTEGER_METHODS = ['noise_floor', 'SFDR', 'SINAD', 'THD', 'SNR', 'ENOB']

    def __init__(self):
        self.signal = None
        self.fft_signal = None
        self.cache_signal()
        self.cache_fft_signal()
        
    def parse_file(self, path, max_peaks=0, dB = None, time_domain = None):
      
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
            self.fft_signal = self.signal.FFT(dB, time_domain)
        
        finally:
            self.cache_signal()
            self.cache_fft_signal(max_peaks)
            pub.sendMessage("SIGNAL CHANGED")
    
    
    def cache_signal(self):
    
        if self.signal is None:
          self.data = []
          self.INL, self.INL_max = [], 0
          self.DNL, self.DNL_max = [], 0
          self.histogram, self.ideal_histogram = [], []
        else:
          self.data = self.signal.data
          self.INL, self.INL_max = self.signal.INL()
          self.DNL, self.DNL_max = self.signal.DNL()
          self.histogram, self.ideal_histogram = self.signal.histogram(), self.signal.ideal_histogram()
    
    def cache_fft_signal(self, max_peaks=0):

        if self.fft_signal is None:
            self.fft = []
            self.harmonic_peaks = []
            for name in Model.FFT_METHODS: 
                setattr(self, name, 0 if name in Model.INTEGER_METHODS else [])
        else:
            self.fft = self.fft_signal.fft
            self.harmonic_peaks = self.fft_signal.harmonic_peaks(max_peaks)
            for name in Model.FFT_METHODS: 
                setattr( self, name, getattr(self.fft_signal, name)() )


