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

    - The calls requiring an fft array of numbers use an FFTSignal
      object containing the array of samples, whether it is in dB or
      absolute units, and the original Signal it comes from. The latter
      is mostly ignored, except when some alternative algorithms for
      harmonic peak detection are used behing THD, SINAD, etc. In
      general, an array of numbers can replace this argument type
      everywhere, and the passing of a bare array of reals can
      be easily accomodated in each function taking an FFTSignal.

    - Some function might vary in spec slightly, but changes, if any,
      should be minor.

    - In particular, the functions taking an FFT as input might well
      take a frequency domain signal object FFTSignal as an argument,
      allowing us to compute parameters like distortion or the
      best-fitting sinewave in the input from that. This would be
      transparent to the callers, who can limit themselves to put 
      an array of real values in the fft.fft field of the fft argument
      passed to THD, SINAD, etc. Do not care about this now, though:
      it's easy to change if needed.
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

def histogram(signal):
   """Compute histogram of a sampled signal

   The number of bins in the histogram is implicitly given by the number
   of bits of the samples: 2**signal.nbits bins.

       signal: a Signal object
       returns: an array of 2**signal.nbits numbers (frequencies)
    """

def ideal_histogram(nbits, nsamples):
   """Produce an ideal vector of frequencies (histogram) for the
   nsamples samples of a perfect nbits ADC. Mostly for auxiliary and
   display purposes

        nbits: number of bits of the ideal ADC
        nsamples: number of samples 
       returns: an array of 2**signal.nbits numbers (frequencies)
    """

def DNL(signal):
    """
    Compute differential non-linearity vector for a given time-domain
    signal

    signal: a Signal objectA
    returns: a pair (dnl, total) where
        - dnl is an array of 2**signal.nbits real values and
        - total is a real value (computed from dnl)
    """

def INL(signal):
   """Compute integral non-linearity vector for a given time-domain signal

       signal: a Signal object
       returns: a pair (inl, total) where
        - inl is an array of 2**signal.nbits real values and
        - total is a real (computed from inl)
    """

def FFT(signal, navg, window):
    """
    Compute the amplitudes (in dB) of the FFT of signal, averaging navg
    slices of it and applying window to it

    signal: a Signal object
    navg: number of signal slices to average
    window: a value from a finite list of windows defined in window_types

    returns: an FFTSignal object
    """

def process_gain(nsamples):
    """compute the process gain for a given number of samples

    nsamples: number of samples for computing an FFT
    returns: process gain (a number in dB)
    """

def harmonic_peaks(fft, max_peaks):
    """peak detector

    This auxiliary function computes an array of indices into the fft
    array, pointing to the positions of the first max_peaks most
    significant peaks

    fft: FFTSignal object
    max_peaks: integer (usually in a small range, < 10)

    returns: an array of at most  max_peak indices into 
        the fft.fft array
    """

def noise_floor(fft):
    """noise floor of a frequency-domain signal

    fft: FFTSignal object
    returns: the real value of the fft noise floor
    """

def SFDR(fft):
    """spurious free dynamic range

    fft: FFTSignal object
    returns: a real number
    """

def SINAD(fft):
    """signal to noise and distortion ratio

    fft: FFTSignal object
    returns: a real number
    """

def THD(fft):
    """total harmonic distortion

    fft: FFTSignal object
    returns: a real number
    """

def SNR(fft):
    """signal-to-noise ratio

    fft: FFTSignal object
    returns: a real number
    """

def ENOB(sinad):
    """effective number of bits

    A direct function of the SINAD, relating both scalar values
    """

    return (sinad - 1.76) / 6.02

if __name__ == '__main__':
    pass

