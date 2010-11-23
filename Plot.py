import wx
from wx.lib.pubsub import Publisher as pub

import matplotlib
matplotlib.use('WX')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
from matplotlib.figure import Figure

#FIXME remove when unused
from numpy import arange, sin, pi, cos

__doc__ = """
    This module contains the definitions of all the graphs used in the app.
    It is the only one interfacing with matplotlib.
"""

class Signal(FigureCanvas):
    """ Represents the raw data from a Signal, right after being loaded from a file (Tab 1)
    """
    def __init__(self, parent):
        self.figure = Figure((5,3)) # 5,3 is the initial figure 
        FigureCanvas.__init__(self, parent, -1, self.figure)
        self.axes = self.figure.add_subplot(111)
        
    """ Specifies what has to be done if the signal is changed (the data has to be re-plotted)
    """
    def update(self, data): 
        self.axes.clear()
        self.axes.plot(arange(0,len(data),1) ,data, '.')
        self.draw()


class DNL(Signal):
    """ Represents the DNL plot
    """
    def __init__(self, parent):
        Signal.__init__(self, parent)
        
class INL(Signal):
    """ Represents the INL plot
    """
    def __init__(self, parent):
        Signal.__init__(self, parent)

class Histogram(Signal):
    """ Represents the histogram plot
    """
    def __init__(self, parent):
        Signal.__init__(self, parent)
    
    """ Specifies what has to be done if the signal is changed (the data has to be re-plotted)
    """
    def update(self, histogram, ideal_histogram):
        self.axes.clear()
        self.axes.plot(arange(0,len(histogram),1), histogram, '.') 
        self.axes.plot(arange(0,len(ideal_histogram),1), ideal_histogram, '.')        
        self.draw()

class FFT(Signal):
    """ Represents the FFT plot 
    """
    def __init__(self, parent):
        Signal.__init__(self, parent)
    
    def update(self, fft, harmonic_peaks):
        self.axes.clear()
        self.axes.plot(arange(0,len(fft),1) , fft, '.') 
        self.axes.plot(arange(0,len(harmonic_peaks),1) ,harmonic_peaks, '.')        
        self.draw()
    


