#!  /bin/sh
#   coding: utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from numpy import linspace, pi, sin

def sampled_sine(A, w, phase, C, fs, t0=0.0, t1=1.0):
    samples = (t1 - t0) * fs
    time = linspace(t0, t1, samples, endpoint=False)
    wave = A * sin(w * time + phase) + C
    return wave

if __name__ == '__main__':
    from matplotlib import pyplot as pl

    s = sampled_sine(1, 2*pi, 0, 0, 8000)
    pl.plot(s)
    print 'samples = %d' % s.size
    pl.show()
