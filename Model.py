import ConfigParser
import string

from wx.lib.pubsub import Publisher as pub

from Signal import Signal
from FFTSignal import FFTSignal

class Model:
    """ Holds all the pertinent information regarding the signals.
        It also caches the information so it isn't re-calculated unnecesarily (for example when re-dimensioning windows)
        It communicates with the Controller by emiting messages.
    """

    FFT_METHODS = ['process_gain', 'harmonic_peaks', 'noise_floor', 'SFDR', 'SINAD', 'THD', 'SNR', 'ENOB']
    INTEGER_METHODS = ['noise_floor', 'SFDR', 'SINAD', 'THD', 'SNR', 'ENOB']

    def __init__(self):
        self.signal = None
        self.fft_signal = None
        self.cache_signal()
        self.cache_fft_signal()
        
    def parse_file(self, path, max_peaks=0, dB = None, time_domain = None):
        """ Invoked when a new file needs to be parsed. Will raise an exception if the file contains syntax errors
            Emits the message 'SIGNAL CHANGED' if the file was cached succesfully
        """
      
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
    
    def reprocess_fft(self, window, slices, max_peaks):
        """ Invoked when the FFT controls on tab 3 have been changed. re-calculates fft
            Emits the message 'FFT CHANGED' when done calculating
        """
        
        # TODO: figure out how window, slices and max_peax change the way fft is calculated
        # maybe they define dB and time_domain?
        dB = None
        time_domain = None
        
        self.fft_signal = self.signal.FFT(dB, time_domain)
        self.cache_fft_signal(max_peaks)
        pub.sendMessage("FFT CHANGED")
    
    def cache_signal(self):
        """ Invokes all methods in Signal and caches their result for later use (mainly window resizing)
            Resets values to safe values (0, []) if there was an error while processing the signal definition file
        """
    
        if self.signal is None:
          self.data = []
          self.INL, self.max_INL = [], 0
          self.DNL, self.max_DNL = [], 0
          self.histogram, self.ideal_histogram = [], []
        else:
          self.data = self.signal.data
          self.INL, self.max_INL = self.signal.INL()
          self.DNL, self.max_DNL = self.signal.DNL()
          self.histogram, self.ideal_histogram = self.signal.histogram(), self.signal.ideal_histogram()
    
    def cache_fft_signal(self, max_peaks=0):
        """ Invokes all methods in FFTSignal and caches their result for later use (mainly window resizing)
            Resets values to safe values (0, []) if there was an error while processing the signal definition file
        """

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


