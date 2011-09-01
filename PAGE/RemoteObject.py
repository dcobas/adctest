import sys
import Pyro4
import Item

from Utilities import *
from numpy import *

"""This class represents a remote object, using Pyro4 framework.
All it needs is a URI."""
class RemoteObject(Item.Item, Pyro4.Proxy):
        
    _parameters = {'uri': ['URI', 'Name of the service', '', str]}
                  
    def __init__(self, *args, **kwargs):
        Item.Item.__init__(self, *args, **kwargs)
        Pyro4.Proxy.__init__(self, uri = Pyro4.locateNS().lookup(self.uri))

name = 'Remote Object'
target = RemoteObject

