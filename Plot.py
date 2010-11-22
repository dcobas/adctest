import wx
from wx.lib.pubsub import Publisher as pub

import matplotlib
matplotlib.use('WX')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
from matplotlib.figure import Figure

#FIXME remove when unused
from numpy import arange, sin, pi, cos

class Signal(FigureCanvas):
    def __init__(self, parent):
        self.figure = Figure((5,3)) # 5,3 is the initial figure 
        FigureCanvas.__init__(self, parent, -1, self.figure)
        self.axes = self.figure.add_subplot(111)
        
    def update(self, data): 
        self.axes.clear()
        self.axes.plot(arange(0,len(data),1) ,data, '.')
        self.draw()


class DNL(Signal):
    def __init__(self, parent):
        Signal.__init__(self, parent)
        
class INL(Signal):
    def __init__(self, parent):
        Signal.__init__(self, parent)

class Histogram(Signal):
    def __init__(self, parent):
        Signal.__init__(self, parent)
    
    def update(self, dataReal, dataIdeal):
        self.axes.clear()
        self.axes.plot(arange(0,len(dataReal),1) , dataReal, '.') 
        self.axes.plot(arange(0,len(dataIdeal),1) ,dataIdeal, '.')        
        self.draw()
    


