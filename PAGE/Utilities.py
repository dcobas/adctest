def Property(func):
    return property(**func())

decodeDict = {'KHZ': 3, 'MHZ': 6, 'HZ':0, 'UHZ': -6, 'NHZ': 9, 
              'MV': -3, 'NV': -6, 'KV': 3, 'V':0,
              'MVPP': -3, 'NVPP': -6, 'KVPP': 3, 'VPP':0}

def decode(values):
    return float(values[0])* (10.**float(decodeDict[values[1].upper()]))

def parse(value, s):
    if type(value) is str:
        value = value.split(" ")
        value[0] = float(value[0])
        value = tuple(value)
    
    if type(value) is tuple and len(value) == 1:
        value = value[0]
        
    if type(value) is not tuple: 
        value = (value, s)
    
    return tuple(str(i) for i in value)

def prettyParameter(x, vx):
    print 'Parameter %s is called %s.' % (x, vx[0])
    print 'Description:', vx[1]
    print 'Default value, in %s, is %s' % (repr(vx[3]), repr(vx[2]))

