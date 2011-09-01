__author__="Federico"
__date__ ="$Aug 17, 2011 4:43:08 PM$"

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


