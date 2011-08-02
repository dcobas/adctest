from Signal import *

class TwoToneSignal(Signal):
    """A class that represent a time-domain sampled signal with two sinusoids
    with similiar frequenciess. 
    """
    
    def __init__(self, nbits = 0, rate = 1, data = []):
        """initialize a signal object

        nbits: bit width of the sample values
        rate: sampling rate of sample production
        data: an array of samples (usually nbits-long words, stored in
              a numpy array)
        """
        super(TwoToneSignal, self).__init__(nbits, rate, data)
        
    
    def items(self):
        output = super(TwoToneSignal, self).items()
        
        output.append(('The cake is a lie', "%s ", True))
        return output    
    
    def precalculateAll(self):
        """Evaluates all the parameters of the signal, and also call the
        precalculate method for each window function we know."""
        return

