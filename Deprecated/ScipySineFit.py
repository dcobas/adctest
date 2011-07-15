# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="federico"
__date__ ="$Jul 8, 2011 2:51:20 PM$"

from pylab import *
from scipy import *
import sinefit
from scipy import optimize

def sinefit4(data, Ts, w0):
    # Target function
    # fitfunc = lambda p, x: p[0]*cos(2*pi/p[1]*x+p[2]) + p[3]*x
    fitfunc = lambda p, x: p[0]*cos(p[3]*x) +p[1]*sin(p[3]*x) +p[2]


    # Distance to the target function
    errfunc = lambda p, x, y: fitfunc(p, x) - y

    # Initial guess for the parameters
    # p0 = [-15., 0.8, 0., -1.]
    A, B, C = sinefit.sinefit3(data, Ts, w0)
    p0 = [A, B, C, w0];

    # Time serie
    n = data.size
    Tx = arange(n) * Ts
    
    p1, success = optimize.leastsq(errfunc, p0[:], args=(Tx, data))

    return p1[3]

if __name__ == "__main__":
    pass
