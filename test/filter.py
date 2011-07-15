from sys import argv

def adj(x):
    return round(x/5.0 * (2**15))

src = open(argv[1], "r")
lines = ['\t' + i for i in src.readlines()]
src.close()

dest = open(argv[2], "w")
dest.write("[SIGNAL]\nnbits = 24\nrate = 1000000\n=ndata = ")
dest.writelines(lines)
dest.close()    
 

