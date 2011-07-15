# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="federico"
__date__ ="$Jul 11, 2011 2:40:18 PM$"

from numpy import *
from scipy import optimize

def sineguess(dft, rate, nsamples):
    w0index = argmax(dft)
    w0 = w0index * (2 * pi * rate) / nsamples

    return w0, w0index

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

def sinefit4(data, Ts, w0):
    # Target function
    fitfunc = lambda p, x: p[0]*cos(p[3]*x) +p[1]*sin(p[3]*x) +p[2]

    # Distance to the target function
    errfunc = lambda p, x, y: fitfunc(p, x) - y

    # Initial guess for the parameters
    A, B, C = sinefit3(data, Ts, w0)
    p0 = [A, B, C, w0];

    # Time serie
    n = data.size
    Tx = arange(n) * Ts

    p1, success = optimize.leastsq(errfunc, p0[:], args=(Tx, data))

    return p1

def makesine(samples, periods, bits, amplitude=1, noise=0):
    t = arange(samples)/float(samples)
    sine = amplitude * sin(2*pi*periods*t)
    sine += noise * ((t % 0.02) / 0.02 - 0.01)
    sine = (sine * 2**bits + 0.5).astype(int)
    place(sine, sine >=  2**bits, 2**bits)
    place(sine, sine <= -2**bits, -2**bits)
    return sine

if __name__ == "__main__":
    sine = makesine(20000, 20, 12, 443, 10)
    print sine

    dft = 10*log10(abs(fft.rfft(sine)))

    w0, w0index = sineguess(dft, 133, 20000)
    out = sinefit4(sine, 2*pi*(133**-1), w0)

    print w0, w0index, out

    orig = makesine(20000, 20, 12, 443, 0);
    noise = sine -orig

    ndft = 10*log10(abs(fft.rfft(noise)))
    print noise
    snr = sum(dft**2)/sum(ndft**2)
    print "SNR:", snr