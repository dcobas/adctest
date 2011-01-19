from numpy import*
from math import *
import matplotlib.pyplot as pl


def adc_transfer(fsr, bits):
    
    #MAKING THE TRANSFER FUNCTION
    a=float(math.pow(2,bits))
    lsb=float(fsr/a)
    print("the LSB is"),lsb
    digital=[]
    analog=[]
    plot_analog=[]
    plot_digital=[]
    for i in range (a):
        b=lsb*i
        analog.append(b)
        digital.append(i)
        for j in range(a):
            plot_digital.append(digital[i])
        for w in range(a):
            plot_analog.append((w/a+i)*lsb)                    
        



            
    print ("THE ANALOG VALUES ARE: "),analog [:]
    print ("THE DIGITAL VALUES ARE: "),digital[:]
    print ("plot_analog:   "),plot_analog[:]
    print ("plot_digital:  "),plot_digital[:]
    
    
    #PLOTTING THE TRANSFER FUNCTION
    pl.plot(plot_analog, plot_digital)
    pl.show()
    
    return analog,digital


full_scale_range=input("GIVE ME THE FULL SCALE RANGE: ")
num_of_bits=input("GIVE ME THE NUMBER OF BITS: ")
adc_transfer(full_scale_range,num_of_bits)
