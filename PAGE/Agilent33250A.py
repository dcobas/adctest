from Generator import * 
from SineWaveform import SineWaveform
from serial import Serial
from struct import pack
from time import sleep
from numpy import ndarray
#~ import progressbar as pbar

"""This class should manage the Agilent 33250A waveform generator"""
class Agilent33250A(Generator):
    _parameters = {'device':('Serial device', 'Serial device used to communicate with the generator', "/dev/ttyUSB1", 'file'),
                  'bauds':('Bauds', 'Speed of the communication', 9600, int),
                  'to':('Timeout', 'Timeout during read operations',  2, int),
                  'ict':('Inter character space', 'Pause time between each character sent',  1, int)}
                  
    functionList = ('SIN', 'SQU', 'RAMP', 'PULS', 'NOIS', 'DC', 'USER')
    
    def __init__(self, *args, **kwargs):
        self.parameters = dict(self._parameters)
        
        for i in kwargs: 
            if i in self.parameters.keys():
                self.parameters[i][2] = kwargs[i]
        for i in self.parameters.keys():
            self.__setattr__(i, self.parameters[i][2])
        
        
        self.adaptDict = {SineWaveform: self.adaptSine,
                          list: self.adaptData,
                          tuple: self.adaptData,
                          ndarray: self.adaptData,
                          str: self.adaptSavedFunction}
    
    def connect(self):
        self.comm = Serial(port = self.device, baudrate = self.bauds, timeout = self.to, interCharTimeout=self.ict)
        self.comm.read(2)
    
    # utilities
    def adaptSavedFunction(self, wave, *args, **kwargs):
        self.function = ('USER', wave)
        return ""
        
    def adaptSine(self, wave, *args, **kwargs):
        return "APPL:SIN %d HZ, %d VPP, %d V" % (wave.frequency, wave.amplitude, wave.dc)
    
    def adaptData(self, data, *args, **kwargs):
        self.dataUpload(data, *args, **kwargs)
        self.function = ('USER')
        self.function = ('USER', 'VOLATILE')
        return ''
    
    def play(self, wave, *args, **kwargs):
        self.command(self.adapt(wave, *args, **kwargs))
        
    def command(self, what):
        if len(what) == 0: 
            return
        
        if type(what) is str:
            what = (what, )
        
        return sum(map(lambda x: self.comm.write("%s\n" % x), what))
    
    # output
    @Property
    def output():
        doc = "Output status of the generator"

        def fget(self):
            self.command("OUTP?")
            output = self.comm.read(2)[0]
            
            return output == "1"    
        
        def fset(self, status):
            if type(status) is not bool: 
                return
            
            self.command("OUTP %d" % (1 if status else 0))
        
        return locals()
    
    @Property
    def function():
        doc = "Function used by the generator"

        def fget(self):
            self.command("FUNC?")
            output = self.comm.readline()[:-1] # avoid \n
            
            if output == 'USER':
                self.command('FUNC:USER?')
                u = self.comm.readline()[:-1] # avoid \n
                
                return (output, u)
            
            return (output, )
        
        def fset(self, f):
            if type(f) in (tuple, list):
                if len(f) == 2:
                    f, n = f
                else:
                    return
            if type(f) != str:
                return
            f = f.upper()
            
            if ' ' in f:
                f, n = f.split(' ')
            else: 
                n = ''
            
            if f not in self.functionList: 
                return
            
            self.command("FUNC %s %s" % (f, n))
        
        return locals()
    
    @Property
    def frequency():
        doc = "Frequency used by the generator"

        def fget(self):
            self.command("FREQ?")
            output = eval(self.comm.readline()[:-1]) # avoid \n
            
            return output
        
        def fset(self, value):
            f = ' '.join(parse(value, 'HZ'))
            self.command("FREQ %s" % f)
        
        return locals()   
         
    @Property
    def voltage():
        doc = "Output amplitude"

        def fget(self):
            self.command("VOLT?")
            V = eval(self.comm.readline()[:-1]) # avoid \n
            self.command("VOLT? MIN")
            m = eval(self.comm.readline()[:-1])
            self.command("VOLT? MAX")
            M = eval(self.comm.readline()[:-1])
            
            return V, m, M
        
        def fset(self, v):
            if type(v) is str:
                v = v.upper()
                if v[:3] in ['MIN', 'MAX']:
                    self.command('VOLT %s' % v[:3])
                    return
                    
            f = ' '.join(parse(v, 'V'))
            self.command("VOLT %s" % f)
        
        
        return locals()
             
    @Property
    def voltageOffset():
        doc = "Offset of the output signal"

        def fget(self):
            self.command("VOLT:OFFS?")
            V = eval(self.comm.readline()[:-1]) # avoid \n
            self.command("VOLT:OFFS? MIN")
            m = eval(self.comm.readline()[:-1])
            self.command("VOLT:OFFS? MAX")
            M = eval(self.comm.readline()[:-1])
            
            return V, m, M
        
        def fset(self, v):
            if type(v) is str:
                v = v.upper()
                if v[:3] in ['MIN', 'MAX']:
                    self.command('VOLT:OFFS %s' % v[:3])
                    return
                    
            f = ' '.join(parse(v, 'V'))
            self.command("VOLT:OFFS %s" % f)
        
        
        return locals()   
    
    # skipping volt:high volt:low
    @Property
    def voltageRangeAuto():
        doc = "Voltage autoranging for all function. Setter supports also ONCE"

        def fget(self):
            self.command("VOLT:RANG:AUTO?")
            output = self.comm.read(2)[0]
            
            return output == "1"    
        
        def fset(self, status):
            if type(status) is not bool: 
                if status != 'ONCE':
                    return
            else:
                if status: status = 'ON'
                else: status = 'OFF'
            
            self.command("VOLT:RANG:AUTO %s" % status)
        
        return locals()
    
    # skipping volt:high or volt:low
    @Property
    def squareDutyCycle():
        doc = "Duty cycle of a square wave"

        def fget(self):
            self.command("FUNC:SQU:DCYC?")
            V =  eval(self.comm.readline()[:-1])
            self.command("FUNC:SQU:DCYC? MIN")
            m = eval(self.comm.readline()[:-1])
            self.command("FUNC:SQU:DCYC? MAX")
            M = eval(self.comm.readline()[:-1])
            
            return V, m, M
        
        def fset(self, v):
            if type(v) is str:
                v = v.upper()
                if v[:3] in ['MIN', 'MAX']:
                    self.command('FUNC:SQU:DCYC %s' % v[:3])
                    return
                
            self.command("FUNC:SQU:DCYC %f" % v)
        
        
        return locals()   
    
    # data 
    def dataUpload(self, data, ttw = 0.002):
        """Upload a sequence of integers to the volatile memory of the generator.
        TTW is the time to wait between each character of the sequence, which
        is transferred in ASCII"""
        
        #~ i = str(len(data))
        #~ widgets = ['Something: ', pbar.Percentage(), ' ', pbar.Bar(),
           #~ ' ', pbar.ETA(), ' ', pbar.FileTransferSpeed()]
        #~ progress = pbar.ProgressBar(widgets=widgets)

        #~ d = pack('>%sh', data)
        
        #~ command = 'DATA:DAC VOLATILE, #%d%s %s\n' % (len(i), i, d)
        #~ progress = pbar.ProgressBar(widgets=widgets)
        #~ for i in progress(command):
            #~ self.comm.write(i)
            #~ sleep(ttw)
        
        #~ return
        
        command = 'DATA:DAC VOLATILE, %s\n' % ', '.join(str(i) for i in data)
        print "writing"
        self.comm.write(command)
        print "done"
        #for i in progress(command):
        #    self.comm.write(i)
        #    sleep(ttw)
    
    def dataStore(self, destination):
        """Save VOLATILE waveform into 'destination'"""
        if type(destination) is not str: return
        self.command("DATA:COPY %s" % destination)
    
    @Property
    def dataCatalog():
        doc = "List of all available arbitrary waveforms"

        def fget(self):
            self.command('DATA:CAT?')
            return tuple(self.comm.readline()[:-1].replace('"', '').split(','))
        
        return locals()   
        
    
    @Property
    def dataNVCatalog():
        doc = "List of the user defined waveforms store in non-volatile memory"

        def fget(self):
            self.command('DATA:NVOL:CAT?')
            return tuple(self.comm.readline()[:-1].replace('"', '').split(','))
        
        return locals()   
    
        
    @Property
    def dataFree():
        doc = "Free arbitrary waveform slots in non-volatile memory"

        def fget(self):
            self.command('DATA:NVOL:FREE?')
            return int(self.comm.readline()[:-1])
        
        return locals()   
    
    def dataDel(self, what):
        """Delete the waveform 'what'. If 'what' is all, then delete everything.""" 
        if type(what) is not str: return
        
        if what.upper() == 'ALL':
            self.command('DATA:DEL:ALL')
        else:
            self.command('DATA:DEL %s' % what)
        
    
    # commands 
    def sweep(self, interval, waves, callback = None):
        for w in waves:
            self.play(w)
            sleep(interval)
            
            if callback is not None:
                callback(w)


if __name__ == '__main__':
    import sys
    g = Agilent33250A(sys.argv[1])
    g.output = True
    
    waves = [SineWaveform(f = (i, 'KHZ')) for i in xrange(1, 30)]
    def callback(x):
        print x.frequency
    
    g.sweep(0.2, waves, callback)
    
    g.output = False
    
