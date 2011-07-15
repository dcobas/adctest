from numpy import *
import sinefit, ScipySineFit

class WindowedSignal(object):
    pass


class FFTSignal(object):
    """a representation of a frequency-domain signal
    """

    window_function = {
        'No window' : [ones, []],
        'BARTLETT' : [bartlett, []],
        'BLACKMAN' : [blackman, []],
        'HAMMING' : [hamming, []],
        'HANNING' : [hanning, []],
        'KAISER' : [kaiser, [1]],
    }

    WINDOW_TYPES = window_function.keys()
    selectedWindow = 'No window'
    
    data = {}


    def __init__(self, origin, dB = True):
        """initialize an FFTSignal object

        origin: its counterpart in time domain
        dB:  true when in dB units, false if raw amplitude
        """

        # TODO make it possible to create a fd signal without its td counterpart
        self.origin = origin
        self.dB  = dB
        
        self.precalculateAll()
    
    def get(self, what = None):
        if what is None:
            what = self.selectedWindow
        
        # just to be sure
        if what not in self.WINDOW_TYPES:
            what = self.WINDOW_TYPES[0]

        print "Get request: %s --> %s" % (what, self.data[what])
        return self.data[what]
    
    def precalculateAll(self):
        self.data = {}
        
        for i in self.WINDOW_TYPES:
            print "Precalculating fft data for", i  
            self.data[i] = self.precalculate(i)
        
    def precalculate(self, windowName):
        # windows are ok right now
        # wrong values: THD
        # wrong formatting output: THD
        output = WindowedSignal()
        window = self.window_function[windowName][0]
        
        # DFT of the signal scaled by window
        windowParams = [self.origin.nsamples] + self.window_function[windowName][1]
        
        output.dft = 10*log10(abs(fft.rfft(self.origin.data * window(*windowParams))))
        # m = len(output.dft)
        
        # sinusoid frequency detection
        # we need a first approximation, let's search for the maximum in 
        # abs(output.dft) -- we need its index
        
        print "Calculating frequency: rate = %d, nsamples = %d" % (self.origin.rate, self.origin.nsamples)
        w0index = argmax(output.dft)
        w0 = w0index * (2 * pi * self.origin.rate) / self.origin.nsamples
        freqSample = 2*pi*(self.origin.rate)**-1

        
        args = (array(self.origin.data), freqSample, w0)
        print "index:", w0index, "array: %s\nFs [Hz]: %f\tw0 [rad/sec]:%f" % args
        output.w0 = ScipySineFit.sinefit4(*args)#array(self.origin.data), freqSample, w0)
        print "Frequency detected: %.6f" % output.w0

        # let's go through harmonic peaks. we will produce a generator
        # this way 
        def adjust(data, fs):
            while abs(data -fs) > (fs/2.):
                data += fs if data < fs else -fs
            return data
        
        def getGenerator(start, end):
            return (adjust(x, freqSample) for x in xrange(start, end))
        
        output.harmonicPeaksGenerator = getGenerator
        
        # THD seems easy..
        tenHarmonicsIndexes = getGenerator(0, 10)
        tenHarmonics = array([output.dft[i] for i in tenHarmonicsIndexes])
        output.THD = 10.0 * log10(sum(10 ** (tenHarmonics/2.0)))
        
        # we need the avg of HDs
        avgHarmonics = mean(tenHarmonics)
        
        # we also need the noise floor: the average of all components below 
        # avgHarmonics
        filteredNoise = where(output.dft >= avgHarmonics, output.dft, 0)
        output.noiseFloor = mean(filteredNoise)    
        
        # now we can evaluate SNR = max component - noise floor - process gain
        output.SNR = output.dft[w0index] -output.noiseFloor -self.origin.cachedProcessGain 
        
        # now it's time for SINAD
        output.SINAD = -10 * log10(10**(-output.SNR/10) + 10**(-abs(output.THD)/10))
        
        # missing ENOB, how can I get FSR & RSR?
        output.ENOB = 0
        
        # missing SFDR
        output.SFDR = 0

        return output
    
    
