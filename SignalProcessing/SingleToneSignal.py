from Signal import *

# For frequency detection and unit-testin
import Sinefit

# We need all the window functions
import WindowFunction
from WindowedSignal import *

# We use numpy almost all the time..
from numpy import *
import cPickle

class SingleToneSignal(Signal):
    """A class that represent a time-domain sampled signal, and also holds many
    WindowedSignal that represent the signal in frequency domain. 
    """

    """maximum tolerable resolution for a histogram"""
    MAXRES = 256

    """This string indicates the selected window""" 
    selectedWindow = "No window"
    
    """This dictionary maps windows function names to WindowedSignal objects"""
    windowed = {}

    def __getitem__(self, what = None):
        """Get a windowed signal item for a particular window function"""
        if what is None:
            what = self.selectedWindow

        # just to be sure
        if what not in WindowFunction.windows.keys():
            what = self.WindowFunction.windows.keys()[0]
        
        return self.windowed[what]

    def __init__(self, nbits = 0, rate = 1, data = []):
        """initialize a signal object

        nbits: bit width of the sample values
        rate: sampling rate of sample production
        data: an array of samples (usually nbits-long words, stored in
              a numpy array)
        """
        super(SingleToneSignal, self).__init__(nbits, rate, data)
        
    
    def items(self):
        output = super(SingleToneSignal, self).items()
        
        output.append(('Max DNL', "%f ", self.maxDNL))
        output.append(('Max INL', "%f ", self.maxINL))
        output.append(('Theoretical SNR', "%.2f dB", self.thSNR))
        output.append(('Process Gain', "%.2f dB", self.processGain))
        
        
        return output    
    
    def precalculateAll(self):
        """Evaluates all the parameters of the signal, and also call the
        precalculate method for each window function we know."""

        # First of all evaluate the histograms
        skip = False
         
        self.realHistogram = self._histogram() if (not skip) and self.nsamples > 0 else array([0])
        self.idealHistogram = self._ideal_histogram() if (not skip) and self.nsamples > 0 else array([0])
        
        skip = False    
        # Then evaluate DNL and INL
        if skip:
            self.DNL, self.maxDNL = [0], 0
            self.INL, self.maxINL = [0], 0
        else:
            self.DNL, self.maxDNL = self._DNL()
            self.INL, self.maxINL = self._INL()
        skip = False
        
        # ..theoretical SNR and process gain
        self.thSNR = 6.02 * self.nbits + 1.76
        self.processGain = 10.0 * log10(self.nbits / 2.0)

        # This dictionary will hold all the WindowedSignal objects
        self.windowed = {}

        for i in WindowFunction.windows.keys():
            self.windowed[i] = self.precalculate(i)
    
    @timeit
    def precalculate(self, windowName):
        """Evaluates all the parameters for a particular window function. 
        windowName: a string containing the name of the window function

        Returns a WindowFunction object, or None if windowName is not valid."""

        output = WindowedSignal()
        
        
        if windowName not in WindowFunction.windows.keys():
            return None 
            
        if self.nsamples == 0: 
            return output
        
         
        output.nsamples = self.nsamples
        output.rate = self.rate
        
        window = WindowFunction.windows[windowName]
        
        print len(self.data), self.nsamples
        output.data = self.data * window[self.nsamples]

        output.dft = fft.fft(output.data)
        output.dft = abs(output.dft)
        lbnd = max(output.dft) * 10e-12
        output.dft = where(output.dft < lbnd, 10e-12, output.dft)     
        output.udft = output.dft[0:len(output.dft):10]
        
        output.ldft = 10*log10(output.dft)
        output.ludft = 10*log10(output.udft)
        print output.ldft[:50]
        output.w0 = w0 = self.w0
        output.w0index = w0index = self.w0index
        amplitude = hypot(self.A, self.B)
        phase = arctan2(self.B, self.A)
        
        A, B, C = self.A, self.B, self.C
        
        # THD
        tenHarmonics = list(output.harmonicPeaksGenerator(2, 30))
        thindex = vstack(map(lambda x: x[0], tenHarmonics))
        thvalues = vstack(map(lambda x: x[2], tenHarmonics))

        tenHarmonicsValues = array(map(lambda x: x[2], tenHarmonics))
        rssHarmonics = norm(tenHarmonicsValues)
        output.THD = -dB(output.dft[w0index]/rssHarmonics)

        # we need the avg of HDs
        avgHarmonics = mean(tenHarmonicsValues)

        # we also need the noise floor: the average of all components below
        # avgHarmonics
        filteredNoise = where(output.dft < avgHarmonics, output.dft, 0)
        output.noiseFloor = dB(mean(filteredNoise))
        
        output.signalPower = (norm(output.dft)**2)/self.nsamples
        # output.signalPower *= output.signalPower / self.nsamples
        
        time = arange(0, self.nsamples, dtype=float)/self.rate
        thSin = C + A * cos(w0*time) + B * sin(w0*time)
        output.th = copy(thSin)
        
        #noise = self.data - thSin
        
        noiseMask = array(ones(len(output.dft)))
        noiseMask[0] = 0 # shouldn't be necessary
        noiseMask[w0index] = 0
        noiseMask[-w0index] = 0
        for i in thindex: noiseMask[int(i)] = 0
        
        noise = where(noiseMask, self.data, 0)
        output.noisePower = (norm(noise)**2) / self.nsamples
        
        # now we can evaluate SNR = max component - noise floor - process gain
        #output.SNR = 10*log10(output.signalPower/output.noisePower)
        num = output.signalPower
        output.SNR = 20*log10(num/output.noisePower)
        
        # now it's time for SINAD
        rmsNoise = sqrt(sum((self.data -thSin)**2)/len(self.data))
        rmsSignal = max(self.data)/sqrt(2)
        output.SINAD = dB(rmsSignal/rmsNoise)
        
        # ENOB
        fsr = 2**(self.nbits -1)
        ra = (max(output.data) - min(output.data))/2.0
        factor = dB(fsr/ra)
        output.ENOB = (output.SINAD - 1.76 + factor) / 6.02

        # SFDR - should I use dB(x) instead of 10log10 ?
        output.maxPeak = 10*log10(output.dft[w0index])
        secondPeak = max(thvalues)
        output.secondPeak = 10*log10(secondPeak)
        
        output.SFDR = 10*log10(output.dft[w0index]/secondPeak)
        
        output.report()
        return output
    
    def histogram_resolution(self):
        """Upper bound to the histogram's length."""
        return min(self.MAXRES , 2**self.nbits)
        
    @timeit
    def _histogram(self):
        """Compute histogram of a sampled signal

        The number of bins in the histogram is histogram_resolution().
        
        Necessary for DNL and INL.

           returns: an array of histogram_resolution() numbers (frequencies)
        """
        bins = self.histogram_resolution()#2**self.nbits
        hist, discard = histogram(self.data, bins)
        
        print "real", len(hist) -2
        return hist[1:-1]

    @timeit
    def _ideal_histogram(self):
        """Produce an ideal vector of frequencies (histogram)    for the
        nsamples samples of a perfect nbits ADC. 
        Necessary for DNL and INL. Needs real histogram

           returns: an array of 2**signal.nbits numbers (frequencies)
        """
        Mt = self.nsamples
        res = self.histogram_resolution()
        hres = res/2.
        hpi = pi/2.
        top = 2**self.nbits
        htop = top/2
        
        
        factor = sin(hpi * Mt / (Mt + self.realHistogram[0] + self.realHistogram[-1]))
        n = arange(0, res)-hres
        n = arcsin((n)/(factor*hres)) - arcsin((n-1)/(factor*hres))
        
        result =  (n * Mt / pi)
        
        print "len(result):", len(result)
        print result
        
        return result[2:]
        
    @timeit
    def _DNL(self):
        """Evaluate DNL, needs real and ideal histrograms."""
        dnl = (self.realHistogram/self.idealHistogram) -1
        return dnl, max(abs(dnl))
    
    @timeit
    def _INL(self):
        """Evaluate INL, needs DNL."""
        inl = cumsum(self.DNL)
        return inl, max(abs(inl))

