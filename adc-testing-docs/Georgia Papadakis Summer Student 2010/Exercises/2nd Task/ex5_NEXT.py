from numpy import*
from math import *
import matplotlib.pyplot as pl

#def Denary2Binary(n):
#    #convert denary integer n to binary string bStr
#    bStr = ''
#    if n < 0: raise ValueError, "must be a positive integer"
#    if n == 0: return '0'
#    while n > 0:
#       bStr = str(n % 2) + bStr
#       n = n >> 1
#    return bStr

def adc_transfer(v, fsr, bits):
    
    #MAKING THE TRANSFER FUNCTION
    a=2.0**bits
    lsb=float(fsr/a)
    print("the LSB is"),lsb
    digital=[]
    analog=[]
    for i in range (a):
        b=lsb*i
        analog.append(b)
        digital.append(i)
    print ("THE ANALOG VALUES ARE: "),analog [:]
    print ("THE DIGITAL VALUES ARE: "),digital[:]
    
    #PLOTTING THE TRANSFER FUNCTION
    #pl.plot(analog, digital)
    #pl.show()
    
    #AND NOW THE CORRESPONDANCE!!!
   
    i=0
    if (v>=analog[0]) and (v<=analog[int(math.pow(2,bits)-1)]):
       while i<=a:
           if (v>=analog[i]) and (v<analog[i+1]):
               return digital[i]
           i=i+1
    elif (v>analog[int(math.pow(2,bits)-1)]) :
        return digital[int(math.pow(2,bits)-1)]
    else:
        return digital[0]
            



voltage_value=float(input("GIVE ME THE VOLTAGE VALUE: "))
full_scale_range=input("GIVE ME THE FULL SCALE RANGE: ")
num_of_bits=input("GIVE ME THE NUMBER OF BITS: ")

        
digital_value=adc_transfer(voltage_value,full_scale_range,num_of_bits)
print ("THE DIGITAL VALUE CORRESPONDING TO THE ANALOG IS :"),digital_value
