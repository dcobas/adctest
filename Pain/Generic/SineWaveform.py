import Waveform

def Property(func):
    return property(**func())

def parse(value, s):
    if type(value) is str:
        value = value.split(" ")
        value[0] = float(value[0])
        value = tuple(value)
    
    if type(value) is tuple and len(value) == 1:
        value = value[0]
        
    if type(value) is not tuple: 
        return (value, s)
    else: return value

class SineWaveform(Waveform.Waveform):
    def apply(self):
        return ""
    
    _freq = (1, 'KHZ');
    _amp = (0.1, 'VPP');
    _dc = (0, 'V');
    
    @Property
    def frequency():
        doc = "Frequency of the sinewave"
        
        def fget(self):
            return self._freq
        
        def fset(self, value):
            self._freq = parse(value, 'HZ')
        
        def fdel(self):
            del self._freq
        
        return locals()
    
    @Property
    def amplitude():
        doc = "Amplitude of the sinewave"
        
        def fget(self):
            return self._amp
        
        def fset(self, value):
            self._amp = parse(value, 'HZ')
        
        def fdel(self):
            del self._amp
        
        return locals()
    
    @Property
    def dc():
        doc = "Amplitude of the sinewave"
        
        def fget(self):
            return self._dc
        
        def fset(self, value):
            self._dc = parse(value, 'HZ')
        
        def fdel(self):
            del self._dc
        
        return locals()
