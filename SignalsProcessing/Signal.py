# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Federico Asara"
__date__ ="$Jul 11, 2011 2:39:38 PM$"
__doc__= """This module offers the Signal class, which calculate a variety of
parameters of an ADC output signal. """

# We use its array for data representation, also we use its FFT implementation
from numpy import *
from matplotlib import pyplot

# For frequency detection and unit-testin
import sinefit

# We need all the window functions
import WindowFunction

def dB(x): return 20*log10(x)

def norm(v):
    m = max(abs(v))
    w = v/m
    return m * sqrt(sum(w*w))

class WindowedSignal:
    """Container object that will hold information about a DFT of a signal
    multiplied by some window function"""
    pass

class Signal(object):
    """A class that represent a time-domain sampled signal, and also holds many
    WindowedSignal that represent the signal in frequency domain. 
    """

    # maximum tolerable resolution for a histogram
    MAXRES = 512

    # indicates the selected window
    selectedWindow = "No window"

    windowed = {}

    def __getitem__(self, what):
        """Get a windowed signal item for a particular window function"""
        if what is None:
            what = self.selectedWindow

        # just to be sure
        if what not in WindowFunction.windows.keys():
            what = self.WindowFunction.windows.keys()[0]
        
        return self.windowed[what]

    def __init__(self, nbits, rate, data):
        """initialize a signal object

        nbits: bit width of the sample values
        rate: sampling rate of sample production
        data: an array of samples (usually nbits-long words, stored in
              a numpy array)
        """
        self.nbits = nbits
        self.rate = rate
        self.data = array(data, dtype=float) # just to be sure
        print mean(self.data)
        self.data -= (max(self.data) +min(self.data))/2.
        self.nsamples = len(data)


        print self.data
        
        self.precalculateAll()
        
    def precalculateAll(self):
        """Evaluates all the parameters of the signal, and also call the
        precalculate method for each window function we know."""

        # First of all evaluate the histograms
        self.idealHistogram = [0]#self._ideal_histogram()
        self.realHistogram = [0]#self._histogram()

        # Then evaluate DNL and INL
        self.DNL, self.maxDNL = [0], 0#self._DNL()
        self.INL, self.maxINL = [0], 0#self._INL()

        # ..theoretical SNR and process gain
        self.thSNR = 6.02 * self.nbits + 1.76
        self.processGain = 10.0 * log10(self.nbits / 2.0)

        # This dictionary will hold all the WindowedSignal objects
        self.windowed = {}

        for i in WindowFunction.windows.keys():
            print
            print "Precalculating fft data for", i
            print
            self.windowed[i] = self.precalculate(i)

    def precalculate(self, windowName):
        """Evaluates all the parameters for a particular window function.

        windowName: a string containing the name of the window function

        Returns a WindowFunction object, or None if windowName is not valid."""
        # windows are ok right now
        # wrong values: THD
        # wrong formatting output: THD

        if windowName not in WindowFunction.windows.keys():
            return None # and maybe launch an exception

        output = WindowedSignal()
        window = WindowFunction.windows[windowName]

        print "Filtering data"
        output.data = self.data * window[self.nsamples]

        print "FFT-ing data"
        output.dft = abs(fft.rfft(output.data))
        print output.dft
        output.udft = output.dft[0:len(output.dft):10]

        print "log10-ing data"
        output.ldft = 10*log10(output.dft)
        output.ludft = 10*log10(output.udft)

        print "Guessing w0"
        # sinusoid frequency detection
        
        w0index = argmax(output.dft)
        freqSample = 2 * pi * self.rate
        w0 = freqSample * float(w0index)/self.nsamples
        ratio = w0 / w0index
        print "Samples/period:",self.nsamples / w0index
        print freqSample, w0
        output.w0, A, B, C  = sinefit.sinefit4(self.data, 1.0/self.rate, w0)
        print A, B, C, output.w0
        amplitude = hypot(A, B)
        phase = arctan2(B, A)
        # let's go through harmonic peaks. we will produce a generator
        # this way
        def adjust(data, fs):
            while data >= fs:
                data -= fs

            if data >= fs/2.:
                data = fs -data;

            return data

        def getGenerator(start, end):
            indexes = (adjust(x * w0index, self.nsamples -1) for x in xrange(start , end))
            return ((i, ratio*i, output.dft[i]) for i in indexes)

        def getLogGenerator(start, end):
            indexes = (adjust(x * w0index, self.nsamples -1) for x in xrange(start , end))
            return ((i, ratio*i, 10*log10(output.dft[i])) for i in indexes)

        output.harmonicPeaksGenerator = getGenerator
        output.logHarmonicPeaksGenerator = getLogGenerator
        
        # THD seems easy..
        tenHarmonics = list(getGenerator(2, 10))
        thindex = vstack(map(lambda x: x[0], tenHarmonics))
        thvalues = vstack(map(lambda x: x[2], tenHarmonics))

        tenHarmonicsValues = array(map(lambda x: x[2], tenHarmonics))
        rssHarmonics = norm(tenHarmonicsValues)
        output.THD = dB(output.dft[w0index]/rssHarmonics)
        print rssHarmonics, output.dft[w0index-3:w0index+3]

        # we need the avg of HDs
        avgHarmonics = mean(tenHarmonicsValues)

        # we also need the noise floor: the average of all components below
        # avgHarmonics
        filteredNoise = where(output.dft < avgHarmonics, output.dft, 0)
        output.noiseFloor = dB(mean(filteredNoise))

        output.signalPower = norm(output.dft)
        output.signalPower *= output.signalPower / self.nsamples
        #sum(where(output.dft < output.noiseFloor, output.dft, 0)**2)/(self.nsamples**2 )

        # thSin = C + Sinefit.makesine(self.nsamples, w0index, self.nbits, 1  )
        time = arange(0, self.nsamples, dtype=float)/self.rate
        print A, B, C, phase, amplitude
        # thSin = C + amplitude * sin(w0index*2*pi*time + phase)
        thSin = C + A * cos(w0*time) + B * sin(w0*time)
        tmp = file("/tmp/something", 'w')
        tmp.writelines("%f\n" % i for i in thSin)
        tmp.close()

        noise = self.data - thSin
        print 'data = ', self.data
        print 'thSin = ', thSin
        print 'noise = ', noise, 'max noise = ', max(abs(noise))

        output.noisePower = norm(noise)
        output.noisePower *= output.noisePower

        # now we can evaluate SNR = max component - noise floor - process gain
        # output.SNR = output.dft[w0index] -output.noiseFloor -self.processGain
        output.SNR = dB(output.signalPower/output.noisePower)

        # now it's time for SINAD
        clean = array(output.dft)
        clean[0] = 0
        clean[w0index] = 0
        output.SINAD = dB(output.dft[w0index]/norm(clean))

        # ENOB
        fsr = 2**(self.nbits -1)
        ra = (max(output.data) - min(output.data))/2.0
        factor = dB(fsr/ra)
        output.ENOB = (output.SINAD - 1.76 + factor) / 6.02

        # SFDR - should I use dB(x) instead of 10log10 ?
        output.maxPeak = 10*log10(output.dft[w0index])
        secondPeak = max(thvalues)
        output.secondPeak = 10*log10(secondPeak)
        
        output.SFDR = 10*log10(output.dft[w0index] - secondPeak)[0] #10*log10
        
        print "Sampling frequency       = %.2f Hz" % self.rate
        print "Input frequency detected = %.2f Hz" % (output.w0/(2*pi))
        print "THD                      = %g dB" % output.THD
        print "Noise floor              = %.6f dB" % output.noiseFloor
        print "Signal power             = %.f " % output.signalPower
        print "Noise power              = %.f " % output.noisePower
        print "SNR                      = %.2f dB" % output.SNR
        print "SINAD                    = %.2f dB" % output.SINAD
        print "ENOB                     = %.f b" % output.ENOB
        print "SFDR                     = %.2f dBc" % output.SFDR
        
        return output
    
    def histogram_resolution(self):
        bins = 2**self.nbits
        return 512 if bins > self.MAXRES else bins

    def _histogram(self):
        """Compute histogram of a sampled signal

        The number of bins in the histogram is implicitly given by the number
        of bits of the samples: 2**signal.nbits bins.

           returns: an array of 2**signal.nbits numbers (frequencies)
        """
        bins = 2**self.nbits
        hist, discard = histogram(self.data, bins)
        
        return hist[1:-1]

    def _ideal_histogram(self):
        """Produce an ideal vector of frequencies (histogram) for the
        nsamples samples of a perfect nbits ADC. Mostly for auxiliary and
        display purposes

           returns: an array of 2**signal.nbits numbers (frequencies)
        """
        Mt = self.nsamples  
        A = sin(pi/2 * Mt / (Mt + self.data[0] + self.data[-1]))
        range = 2**self.nbits
        midrange = range/2
        n = arange(1, range-1)
        p = arcsin(A/midrange * (n - midrange))
        q = arcsin(A/midrange * (n - 1 - midrange))
        p = (p - q) / pi

        return Mt * p
        
    def _DNL(self):
        dnl = (self.realHistogram/self.idealHistogram) -1
        return dnl, max(abs(dnl))

    def _INL(self):
        inl = cumsum(self.DNL)
        return inl, max(abs(inl))


