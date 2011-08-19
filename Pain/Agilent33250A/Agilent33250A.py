import Generic.Generator as gen
import time

from SineWaveform import *
    
def Property(func):
    return property(**func())
    
"""This class should manage the Agilent 33250A waveform generator"""
class Agilent33250A(gen.Generator):
    def __init__(self, device = "/dev/ttyUSB0", bauds = 57600, to = 2, interCharTimeout=1):
        gen.Generator.__init__(self, device = device, bauds = bauds, to = to, interCharTimeout=interCharTimeout)
    
    def command(self, what):
        if type(what) is str:
            what = (what, )
        
        return sum(map(lambda x: self.write("%s\n" % x), what))
    
    @Property
    def output():
        doc = "Output status of the generator"

        def fget(self):
            self.command("OUTP?")
            output = self.read(2)[0]
            
            return output == "1"    
        
        def fset(self, status):
            if type(status) is not bool: 
                return
            
            self.command("OUTP %d" % (1 if status else 0))
        
        return locals()
    
    # legacy
    def lsine(self, frequency, amplitude, dc = 0, freqm = 'HZ', ampm = 'VPP', dcm = 'V'):
        self.command("APPL:SIN %.2f %s, %.2f %s, %.2f %s" % (frequency, freqm, amplitude, ampm, dc, dcm))
    
    def sweep(self, interval, waves, callback = None):
        for w in waves:
            self.command(w.apply())
            time.sleep(interval)
            
            if callback is not None:
                callback(f)
    
    # legacy
    def lsweep(self, interval, frequencies, amplitude, dc = 0, freqm = 'HZ', ampm = 'VPP', dcm = 'V', callback = None):
        
        for f in frequencies:
            self.sine(f, amplitude, dc, freqm, ampm, dcm)
            time.sleep(interval)
            
            if callback is not None:
                callback(f)
        
