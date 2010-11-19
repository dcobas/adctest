# FIXME the following two lines raise an error
# import wxversion
# wxversion.ensureMinimal('2.8')
# Used to guarantee to use at least Wx2.8
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
        self.figure = Figure()
        FigureCanvas.__init__(self, parent, -1, self.figure)
        self.axes = self.figure.add_axes([0.085, 0.05, 0.85, 0.9])
        
    def update(self, data): 
        self.axes.clear()
        self.axes.plot(arange(0,len(data),1) ,data, '.')        
        self.draw()
        
    


