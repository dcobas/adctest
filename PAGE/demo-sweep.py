import sys
from Agilent33250A import *
from SineWaveform import *
from Sis33 import *
import cPickle

g = Agilent33250A(sys.argv[1])
s = Sis33Device(int(sys.argv[2]))

w1 = 5e6
w2 = 6e6
step = 1e6

def generateTwoTone(i):
    return SineWaveform(w1+step*i).generate(30e6, 1e4, 12, 1.) + SineWaveform(w2+step*i).generate(30e6, 1e4, 12, 1.) 

waves = (SineWaveform(w1+step*i, 2, 0) for i in xrange(11))#(generateTwoTone(i) for i in xrange(11))
output = []

def callback(x):
    output.append(s.readEvent(7, 10000))
    
g.output = True
g.sweep(1, waves, callback)
g.output = False

cPickle.dump(output, file('/tmp/output.pickle', 'w'))

s.close()
