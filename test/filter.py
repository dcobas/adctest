from sys import argv

def adj(x):
    return round(x/5.0 * (2**15))

src = open(argv[1], "r")
lines = [int(i.split(", ")[-1][:-1], int(argv[5])) for i in src.readlines()]
src.close()

dest = open(argv[2], "w")
dest.write("[SIGNAL]\nnbits = %s\nrate = %s\ndata = " % (argv[3], argv[4]))
dest.writelines('\t%d\n ' % i for i in lines[int(argv[6]):])
dest.close()    
 

