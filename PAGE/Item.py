__author__ = "Federico Asara"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Federico Asara", "Juan David Gonzalez Cobas"]
__license__ = "GPL2"
__version__ = "1.0.0"
__maintainer__ = "Federico Asara"
__email__ = "federico.asara@gmail.com"
__status__ = "Production"

"""This class just represent an API item. An item is configurable and has two
methods, get and set, which actually wrap getattribute and setattr."""
class Item(object):
    
    # these are the default values of the parameters used
    # 
    # the key of the dictionary is the actual name of the parameter in the class
    # the item is a list:
    # 1. Name of the parameter
    # 2. Description
    # 3. Default value
    # 4. Type (it's just an object, really)
    _parameters = {}

    def __init__(self, *args, **kwargs):
        """Create the object and loads alll the parameters from kwargs.
        Look at _parameters for more information."""
        
        self.parameters = dict(self._parameters)
        
        for i in kwargs: 
            if i in self.parameters.keys():
                self.parameters[i][2] = kwargs[i]
        for i in self.parameters.keys():
            self.__setattr__(i, self.parameters[i][2])
    
