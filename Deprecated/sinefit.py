#!  /bin/sh
#   coding: utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from numpy import *

from matplotlib import pyplot as pl

def sinefit3(samples, sample_t, w0):
    """fit a sampled wave to a sine of kwnown frequency
    
    This routine implements the algoritm of IEEE 1241, sect. 4.1.4.1.,
    fitting a sine of given frequency w0 to the samples given, which are
    assumed equally spaced by a sample period of sample_t
    
        a0 cos(w0 t + theta) + b0 sin(w0 t + theta) + c0
    
    The return value is the triple (a0, b0, c0) 
    """

    n = samples.size
    t = w0 * arange(n) * sample_t
    D0T = matrix(vstack([cos(t), sin(t), ones(n)]))
    D0 = D0T.T
    x0 = (D0T * D0).I * D0T * matrix(samples).T
    return array(x0).reshape((3,))


# page 27
def sinefit4(samples, sample_t, w0, tol=1e-4):
    """fit a sampled wave to a sine of unknown frequency

    This routine implements the algorithm of IEEE 1241, sect. 4.1.4.3.,
    fitting a sine wave the the samples given, which are assumed equally
    spaced in time by a sample period sample_t. 

        a0 cos(w0 t + theta) + b0 sin(w0 t + theta) + c0

    An initial frequency estimate w0 is required to start, and an
    optional relative error in frequency is admitted (1e-4 by default)

    The return value is the quadruple (w0, a0, b0, c0)
    """

    a0, b0, c0 = sinefit3(samples, sample_t, w0)
    deltaw0 = 0
    print "Params: %f, %f" % (sample_t, w0)
    print "a0\tb0\tc0\tdeltaw0"
    print "%f\t%f\t%f\t%f" % (a0, b0, c0, deltaw0)
    
    # we could move n and t definitions outside the while loop
    
    while True:
        # update freq
        w0 += deltaw0
        
        # get our array t1 -> tn
        n = samples.size
        t = arange(n) * sample_t
        
        # multiply it with the frequency
        w0t = w0 * t
        
        # create the nX4 matrix and its transpose
        D0T = matrix(vstack([cos(w0t), sin(w0t), ones(n),
                    -a0*t*sin(w0t) + b0*t*cos(w0t)]))
        D0 = D0T.T
        
        # get the solution
        x0 = (D0T * D0).I * D0T * matrix(samples).T
        x0 = array(x0).reshape((4,))
        a0, b0, c0, deltaw0 = x0
        
        print "%f\t%f\t%f\t%f" % (a0, b0, c0, deltaw0)
        if abs(deltaw0/w0) < tol:
            print "%f/%f < %f" % (deltaw0, w0, tol) 
            return (w0+deltaw0, a0, b0, c0)




if __name__ == '__main__':

    a = 0.0
    b = 10*pi
    samples = 2000
    w = 1
    samp = sin(w*linspace(a, b, samples))
  
    # fitting with known frequency
    a0, b0, c0 = sinefit3(samp, (b-a)/samples, w)
    ampl = hypot(a0, b0)
    theta = arctan2(a0, b0)
    print '--- %.2f * sin(%.5f t + %.2f) + %.2f' % (ampl, w, theta, c0)

    # fitting with free frequency
    err = 1+0.1*(random.random_sample() - 0.05)
    w0, a0, b0, c0 = sinefit4(samp, (b-a)/samples, w*err)
    ampl  = hypot(a0, b0)
    theta = arctan2(a0, b0)
    print '%.2f * sin(%.5f t + %.2f) + %.2f' % (ampl, w0, theta, c0)
