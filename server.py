import sys
import commands
import PAGE
import PAGE.Agilent33250A, PAGE.Sis33, PAGE.SineWaveform
import Pyro4

print 'Agilent'
agilent = PAGE.Agilent33250A.target()
agilent.device = sys.argv[1]
agilent.connect()

print 'Sis33'
sis33 = PAGE.Sis33.target(sys.argv[2])

print 'Sine'
sine = PAGE.SineWaveform.target()

print 'Daemon'
hn = commands.getoutput('hostname')
daemon=Pyro4.Daemon(host = hn)

print 'Registering'
uris = map(daemon.register, (agilent, sis33, sine))

print 'Nameserver'
ns = Pyro4.locateNS()
map(ns.register, ('agilent', 'sis33', 'sine'), uris)

print 'Run'
daemon.requestLoop()

print 'Done'

