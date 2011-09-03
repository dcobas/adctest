__author__ = "Federico Asara"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Federico Asara", "Juan David Gonzalez Cobas"]
__license__ = "GPL2"
__version__ = "1.0.0"
__maintainer__ = "Federico Asara"
__email__ = "federico.asara@gmail.com"
__status__ = "Production"

__doc__ = """
This simple demo executes a frequency sweep using a remote generator and a 
remote ADC."""

import PAGE
import PAGE.SineWaveform as sw
import PAGE.RemoteObject as ro

# Just for fun 
#
# example: create a sinewaveform, frequency 5000 Hz, amplitude 2 V
# using kwargs or attributes is actually the same. 
# s = sw.SineWaveform(amplitude = 2)
# s.frequency = 50000

# create a generator, using a remote object 
g = ro.RemoteObject('agilent')
g.connect()  # connect is a generator function
g.set('output', True) 

# if Generator was a local object, you could as well use
# g.output = True

# create an ADC, using a remote object 
a = ro.RemoteObject('sis33')

output = []
def callback(wave):
    # wave is being played by the generator
    # 10000 samples
    output.append(a.readEvent(10000))

# let's create a few waves, this time for real!
waves = (sw.SineWaveform(frequency = 1000*(i**2)) for i in xrange(1, 11))

# sweep each 0.5 seconds in waves, calling callback each time you change 
g.sweep(0.5, waves, callback)

for i in output: 
    print output

