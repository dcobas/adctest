from ConfigParser import RawConfigParser
from numpy import max, abs, sum, sqrt, log10
from time import time                                      

# timeit decoratr
def timeit(method):
    def timed(*args, **kw):
        ts = time()
        result = method(*args, **kw)
        te = time()

        print '%r (%r, %r) %2.3f sec' %  (method.__name__, args, kw, te-ts)
        return result

    return timed
    
# db converter
def dB(x): return 20*log10(x)

def norm(v):
    m = max(abs(v))
    w = v/m
    return m * sqrt(sum(w*w))

# empty generator
def fake(x, y): 
    return (i for i in [])

@timeit
def readFile2(path):
    config = RawConfigParser()
    config.read(path)
    
    nbits = config.getint('SIGNAL', 'nbits')
    rate = config.getint('SIGNAL', 'rate')
    dataString = config.get('SIGNAL', 'data').split('\n')
    
    data = map(int, dataString)
    
    return nbits, rate, data
    
@timeit
def readFile(path):
    config = RawConfigParser()
    config.read(path)
    
    nbits = config.getint('INFO', 'nbits')
    rate = config.getint('INFO', 'rate')
    elements = config.getint('INFO', 'elements')
    
    output = [map(int, config.get('SIGNAL-%d' % i, 'data').split('\n')) for i in xrange(elements)]
    
    return nbits, rate, output
