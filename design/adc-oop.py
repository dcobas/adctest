#!   /usr/bin/env   python
#    coding: utf8

__doc__ = """
    Interface for the adc ADC characterization module

    This is a preliminary spec of the interface to be expected from the
    GUI of the ADC characterization environment

    Some notes:

    - A Signal object packs all the info we may need from a signal, to
      wit, 
      * its raw data vector and, implicitly, 
      * raw data vector length == number of samples, 
      * number of bits (size of the integer samples in raw data vector)
      * sampling rate
"""

window_types = [
    'RECTANGULAR', 
    'HANN', 
    'HAMMING', 
    'TUKEY', 
    'COSINE', 
    'LANCZOS', 
    'BARTLETT_HANN', 
]

class Signal(object):
    """a representation of a time-domain sampled signal
    """

    def __init__(self, data, nbits, rate):
        """initialize a signal object

        data: an array of samples (usually nbits-long words, stored in
            a numpy array)
        nbits: bit width of the sample values
        rate: sampling rate of sample production
        """

        self.data = data
        self.nbits = nbits
        self.rate = rate

    def histogram(self):
       """Compute histogram of a sampled signal

       The number of bins in the histogram is implicitly given by the number
       of bits of the samples: 2**signal.nbits bins.

           returns: an array of 2**signal.nbits numbers (frequencies)
       """

    def ideal_histogram(self):
       """Produce an ideal vector of frequencies (histogram) for the
       nsamples samples of a perfect nbits ADC. Mostly for auxiliary and
       display purposes

           returns: an array of 2**signal.nbits numbers (frequencies)
       """

    def DNL(self):
        """Compute differential non-linearity vector for a given time-domain
        signal

        returns: a pair (dnl, total) where
            - dnl is an array of 2**signal.nbits real values and
            - total is a real value (computed from dnl)
        """

    def INL(self):
       """Compute integral non-linearity vector for a given time-domain signal

           returns: a pair (inl, total) where
            - inl is an array of 2**signal.nbits real values and
            - total is a real (computed from inl)
        """

    def FFT(self, navg, window):
        """Compute the amplitudes (in dB) of the FFT of signal, averaging navg
        slices of it and applying window to it

        navg: number of signal slices to average
        window: a value from a finite list of windows defined in window_types

        returns: an FFTSignal object
        """

class FFTSignal(object):
    """a representation of a frequency-domain signal
    """

    def __init__(self, fft, dB = None, time_domain = None):
        """initialize an FFTSignal object

        fft: array of numeric values of the fft
        dB:  true when in dB units, false if raw amplitude
        time_domain: the original time-domain signal if available, None
            otherwise

            self.fft = fft
            self.dB  = dB
            self.time_domain = time_domain
        """

    def process_gain(self):
        """compute the process gain for a given number of samples

        returns: process gain (a number in dB)
        """

    def harmonic_peaks(self, max_peaks):
        """peak detector

        This auxiliary function computes an array of indices into the fft
        array, pointing to the positions of the first max_peaks most
        significant peaks

        max_peaks: integer (usually in a small range, < 10)

        returns: an array of at most  max_peak indices into 
            the fft.fft array
        """

    def noise_floor(self):
        """noise floor of a frequency-domain signal

        returns: the real value of the fft noise floor
        """

    def SFDR(self):
        """spurious free dynamic range

        returns: a real number
        """

    def SINAD(self):
        """signal to noise and distortion ratio

        returns: a real number
        """

    def THD(self):
        """total harmonic distortion

        fft: FFTSignal object
        returns: a real number
        """

    def SNR(self):
        """signal-to-noise ratio

        returns: a real number
        """

    def ENOB(self):
        """effective number of bits

        A direct function of the SINAD, relating both scalar values
        """

if __name__ == '__main__':
    pass
