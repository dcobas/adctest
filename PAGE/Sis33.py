# 
from ctypes import *
from Configurable import *

lib = CDLL("./libsis33.L865.so")

SIS33_ROUND_NEAREST, SIS33_ROUND_DOWN, SIS33_ROUND_UP = range(3)
SIS33_TRIGGER_START, SIS33_TRIGGER_STOP = range(2)
SIS33_CLKSRC_INTERNAL, SIS33_CLKSRC_EXTERNAL = range(2)

class Sis33Acq(Structure):
    _fields_ = [("data",POINTER(c_uint16)),
                ("nr_samples" , c_uint32),
                ("prevticks", c_uint64),
                ("size", c_uint32)]
    
    @classmethod
    def zalloc(cls, events, ev_length):
        pointer = POINTER(cls)
        lib.sis33_acqs_zalloc.restype = pointer
        acqs = lib.sis33_acqs_zalloc(events, ev_length)
        
        # insert error control
        return acqs
    
    @staticmethod
    def free(item, n_acqs):
        lib.sis33_acqs_free(item, n_acqs)

class Timeval(Structure):
    _fields_ = [("tv_sec", c_uint32),
                ("tv_usec", c_uint32)]
    
    @classmethod
    def create(cls, s, u):
        t = cls()
        t.tv_sec = s;
        t.tv_usec = u;
        
        return t
                
class Sis33Exception(Exception):
    @classmethod
    def spawn(cls, desc):
        return cls(strerror(errno()), desc)
    
def Property(func):
    return property(**func())
    
def logLevel(l):
    return lib.sis33_loglevel(l)
    
def errno():
    return lib.sis33_errno()

def strerror(i):
    return lib.sis33_strerror(i)

def perror(s):
    lib.sis33_perror(s)

"""This class should manage a generic waveform generator"""
class Sis33Device(object):
    _ptr = 0
class SineWaveform(Waveform.Waveform):
    _parameters = {'index':('Device Index', 'Serial device used to communicate with the generator', 2, int)}
    
    def __init__(self, *args, **kwargs):
        self.parameters = dict(self._parameters)
        
        for i in kwargs: 
            if i in self.parameters.keys():
                self.parameters[i][2] = kwargs[i]
        for i in self.parameters.keys():
            self.__setattr__(i, self.parameters[i][2])
        
        self.pointer = lib.sis33_open(self.index)
    
    def __del__(self, index):
        if self._ptr != 0:
            self.close()
    
    def close(self):
        lib.sis33_close(self.pointer)
        self._ptr = 0 # bypass pointer
    
    @Property
    def pointer():
        doc = "Device descriptor"
        
        def fget(self):
            if (self._ptr == 0): raise Sis33Exception('Null pointer')
            return self._ptr
        
        def fset(self, value):
            if (value == 0): raise Sis33Exception('Null pointer')
            self._ptr = value
        
        return locals()
    
    @Property
    def clockSource():
        doc = "Clock source of the device"
        
        def fget(self):
            i = c_int()
            if lib.sis33_get_clock_source(self.pointer, byref(i)):
                raise Sis33Exception.spawn('Get Clock Source')
            return i.value
        
        def fset(self, value):
            value = c_long(value)
            if lib.sis33_set_clock_source(self.pointer, value):
                raise Sis33Exception.spawn('Set Clock Source (%d)' % value)
        
        return locals()
        
    @Property
    def clockFrequency():
        doc = "Clock frequency used"
        
        def fget(self):
            i = c_int()
            if lib.sis33_get_clock_frequency(self.pointer, byref(i)):
                raise Sis33Exception.spawn('Get Clock Frequency')
            return i.value
        
        def fset(self, value):
            value = c_long(value)
            if lib.sis33_set_clock_frequency(self.pointer, value):
                raise Sis33Exception.spawn('Set Clock Frequency (%d)' % value)
        
        return locals()
    
    @Property
    def clockFrequencies():
        doc = "Clock frequencies"
        
        def fget(self):
            i = lib.sis33_get_nr_clock_frequencies(self.pointer)  
            if i == 0: 
                raise Sis33Exception('Clock Frequencies number is 0')
            
            output = (c_uint*i)()
            if lib.sis33_get_available_clock_frequencies(self.pointer, output, c_long(i)):
                raise Sis33Exception.spawn('Get Clock Frequencies')
            return tuple(output)
        
        return locals()
    
    
    def roundClockFrequency(self, clkfreq, roundType):
        """Round a clock frequency to a valid value. """
        return lib.sis33_round_clock_frequency(self.pointer, clkfreq, roundType)
    
    @Property
    def eventLengths():
        doc = "Get the available event lengths. "
        
        def fget(self):
            i = lib.sis33_get_nr_event_lengths(self.pointer) 
            if i == 0: 
                raise Sis33Exception('Event Length number is 0')
            
            output = (c_uint*i)()
            if lib.sis33_get_available_event_lengths(self.pointer, output, c_long(i)):
                raise Sis33Exception.spawn('Get Event Lengths')
            return tuple(output)
        
        return locals()
        
    def roundEventLength(self, evLen, roundType):
        """Round an event length to a valid value. """
        return lib.sis33_round_event_length(self.pointer, evLen, roundType)
    
    def trigger(self, trigger):
        if lib.sis33_trigger(self.pointer, trigger):
            raise Sis33Exception.spawn('Trigger (%d)' % trigger)
    
    @Property
    def enableExternalTrigger():
        doc = "Enable/Disable status of the external trigger"
        
        def fget(self):
            i = c_int()
            if lib.sis33_get_enable_external_trigger(self.pointer, byref(i)):
                raise Sis33Exception.spawn('Get Enble External Trigger')
            return i.value
        
        def fset(self, value):
            value = c_long(value)
            if lib.sis33_set_enable_external_trigger(self.pointer, value):
                raise Sis33Exception.spawn('Set Enable External Trigger (%d)' % value)
        
        return locals()
    
    @Property
    def startAuto():
        doc = "Autostart mode"
        
        def fget(self):
            i = c_int()
            if lib.sis33_get_start_auto(self.pointer, byref(i)):
                raise Sis33Exception.spawn('Get Start Auto')
            return i.value
        
        def fset(self, value):
            value = c_long(value)
            if lib.sis33_set_start_auto(self.pointer, value):
                raise Sis33Exception.spawn('Set Start Auto (%d)' % value)
        
        return locals()
        
        
    @Property
    def startDelay():
        doc = "Start delay"
        
        def fget(self):
            i = c_int()
            if lib.sis33_get_start_delay(self.pointer, byref(i)):
                raise Sis33Exception.spawn('Get Start Delay')
            return i.value
        
        def fset(self, value):
            value = c_long(value)
            if lib.sis33_set_start_delay(self.pointer, value):
                raise Sis33Exception.spawn('Set Start Delay (%d)' % value)
        
        return locals()
    
    @Property
    def stopAuto():
        doc = "Autostop mode"
        
        def fget(self):
            i = c_int()
            if lib.sis33_get_stop_auto(self.pointer, byref(i)):
                raise Sis33Exception.spawn('Get Stop Auto')
            return i.value
        
        def fset(self, value):
            value = c_long(value)
            if lib.sis33_set_stop_auto(self.pointer, value):
                raise Sis33Exception.spawn('Set Stop Auto (%d)' % value)
        
        return locals()
        
    @Property
    def stopDelay():
        doc = "Stop delay"
        
        def fget(self):
            i = c_int()
            if lib.sis33_get_stop_delay(self.pointer, byref(i)):
                raise Sis33Exception.spawn('Get Stop Delay')
            return i.value
        
        def fset(self, value):
            value = c_long(value)
            if lib.sis33_set_stop_delay(self.pointer, value):
                raise Sis33Exception.spawn('Set Stop Delay (%d)' % value)
        
        return locals()
        
    @Property
    def nrChannels():
        doc = "Number of channels on the device."
        
        def fget(self):
            return lib.sis33_get_nr_channels(self.pointer)
        
        return locals()
        
    def channelSetOffset(self, channel, offset):
        i = lib.sis33_channel_set_offset(self.pointer, channel, offset)
        if i != 0: 
            raise Sis33Exception.spawn('Channel Set Offset (%d)' % channel)
    
    def channelGetOffset(self, channel):
        r = c_int()
        i = lib.sis33_channel_get_offset(self.pointer, channel, byref(r))
        if i != 0: 
            raise Sis33Exception.spawn('Channel Get Offset (%d)' % channel)
        
        return r
    
    def channelSetOffsetAll(self, offset):
        i = lib.sis33_channel_set_offset_all(self.pointer, offset)
        if i != 0: 
            raise Sis33Exception.spawn('Channel Set Offset All')
        
    @Property
    def nrSegments():
        doc = "Number of segments on the device."
        
        def fget(self):
            i = c_int()
            if lib.sis33_get_nr_segments(self.pointer, byref(i)):
                raise Sis33Exception.spawn('Get Nr Segments')
            return i.value
        
        def fset(self, value):
            value = c_long(value)
            if lib.sis33_set_nr_segments(self.pointer, value):
                raise Sis33Exception.spawn('Set Nr Segments (%d)' % value)
        
        return locals()
    
    @Property
    def maxNrSegments():
        doc = "Maximum number of segments"
        
        def fget(self):
            i = c_int()
            if lib.sis33_get_max_nr_segments(self.pointer, byref(i)):
                raise Sis33Exception.spawn('Get Maximum Nr Segments')
            return i.value
        
        return locals()
            
    @Property
    def minNrSegments():
        doc = "Minimum number of segments"
        
        def fget(self):
            i = c_int()
            if lib.sis33_get_min_nr_segments(self.pointer, byref(i)):
                raise Sis33Exception.spawn('Get Minimum Nr Segments')
            return i.value
        
        return locals()
            
    @Property
    def maxNrEvents():
        doc = "Maximum number of events"
        
        def fget(self):
            i = c_int()
            if lib.sis33_get_max_nr_events(self.pointer, byref(i)):
                raise Sis33Exception.spawn('Get Maximum Nr Events')
            return i.value
        
        return locals()
        
    @Property
    def nrBits():
        doc = "Number of bits of the device."
        
        def fget(self):
            return lib.sis33_get_nr_bits(self.pointer)
        
        return locals()
    
    @Property
    def eventTimestampingIsSupported():
        doc = "Device implements event hardware timestamping."
        
        def fget(self):
            return lib.sis33_event_timestamping_is_supported(self.pointer)
        
        return locals()
            
    @Property
    def maxEventTimestampingClockTicks():
        doc = "Maximum number of clock ticks of the event timestamping unit. "
        
        def fget(self):
            i = c_int()
            if lib.sis33_get_max_event_timestamping_clock_ticks(self.pointer, byref(i)):
                raise Sis33Exception.spawn('Get Maximum Event Timestamping Clock Ticks')
            return i.value
        
        return locals()
            
    @Property
    def maxEventTimestampingDivider():
        doc = "Maximum event timestamping divider available on a device. "
        
        def fget(self):
            i = c_int()
            if lib.sis33_get_max_event_timestamping_divider(self.pointer, byref(i)):
                raise Sis33Exception.spawn('Get Maximum Event Timestamping Divider')
            return i.value
        
        return locals()
    
    @Property
    def eventTimestampingDivider():
        doc = "Current event timestamping divider on a device. "
        
        def fget(self):
            i = c_int()
            if lib.sis33_get_event_timestamping_divider(self.pointer, byref(i)):
                raise Sis33Exception.spawn('Get Event Timestamping Divider')
            return i.value
        
        def fset(self, value):
            value = c_long(value)
            if lib.sis33_set_event_timestamping_divider(self.pointer, value):
                raise Sis33Exception.spawn('Set Event Timestamping Divider (%d)' % value)
        
        return locals()
    
    def acq(self, segment, nr_events, ev_length):
        ev_length = self.roundEventLength(ev_length, SIS33_ROUND_NEAREST)
        if lib.sis33_acq(self.pointer, segment, nr_events, ev_length):
            raise Sis33Exception.spawn('Acq')
        
    def acqWait(self, segment, nr_events, ev_length):
        ev_length = self.roundEventLength(ev_length, SIS33_ROUND_NEAREST)
        if lib.sis33_acq_wait(self.pointer, segment, nr_events, ev_length):
            raise Sis33Exception.spawn('Acq Wait')
    
    def acqTimeout(self, segment, nr_events, ev_length, timeout):
        ev_length = self.roundEventLength(ev_length, SIS33_ROUND_NEAREST)
        if lib.sis33_acq_timeout(self.pointer, segment, nr_events, ev_length, timeout):
            raise Sis33Exception.spawn('Acq Timeout')
    
    def acqCancel(self):
        if lib.sis33_acq_cancel(self.pointer): 
            raise Sis33Exception.spawn('Acq Cancel')
    
    def fetch(self, segment, channel, acqs, n_acqs, endtime):
        if lib.sis33_fetch(self.pointer, segment, channel, acqs, n_acqs, endtime) < 0:
            raise Sis33Exception.spawn('Fetch')
        
    def fetchWait(self, segment, channel, acqs, n_acqs, endtime):
        if lib.sis33_fetch_wait(self.pointer, segment, channel, acqs, n_acqs, endtime) < 0:
            raise Sis33Exception.spawn('Fetch Wait')
    
    def fetchTimeout(self, segment, channel, acqs, n_acqs, endtime, timeout):
        if lib.sis33_fetch_timeout(self.pointer, segment, channel, acqs, n_acqs, endtime, timeout) < 0:
            raise Sis33Exception.spawn('Fetch Timeout')
    
    def readEvent(self, channel, samples, segment = 0):
        ev_length = self.roundEventLength(samples, SIS33_ROUND_UP)
        
        self.acqWait(segment, 1, ev_length)
        a = Sis33Acq.zalloc(1, ev_length)
        t = Timeval()
        
        self.fetchWait(segment, channel, byref(a[0]), 1, byref(t))
        
        # memory leak!
        return [a[0].data[i] for i in xrange(samples)]
        
        
        
