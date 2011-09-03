__author__ = "Federico Asara"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Federico Asara", "Juan David Gonzalez Cobas"]
__license__ = "GPL2"
__version__ = "1.0.0"
__maintainer__ = "Federico Asara"
__email__ = "federico.asara@gmail.com"
__status__ = "Production"

# PAGE: Python ADC and GEnerators API

hasSis33 = False

import SineWaveform, TTWaveform
import Agilent33250A
import RemoteObject

try:
    import Sis33
    hasSis33 = True
except:
    print 'Error while loading Sis33 module, skipping it'

waveforms = (RemoteObject, SineWaveform, TTWaveform)
generators = (Agilent33250A, RemoteObject)

if hasSis33:
    adcs = (RemoteObject, Sis33)
else:
    adcs = (RemoteObject, )


