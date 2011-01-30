#!  /bin/sh
#   coding: utf-8
#   vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

def ideal_adc(vals, N, Vmin, Vmax, mid_tread=False):
    """computes an ideal ADC characteristic function

    vals is a vector of values to be converted by an 
    ideal ADC whose characteristic is defined by the Vmin and Vmax full
    scale range, and the N number of bits. The optional mid_tread
    parameter allow to use the mid_tread convention as per
    IEEE 1241 sec. 1.2.

    A vector of converted vals object is returned, taking into account
    saturation at both ends of scale
    """

    FS = float(Vmax - Vmin)
    lsb = FS / 2**N

    if mid_tread:
        vals = vals + lsb/2

    t = (vals - Vmin) / lsb
    print vals, t
    code = array(t, dtype=int)
    code[code<0] = 0
    code[code>(2**N-1)] = 2**N-1
    return code

if __name__ == '__main__':

    from numpy import *
    from matplotlib import pyplot as pl

    v = linspace(-1.0, 11, 3000)
    print v
    my_adc = ideal_adc(v, 4, 0, 10.0, mid_tread=1)
    pl.plot(v, my_adc)
    pl.show()
