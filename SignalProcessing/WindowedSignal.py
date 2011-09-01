from numpy import * 

class WindowedSignal:
    data = array([])
    th = array([])
    nsamples = 0
    dft = array([])
    udft = array([])
    ldft = array([])
    ludft = array([])
    ratio = 0   
    maxPeak = 0
    w0 = 0
    w0index = 0
    rate = 0
    
    def adjust(self, data, fs):
        while data >= fs:
            data -= fs

        if data >= fs/2.:
            data = fs -data;

        return data
    
    def harmonicPeaksGenerator(self, start, end):
        indexes = (self.adjust(x * self.w0index, self.nsamples -1) for x in xrange(start , end))
        return ((i, self.ratio*i, self.dft[i]) for i in indexes)

    def logHarmonicPeaksGenerator(self, start, end):
        indexes = (self.adjust(x * self.w0index, self.nsamples -1) for x in xrange(start , end))
        return ((i, self.ratio*i, self.ldft[i]) for i in indexes)
    
    
    THD = 0
    noiseFloor = 0
    signalPower = 0
    noisePower = 0
    SNR = 0
    
    SINAD = 0
    ENOB = 0
    
    maxPeak = 0
    secondPeak = 0
    SFDR = 0
    
    amplitude = 0
    phase = 0
    
    def items(self):
        output = []
        
        output.append(('Input frequency [W]', '%.5f Hz', self.w0/(2*pi)))
        output.append(('Peak [W]', '%d', self.w0index))
        output.append(('Amplitude [W]', "%f", self.amplitude))
        output.append(('Phase [W]', "%f", self.phase))
        output.append(('DC [W]', "%f", self.C)) 
        
        output.append(('THD', '%.2f dB', self.THD))
        output.append(('Noise floor', "%g dB", self.noiseFloor))
        output.append(('Signal power', "%.f ", self.signalPower))
        output.append(('Noise power', "%.f ", self.noisePower))
        output.append(('SNR', "%.2f dB", self.SNR))
        output.append(('SINAD', "%.2f dB", self.SINAD))
        output.append(('ENOB', "%.2f b", self.ENOB))
        output.append(('SFDR', "%.2f dBc", self.SFDR))
        
        return output
    
    def report(self):
        for i in self.items():
            print "%s: %s" % (i[0], i[1] % i[2])

