from numpy import*
from math import *
import matplotlib.pyplot as pl


def adc_transfer(fsr, bits,inl):
    
    #MAKING THE TRANSFER FUNCTION
    a=float(math.pow(2,bits))
    lsb=float(fsr/a)
    print("the LSB is"),lsb
    digital=[]
    analog=[]
    plot_analog=[]
    plot_digital=[]
    straight_line=[]
    for i in range (a):
        b=lsb*i
        analog.append(b)
        #THE INL ERROR HAS AN INFLUANCE ON THE Y-AXES(thus,on "digital"and "plot_digital")
        digital.append(i+inl)
        dnl=input ("WHAT IS THE DNL ERROR AT THIS STEP? : ")
        d=(dnl*lsb)
        for w in range(a):
        #THE DNL ERROR HAS AN INFLUANCE ON THE Y-AXES(thus,on "analog" and "plot_analog")
            plot_analog.append((w/a+i)*lsb+d)
            plot_digital.append(digital[i])
            if (w==a/2):
                 straight_line.append((w/a+i)*lsb)
        



            
    print ("THE ANALOG VALUES ARE: "),analog [:]
    print ("THE DIGITAL VALUES ARE: "),digital[:]
    print ("plot_analog:   "),plot_analog[:]
    print ("plot_digital:  "),plot_digital[:]
    print ("THE STRAIGHT LINE VECTOR IS: "),straight_line[:]
    
    
    #PLOTTING THE TRANSFER FUNCTION
#    pl.plot(plot_analog, plot_digital)
#    pl.show()

    #PLOTTING THE STRAIGHT LINE OF THE TRANSFER FUNCTION
#    pl.plot(straight_line,digital)
#    pl.show()

    pl.plot(plot_analog,plot_digital)
    pl.show()
    return analog,digital


full_scale_range=input("GIVE ME THE FULL SCALE RANGE: ")
num_of_bits=input("GIVE ME THE NUMBER OF BITS: ")
inl_error=float(input("PLEASE GIVE ME THE INL ERROR: "))
adc_transfer(full_scale_range,num_of_bits,inl_error)
