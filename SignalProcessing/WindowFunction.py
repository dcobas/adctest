__author__ = "Federico Asara"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Federico Asara", "Juan David Gonzalez Cobas"]
__license__ = "GPL2"
__version__ = "1.0.0"
__maintainer__ = "Federico Asara"
__email__ = "federico.asara@gmail.com"
__status__ = "Production"

from numpy import ones, bartlett, blackman, hamming, hanning, kaiser

class WindowFunction(object):
    def __init__(self, name, function, parameters):
        self.name = name
        self.function = function
        self.parameters = parameters

    def get(self, key, *parameters):
        if len(parameters) != len(self.parameters):
            parameters = self.dump()
            
        return self.function(key, *parameters)
        
    def set(self, what, how):
        for i in xrange(len(self.parameters)):
            if self.parameters[i] == what:
                self.parameters[i +1] = how
                return
    
    def get(self, what):
        for i in xrange(len(self.parameters)):
            if self.parameters[i] == what:
                return self.parameters[i +1]
    
    def dump(self):
        return [self.parameters[i] for i in xrange(len(self.parameters)) if (i % 2) == 1]

    def names(self):
        return [self.parameters[i] for i in xrange(len(self.parameters)) if (i % 2) == 0]

    def __getitem__(self, key):
        return self.function(key, *self.dump())

windows = {
    'No window' : WindowFunction('No window', ones, []) #,
#    'Bartlett' : WindowFunction('Bartlett', bartlett, []),
#    'Blackman' : WindowFunction('Blackman', blackman, []),
#    'Hamming' : WindowFunction('Hamming', hamming, []),
#    'Hanning' : WindowFunction('Hanning', hanning, []),
#    'Kaiser' : WindowFunction('Kaiser', kaiser, ["Beta", 14])
}

if __name__ == "__main__":
    for name in windows:
        print "Using window", name
        print windows[name][15]
