import serial
import time
    
def Property(func):
    return property(**func())
    
"""This class should manage the Agilent 33250A waveform generator"""
class SerialInterface(serial.Serial):
    def __init__(self, device = "/dev/ttyUSB0", bauds = 57600, to = 2, interCharTimeout=1):
        serial.Serial.__init__(self, device, bauds, timeout = to, interCharTimeout = 1)
    
    def command(self, what):
        return self.write("%s\n" % what)
    
    @Property
    def output():
        doc = "The person's name"

        def fget(self):
            self.command("OUTP?")
            output = self.read(2)[0]
            
            return output == "1"    
        
        def fset(self, status):
            if type(status) is not bool: 
                return
            
            self.command("OUTP %d" % (1 if status else 0))
        
        return locals()
    
    def sine(self, frequency, amplitude, dc = 0, freqm = 'HZ', ampm = 'VPP', dcm = 'V'):
        self.command("APPL:SIN %.2f %s, %.2f %s, %.2f %s" % (frequency, freqm, amplitude, ampm, dc, dcm))
     
    def sweep(self, interval, frequencies, amplitude, dc = 0, freqm = 'HZ', ampm = 'VPP', dcm = 'V', callback = None):
        
        for f in frequencies:
            self.sine(f, amplitude, dc, freqm, ampm, dcm)
            time.sleep(interval)
            
            if callback is not None:
                callback(f)
        
