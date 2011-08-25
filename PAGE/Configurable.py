
class Configurable(object):
    parameters = {}
    
    def applyDefaults(self, o = None):
        if o is None: 
            o = self
        for i in self.parameters:
            self.save(i,self.parameters[i][2])
    
    def register(self, parameter, position, description, default, kind):
        self.parameters[parameter] = (position, description, default, kind)
        
    def save(self, parameter, value, o = None):
        if o is None: 
            o = self
        o.__setattr__(self.parameters[parameter][0], value)
    
    def read(self, parameter, o = None):
        if o is None: 
            o = self
        return o.__getattr__(self.parameters[parameter][0])
    

