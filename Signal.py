from FFTSignal import FFTSignal 
from numpy import *

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

class Signal(object):
    """a representation of a time-domain sampled signal
    """

    MAXRES = 512        # maximum tolerable resolution for a histogram

    def __init__(self, nbits, rate, data):
        """initialize a signal object

        nbits: bit width of the sample values
        rate: sampling rate of sample production
        data: an array of samples (usually nbits-long words, stored in
              a numpy array)
        """

        self.nbits = nbits
        self.rate = rate
        self.data = data
        self.nsamples = len(data)

    def histogram_resolution(self):
        bins = 2**self.nbits
        return 512 if bins > self.MAXRES else bins

    def histogram(self):
        """Compute histogram of a sampled signal

        The number of bins in the histogram is implicitly given by the number
        of bits of the samples: 2**signal.nbits bins.

           returns: an array of 2**signal.nbits numbers (frequencies)
        """
        # bins = self.histogram_resolution()
        # hist, bins = histogram(array(self.data), bins)
        bins = 2**self.nbits
        hist, discard = histogram(array(self.data), bins)
        return hist[1:-1]

    def _ideal_histogram(self):
        """Produce an ideal vector of frequencies (histogram) for the
        nsamples samples of a perfect nbits ADC. Mostly for auxiliary and
        display purposes

           returns: an array of 2**signal.nbits numbers (frequencies)
        """
        Mt = len(self.data)
        A = sin(pi/2 * Mt / (Mt + self.data[0] + self.data[-1]))
        range = 2**self.nbits
        midrange = range/2
        n = arange(1, range-1)
        p = arcsin(A/midrange * (n - midrange))
        q = arcsin(A/midrange * (n - 1 - midrange))
        p = (p - q) / pi
        return Mt * p

    def ideal_histogram(self):
        """Produce an ideal vector of frequencies (histogram) for the
        nsamples samples of a perfect nbits ADC. Mostly for auxiliary and
        display purposes

           returns: an array of 2**signal.nbits numbers (frequencies)
        """
        Mt = len(self.data)
        A = sin(pi/2 * Mt / (Mt + self.data[0] + self.data[-1]))
        range = 2**self.nbits
        midrange = range/2
        n = arange(1, range-1)
        p = arcsin(A/midrange * (n - midrange))
        q = arcsin(A/midrange * (n - 1 - midrange))
        p = (p - q) / pi
        # t = linspace(-1, 1, 2**self.nbits)[1:-1]
        # print sum(1/pi * 1/sqrt(1-t**2) / 2**self.nbits * Mt)
        # return 1/pi * 1/sqrt(1-t**2) / 2**self.nbits * Mt
        return Mt * p

    def DNL(self):
        """Compute differential non-linearity vector for a given time-domain
        signal

        returns: a pair (dnl, total) where
            - dnl is an array of 2**signal.nbits real values and
            - total is a real value (computed from dnl)
        """
        ideal = self.ideal_histogram()
        real  = self.histogram()
        print size(ideal), size(real)
        dnl = real/ideal - 1
        return dnl, max(abs(dnl))
        

    def INL(self):
        """Compute integral non-linearity vector for a given time-domain signal

           returns: a pair (inl, total) where
            - inl is an array of 2**signal.nbits real values and
            - total is a real (computed from inl)
        """
        dnl, discard = self.DNL()
        inl = cumsum(dnl)
        return inl, max(abs(inl))

    def FFT(self, navg=1, window='No window'):
        """Compute the amplitudes (in dB) of the FFT of signal, averaging navg
        slices of it and applying window to it

        navg: number of signal slices to average
        window: a value from a finite list of windows defined in window_types

        returns: an FFTSignal object
        """
        print 'using window ', window
        win = FFTSignal.window_function[window](self.nsamples)
        dft = 10*log10(abs(fft.rfft(self.data * win)))
        return FFTSignal(dft, dB=True, time_domain=self.data)

def makesine(samples, periods, bits, amplitude=1, noise=0):

    t = arange(samples)/float(samples)
    sine = amplitude * sin(2*pi*periods*t)
    sine += noise * ((t % 0.02) / 0.02 - 0.01)
    sine = (sine * 2**bits + 0.5).astype(int)
    place(sine, sine >=  2**bits, 2**bits)
    place(sine, sine <= -2**bits, -2**bits)
    out = file('data', 'w')
    for datum in sine:
        out.write(str(datum) + '\n')
    out.close()
    return sine
    

if __name__ == '__main__':
    from matplotlib import pyplot

    bits = 12
    makesine(20000, 20, bits, 1.1)
    f = [ int(sample) for sample in file('data')]
    s = Signal(nbits = bits, rate = 123, data = f)
    ideal = s.ideal_histogram()
    real  = s.histogram()
    # pyplot.plot(ideal)
    # pyplot.plot(real)
    dnl = real/ideal-1
    pyplot.plot(dnl)
    pyplot.plot(cumsum(dnl))
    # pyplot.plot(f)
    pyplot.show()
    print dnl[0:5], dnl[-5:]

