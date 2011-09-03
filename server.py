__author__ = "Federico Asara"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Federico Asara", "Juan David Gonzalez Cobas"]
__license__ = "GPL2"
__version__ = "1.0.0"
__maintainer__ = "Federico Asara"
__email__ = "federico.asara@gmail.com"
__status__ = "Production"

import sys
import commands
import PAGE
import PAGE.Agilent33250A, PAGE.Sis33, PAGE.SineWaveform
import Pyro4

agSerial = sys.argv[1]
sis33Device = int(sys.argv[2])
agName, sis33name, sineName = 'agilent', 'sis33', 'sine'

print 'Agilent 33250A, via %s: %s' % (agSerial, agName)
agilent = PAGE.Agilent33250A.target(device = agSerial)
agilent.connect()

print 'SiS 33xx, via %s: %s' % (sis33Device, sis33Name)
sis33 = PAGE.Sis33.target(index = sis33Device)

print 'SineWaveform:', sineName
sine = PAGE.SineWaveform.target()

print 'Daemon'
hn = commands.getoutput('hostname')
daemon=Pyro4.Daemon(host = hn)

print 'Registering'
uris = map(daemon.register, (agilent, sis33, sine))

print 'Nameserver'
ns = Pyro4.locateNS()
map(ns.register, (agName, sis33Name, sineName), uris)

print 'Run'
daemon.requestLoop()

print 'Done'

