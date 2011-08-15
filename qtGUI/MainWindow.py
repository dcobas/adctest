from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qwt5 import *

import os, os.path
import MainUI
import SignalProcessing.WindowFunction


from SignalProcessing.Signal import *
from SignalProcessing.SingleToneSignal import *
from SignalProcessing.TwoToneSignal import *

from numpy import *
from PyQt4.Qwt5 import QwtPlotGrid  

class MainWindow(QMainWindow):
    modes = (("Single tone performances",       SingleToneSignal),
             ("Two tones intermodulation",      TwoToneSignal),
             ("Frequency response evaluation",  Signal),
             ("Time signal representation",     Signal))[0:1]
             
    # nell'ordine
    tabs  = ((True,  True,  True,  True,  True, False, False),
             (True, False, False, False, False,  True, False),
             (True, False, False, False, False, False,  True),
             (True, False, False, False, False, False, False))
    
    def window(self):
        return self.signal[str(self.ui.windowBox.currentText())]
    
    def __getitem__(self, what):
        return self.plots[what][1]
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        
        self.ui =  MainUI.Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.target = ""
        self.mode = 0
        self.signal = self.modes[self.mode][1]()
        
        # populate the mode box
        self.ui.modeBox.addItems(map(lambda x: x[0], self.modes))
        
        # populate window box
        windows = SignalProcessing.WindowFunction.windows.keys()
        self.ui.windowBox.addItems(windows)
        
        self.ui.actionOpen.activated.connect(self.slotOpenfile)
        self.ui.actionQuit.activated.connect(self.close)
        self.ui.peaksBox.editingFinished.connect(self.update)
        self.ui.windowBox.currentIndexChanged.connect(self.update)
        self.ui.modeBox.currentIndexChanged.connect(self.updateTabs)
        
        # plot creation
        self.plots   = {}
        self.order = []
        self.setupGraph('time', ["&Signal Waveform", "Time [Fs*s]", "Signal"], (False, False))
        self.setupGraph('freq', ["Spectral &Analysis", "Frequency [Hz]", "Signal [dB]"], (False, False))
        self.setupGraph('dnl',  ["&DNL", "Value", "Occurrencies"], (False, False))
        self.setupGraph('inl',  ["&INL", "Value", "Occurrencies"], (False, False))
        self.setupGraph('hist', ["&Histograms", "Value", "Occurrencies"], (False, False))
        self.setupGraph('ttm',  ["&Two Tone", "Frequency [Hz]", "Signal [dB]"], (False, False))
        self.setupGraph('ft',   ["&Frequency response", "Frequency [Hz]", "Amplitude [dB]"], (False, False))
        
        self.updateTabs()
        
        # curves creation
        self.setupCurve("time", "original", "ADC signal", Qt.blue)
        self.setupCurve("time", "theoretical", "Theoretical signal", Qt.yellow)
        self.setupCurve("time", "windowed", "Windowed signal", Qt.red)
        
        self.setupCurve("freq", "original", "Amplitude", Qt.blue, QwtPlotCurve.Sticks)
        
        self.setupCurve("dnl", "original", "DNL", Qt.blue   )
        
        self.setupCurve("inl", "original", "INL", Qt.blue)
        
        self.setupCurve("hist", "real", "Real Histogram", Qt.blue, QwtPlotCurve.Sticks)
        self.setupCurve("hist", "ideal", "Ideal Histogram", Qt.red, QwtPlotCurve.Sticks)
        
        self.setupCurve("ttm", "original", "Amplitude", Qt.blue, QwtPlotCurve.Sticks)
        
        self.setupCurve("ft", "original", "Amplitude", Qt.blue)
        
        self.update()
    
    def updateTabs(self):
        self.mode = self.ui.modeBox.currentIndex()
        self.ui.tabWidget.clear()
        for i in zip(self.tabs[self.mode], self.order):
            if i[0]:
                self.ui.tabWidget.addTab(self.plots[i[1]][0], self.plots[i[1]][1].tabName)   
        
    
    def setupCurve(self, name, cname, title, pencolor = Qt.blue, cs = QwtPlotCurve.Lines):
        plot = self[name]
        curve =  QwtPlotCurve(title)
        plot.curves[cname] = curve
        curve.setStyle(cs)
        curve.setRenderHint(QwtPlotItem.RenderAntialiased)
        curve.setPen(QPen(pencolor))
        curve.setYAxis(QwtPlot.yLeft)
        curve.attach(plot)
    
    def setupGraph(self, name, title, isLog):
        w = QWidget()
        graph = QwtPlot(w)
        graph.curves = {}
        graph.tabName = title[0][:]
        title[0] = title[0].replace("&", "")
        
        w.myLayout = QVBoxLayout()
        w.myLayout.addWidget(graph)
        w.setLayout(w.myLayout)
        
        self.plots[name] = (w, graph)
        self.order.append(name)
        
        graph.grid = QwtPlotGrid()
        graph.grid.enableXMin(True)
        graph.grid.enableYMin(True)
        graph.grid.enableX(True)
        graph.grid.enableY(True)
        graph.grid.setMajPen(QPen(Qt.black, 0, Qt.DotLine))
        graph.grid.setMinPen(QPen(Qt.gray, 0 , Qt.DotLine))
        graph.setTitle(title[0])
        
        graph.legend = QwtLegend()
        graph.legend.setFrameStyle(QFrame.Box | QFrame.Sunken)
        graph.legend.setItemMode(QwtLegend.ClickableItem)
        graph.insertLegend(graph.legend, QwtPlot.BottomLegend)
        
        graph.setAxisTitle(QwtPlot.xBottom, title[1])
        graph.setAxisTitle(QwtPlot.yLeft, title[2])
        
        if isLog[0]: 
            graph.setAxisScaleEngine(QwtPlot.xBottom, QwtLog10ScaleEngine())
        else:
            graph.setAxisScaleEngine(QwtPlot.xBottom, QwtLinearScaleEngine())
        if isLog[1]: 
            graph.setAxisScaleEngine(QwtPlot.yLeft, QwtLog10ScaleEngine())
        else:
            graph.setAxisScaleEngine(QwtPlot.yLeft, QwtLinearScaleEngine())
        
        graph.grid.attach(graph)
                
        graph.zoomers = []
        if True:
            zoomer = QwtPlotZoomer(
                QwtPlot.xBottom,
                QwtPlot.yLeft,
                QwtPicker.DragSelection,
                QwtPicker.AlwaysOff,
                graph.canvas())
            zoomer.setRubberBandPen(QPen(Qt.green))
            graph.zoomers.append(zoomer)

            zoomer = QwtPlotZoomer(
                QwtPlot.xTop,
                QwtPlot.yRight,
                QwtPicker.PointSelection | QwtPicker.DragSelection,
                QwtPicker.AlwaysOff,
                graph.canvas())
            zoomer.setRubberBand(QwtPicker.NoRubberBand)
            graph.zoomers.append(zoomer)

        graph.picker = QwtPlotPicker(
            QwtPlot.xBottom,
            QwtPlot.yLeft,
            QwtPicker.PointSelection | QwtPicker.DragSelection,
            QwtPlotPicker.CrossRubberBand,
            QwtPicker.AlwaysOn,
            graph.canvas())
        graph.picker.setRubberBandPen(QPen(Qt.black))
        graph.picker.setTrackerPen(QPen(Qt.black))
    
    def fetchTD(self):
        enabled = self.signal.nsamples != 0
        
        return enabled, self.signal.data, self.window().data, self.window().th
            
    def fetchFFT(self):
        enabled = self.signal.nsamples != 0
        data = self.window()
        
        if enabled:
            peaks = list(data.logHarmonicPeaksGenerator(2, 2 + self.ui.peaksBox.value()))
        else:
            peaks = []
        
        return enabled, data, peaks
    
    def fetchHist(self):
        enabled = self.signal.nsamples != 0
        
        return enabled, self.realHistogram, self.idealHistogram, self.DNL, self.maxDNL, self.INL, self.maxINL
    
    def redrawPlots(self, *args, **kwargs):
        x = self.signal.nsamples
        timeRange = arange(x)
        self['time'].curves['original'].setData(timeRange, self.signal.data)
        self['time'].curves['windowed'].setData(timeRange, self.window().data)
        self['time'].curves['theoretical'].setData(timeRange, self.window().th)
        self['time'].replot()

        freqRange = arange(x/2)
        self['freq'].curves['original'].setData(freqRange, self.window().ldft[:x/2])
        self['freq'].replot()
        
        hRange = arange(len(self.signal.DNL))
        self['dnl'].curves['original'].setData(hRange, self.signal.DNL)
        self['dnl'].replot()
        self['inl'].curves['original'].setData(hRange, self.signal.INL)
        self['inl'].replot()
        hRange = arange(len(self.signal.realHistogram))
        self['hist'].curves['real'].setData(hRange, self.signal.realHistogram)
        self['hist'].replot()
        self['hist'].curves['ideal'].setData(hRange, self.signal.idealHistogram)
        self['hist'].replot()
    
    def update(self, *args, **kwargs):
        self.ui.propertiesList.clear() 
        
        if self.signal.nsamples > 0  :
            peaks = list(self.window().logHarmonicPeaksGenerator(2, 2 + self.ui.peaksBox.value()))
            
            items = [QTreeWidgetItem([i[0], i[1] % i[2]]) for i in self.signal.items()]
            self.ui.propertiesList.addTopLevelItems(items)
            
            items = [QTreeWidgetItem([i[0], i[1] % i[2]]) for i in self.window().items()]
            self.ui.propertiesList.addTopLevelItems(items)
            
            for x in xrange(len(peaks)):
                self.ui.propertiesList.addTopLevelItem(QTreeWidgetItem(["Harmonic no. %d" % (x +2), "%.6f dB" % peaks[x][2]]))
       
        self.redrawPlots()
    
    def slotOpenfile(self):
        fileName = str(QFileDialog.getOpenFileName(self, caption = "Open file", filter = "*.txt"))
        
        if fileName != "": 
            self.loadSignal(fileName)
    
    def loadSignal(self, fileName):
        print "Opening", fileName, len(fileName)
        self.signal = self.modes[self.mode][1](*readFile(fileName)) 
        self.update()
        
    
    
