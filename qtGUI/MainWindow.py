from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qwt5 import *
import cPickle

import os, os.path
import MainUI
import SignalProcessing.WindowFunction

from PAGE.SineWaveform import *
from PAGE.RemoteObject import *


from ModuleSelector import *
from SourceSelector import *

from SignalProcessing.Signal import *
from SignalProcessing.SingleToneSignal import *
from SignalProcessing.TwoToneSignal import *
from SignalProcessing.Utilities import readFile

from numpy import *
from PyQt4.Qwt5 import QwtPlotGrid  
import time

class MainWindow(QMainWindow):
    # nell'ordine
    tabs  = ((True,  True,  True,  True,  True, False, False),
             (True, False, False, False, False,  True, False),
             (True, False, False, False, False, False,  True),
             (True, False, False, False, False, False, False))
    
    def window(self, i = None):
        if i is None:
            i = int(self.ui.freqBar.value())
        if type(i) is int: 
            return self.signals[i][str(self.ui.windowBox.currentText())]
        
        return i[str(self.ui.windowBox.currentText())]
    
    def __getitem__(self, what):
        return self.plots[what][1]
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui =  MainUI.Ui_MainWindow()
        self.ui.setupUi(self)
                
        # chain hooks
        self.blueprints = {'file': self.filePlan,
                           'synth': self.synthPlan,
                           'fc': self.fcPlan,
                           'adc': self.adcPlan}
        
        self.dataFetch = {'file': self.fetchFile,
                           'synth': self.fetchSynth,
                           'fc': self.fetchFC,
                           'adc': self.fetchADC}
        
        # which chain we are using
        self.chain = 'none'
        
        # ADC object
        self.adc = None
        
        # Wave object
        self.wave = None
        
        # Generator object
        self.gen = None
        
        # Signals to show
        self.signals = [Signal()]
        
        # Control Boxes settings
        self.controlBoxesEnabler = {'file': (False, False, False, True),
                                    'synth': (True, False, True, True),
                                    'fc': (True, True, True, True),
                                    'adc': (False, True, True, True)}
                                    
        self.controlBoxesWidgets = (self.ui.fsBox, self.ui.acqBox, self.ui.wgBox, self.ui.dataBox)
        
        self.ui.wgFSR.setValue(5.)
        self.ui.wgBits.setValue(24)
        self.ui.wgFs.setValue(50e6)
        self.ui.wgSamples.setValue(10000)
        
        # populate window box
        windows = SignalProcessing.WindowFunction.windows.keys()
        self.ui.windowBox.addItems(windows)
        self.ui.windowBox.currentIndexChanged.connect(self.update) # check if..
        
        self.ui.actionQuit.activated.connect(self.close)
        self.ui.actionNew_Analysis.activated.connect(self.test)
        self.ui.actionFull_Chain_rapid_test.activated.connect(self.fcrtest)
        self.ui.fsGo.clicked.connect(self.update)
        self.ui.freqBar.valueChanged.connect(self.updateBar)
        self.ui.actionDump.activated.connect(self.dump)
        
        # plot creation
        self.plots = {}
        self.order = []
        
        self.setupGraph('time', ["&Signal Waveform", "Time [Fs*s]", "Signal"], (False, False))
        self.setupGraph('freq', ["Spectral &Analysis", "Frequency [Hz]", "Signal [dB]"], (False, False))
        self.setupGraph('dnl',  ["&DNL", "Value", "Occurrencies"], (False, False))
        self.setupGraph('inl',  ["&INL", "Value", "Occurrencies"], (False, False))
        self.setupGraph('hist', ["&Histograms", "Value", "Occurrencies"], (False, False))
        self.setupGraph('ttm',  ["&Two Tone", "Frequency [Hz]", "Signal [dB]"], (False, False))
        self.setupGraph('ft1',   ["Frequency response (&amplitude)", "Frequency [Hz]", ""], (False, False))
        self.setupGraph('ft2',   ["Frequency response (&quality)", "Frequency [Hz]", ""], (False, False))
        
        # self.updateTabs()
        
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
        
        self.setupCurve("ft1", "original", "Amplitude", Qt.blue)
        
        self.setupCurve("ft2", "snr", "SNR", Qt.blue)
        self.setupCurve("ft2", "sinad", "SINAD", Qt.black)
        self.setupCurve("ft2", "thd", "THD", Qt.red)
        
        for i in self.order:
            self.ui.tabWidget.addTab(self.plots[i][0], self.plots[i][1].tabName)  
        
        # self.update()
    
    ############################################################################
    ## Dialogs
    ############################################################################
    def getModule(self, k):
        ms = ModuleSelector(parent = self, kind = k)
        ms.show()
        status = ms.exec_() == QDialog.Accepted
        
        if not status:
            print 'User cancel'
            return None
        
        return ms.generatePrefs()
    
    def test(self, *args, **kwargs):
        source = SourceSelector(self)
        source.show()
        status = source.exec_() == QDialog.Accepted
        
        if not status:
            print 'User cancel'
            return
        
        # get the output
        plan = source.answer()
        print plan
        
        self.blueprints[plan]()
    
    def dump(self):
        a = file('/tmp/alldump.adctest', 'w')
        cPickle.dump(self.signals, a)
        a.close()
        a = file('/tmp/singledump.adctest', 'w')
        cPickle.dump(self.signals[int(self.ui.freqBar.value())], a)
        a.close()
        print 'Dump'
        
    ############################################################################
    ## Plans
    ############################################################################
    def waveGenerate(self):
        rate = float(self.ui.wgFs.value())
        bits = int(self.ui.wgBits.value())
        
        data = self.wave.generate(float(self.ui.wgFs.value()), 
                                  int(self.ui.wgSamples.value()), 
                                  int(self.ui.wgBits.value()), 
                                  float(self.ui.wgFSR.value()))
        
        return bits, rate, data
    
    def waveUpdateUI(self):
        self.ui.fsStart.setValue(self.wave.get('frequency'))
        self.ui.fsEnd.setValue(self.wave.get('frequency'))
        self.ui.fsSteps.setValue(1)
        
    def adcUpdateUI(self):
        temp = self.adc.get('clockFrequencies')
        cfs = [str(i) for i in temp]
        self.ui.adcFs.clear()
        self.ui.adcFs.addItems(cfs)
        
        self.ui.adcFs.setCurrentIndex(temp.index(self.adc.get('clockFrequency')))
        self.ui.adcSamples.setValue(2**14)
    
    def adcAcquire(self):
        rate = float(self.ui.adcFs.currentText())
        bits = self.adc.get('nrBits')
        
        samples = int(self.ui.adcSamples.value())
        
        data = self.adc.readEvent(samples)
        
        return bits, rate, data
    
    def fcCreateList(self):
        start = float(self.ui.fsStart.value())
        end   = float(self.ui.fsEnd.value())
        steps = int(self.ui.fsSteps.value())
        
        if steps == 1:
            return [start]
        
        s = (end - start)/(float(steps) -1)
        
        return [start + i*s for i in xrange(steps)]
    
    def filePlan(self):
        fileName = str(QFileDialog.getOpenFileName(self, caption = "Open file", filter = "*.adc"))
        
        if fileName == "": 
            return
        
        self.chain = 'file'
        self.wave = None
        self.generator = None
        self.adc = None
        self.filename = fileName
        
        #print "Opening", fileName, len(fileName)
        #self.signal = [self.modes[self.mode][1](*readFile(fileName))]
        self.update()
    
    def synthPlan(self):
        wave = self.getModule('waveforms')
        
        if wave is None:
            return
        
        self.chain = 'synth'
        self.wave = wave[0](**wave[1])
        self.generator = None
        self.adc = None
        self.filename = None
        
        self.waveUpdateUI()
        
        self.update()
    
    def fcPlan(self):
        wave = self.getModule('waveforms')
        if wave is None:
            return
            
        generator = self.getModule('generators')
        if generator is None:
            return
            
        adc = self.getModule('adcs')
        if adc is None:
            return
        
        self.chain = 'fc'
        self.wave = wave[0](**wave[1])
        self.generator = generator[0](**generator[1])
        self.adc = adc[0](**adc[1])
        self.filename = None
        
        self.waveUpdateUI()
        self.adcUpdateUI()
        
        self.update()
    
    def adcPlan(self):
        adc = self.getModule('adcs')
        if adc is None:
            return
        
        self.chain = 'adc'
        self.wave = None
        self.generator = None
        self.adc = adc[0](**adc[1])
        self.filename = None
        
        self.adcUpdateUI()
        
        self.update()
    
    def fcrtest(self, *args, **kwargs):
        self.chain = 'fc'
        self.wave = SineWaveform()
        self.wave.frequency = 1e6
        self.generator = RemoteObject(uri = 'agilent')
        self.adc = RemoteObject(uri = 'sis33')
        self.filename = None
        
        self.waveUpdateUI()
        self.adcUpdateUI()
        
        self.update()
    
    def update(self, *args, **kwargs):
        print 'Fetching data:', self.chain
        bits, rate, data = self.dataFetch[self.chain]()
        
        print 'Data fetch complete, elaboration is beginning'
        
        decision = SingleToneSignal
        self.signals = [decision(bits, rate, i) for i in data]
        
        if len(data) > 1:
            avgItems = self.signals[0].items()
            d = array(map(lambda x: x[2], avgItems))
            
            for s in self.signals[1:]:
                d += array(map(lambda x: x[2], s.items()))
            d = d/float(len(self.signals))
            
            for j in xrange(len(d)):
                avgItems[j] = ('Avg. ' + avgItems[j][0], avgItems[j][1], d[j])
            
            avgItems2 = self.signals[0].items()
            d = array(map(lambda x: x[2], avgItems2))
            
            for s in self.signals[1:]:
                d += array(map(lambda x: x[2], s.items()))
            d = d/float(len(self.signals))
            
            for j in xrange(len(d)):
                avgItems2[j] = ('Avg. ' + avgItems2[j][0], avgItems2[j][1], d[j])
        
            self.avgItems = [QTreeWidgetItem([i[0], i[1] % i[2]]) for i in avgItems + avgItems2]
            self.ui.avgList.addTopLevelItems(self.avgItems[:])
            self.ui.avgList.show()
            self.ui.freqBar.show()
        else:
            self.ui.avgList.hide()
            self.ui.freqBar.hide()
            
        self.ui.freqBar.blockSignals(True)
        self.ui.freqBar.setMinimum(0)
        self.ui.freqBar.setMaximum(len(data) -1)
        self.ui.freqBar.setValue(0)
        self.ui.freqBar.blockSignals(False)
        
        self.updatePlots()
    
    def updatePlots(self, *args, **kwargs):
        self.updateST()
        self.redrawPlotsFR()
    
    def fetchFile(self):
        return readFile(self.fileName)
    
    def fetchSynth(self):
        print 'fetchSynth'
        self.frequencies = frequencies = self.fcCreateList()
        
        print frequencies
        output = []
        for i in frequencies:
            print i
            self.wave.frequency = i
            bits, rate, data = self.waveGenerate()
            
            output.append(data)
            print data
        
        return bits, rate, output
    
    def fetchFC(self):
        # if the generator cannot directly support this 
        playable = self.generator.adaptKeys()
        if type(self.wave) not in playable:
            def play():
                bits, rate, wave = self.waveGenerate()    
                self.generator.set('frequency', rate)
                self.generator.play(wave)
        else:
            def play():
                self.generator.play(self.wave)
        
        # play the wave
        self.frequencies = frequencies = self.fcCreateList()
        
        output = []
        for i in frequencies:
            self.wave.frequency = i
            
            play()
            time.sleep(0.5)
            bits, rate, wave = self.adcAcquire()
            output.append(wave)
        
        return bits, rate, output
    
    def fetchADC(self):
        bits, rate, wave = self.adcAcquire()
        
        return bits, rate, wave
    
    ############################################################################
    ## GUI setup
    ############################################################################
    def updateBar(self, *args, **kwargs):
        bar = self.ui.freqBar
        label = self.ui.freqLabel
        
        i = int(bar.value())
        label.setText("%g Hz" % self.frequencies[i])
        
        self.updatePlots()
    
    def updateTabs(self):
        self.ui.tabWidget.clear()
        
        for i in zip(self.tabs[self.mode], self.order):
            if i[0]:
                self.ui.tabWidget.addTab(self.plots[i[1]][0], self.plots[i[1]][1].tabName)  
                
    def updateControlBoxes(self):
        for (en, cb) in zip(self.controlBoxesEnabler[self.mode], self.controlBoxesWidgets):
            cb.setEnabled(en)
    
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
    
    
    ############################################################################
    ## Load data
    ############################################################################
    def fetchTD(self):
        i = int(self.ui.freqBar.value())
        enabled = self.signals[i].nsamples != 0
        
        return enabled, self.signals[i].data, self.window().data, self.window().th
            
    def fetchFFT(self):
        i = int(self.ui.freqBar.value())
        enabled = self.signals[i].nsamples != 0
        data = self.window()
        
        if enabled:
            peaks = list(data.logHarmonicPeaksGenerator(2, 2 + self.ui.peaksBox.value()))
        else:
            peaks = []
        
        return enabled, data, peaks
    
    def fetchHist(self):
        i = int(self.ui.freqBar.value())
        enabled = self.signals[i].nsamples != 0
        
        # ?
        return enabled, self.realHistogram, self.idealHistogram, self.DNL, self.maxDNL, self.INL, self.maxINL
    
    def redrawPlotsST(self, *args, **kwargs):
        print 'redrawPlotsST'
        
        i = int(self.ui.freqBar.value())
        x = self.signals[i].nsamples
        
        timeRange = arange(x)
        self['time'].curves['original'].setData(timeRange, self.signals[i].data)
        self['time'].curves['windowed'].setData(timeRange, self.window().data)
        self['time'].curves['theoretical'].setData(timeRange, self.window().th)
        self['time'].curves['windowed'].show()
        self['time'].curves['theoretical'].show()
        self['time'].replot()

        freqRange = arange(x/2)
        self['freq'].curves['original'].setData(freqRange, self.window().ldft[:x/2])
        self['freq'].replot()
        
        hRange = arange(len(self.signals[i].DNL))
        self['dnl'].curves['original'].setData(hRange, self.signals[i].DNL)
        self['dnl'].replot()
        self['inl'].curves['original'].setData(hRange, self.signals[i].INL)
        self['inl'].replot()
        hRange = arange(len(self.signals[i].realHistogram))
        self['hist'].curves['real'].setData(hRange, self.signals[i].realHistogram)
        self['hist'].replot()
        self['hist'].curves['ideal'].setData(hRange, self.signals[i].idealHistogram)
        self['hist'].replot()
    
    def redrawPlotsTT(self, *args, **kwargs):
        i = int(self.ui.freqBar.value())
        x = self.signals[i].nsamples
        timeRange = arange(x)
        self['time'].curves['original'].setData(timeRange, self.signals[i].data)
        self['time'].curves['windowed'].hide()
        self['time'].curves['theoretical'].hide()
        self['time'].replot()

        freqRange = arange(x/2)
        self['ttm'].curves['original'].setData(freqRange, self.signals[i].lfft[:x/2])
        self['ttm'].replot()
    
    def redrawPlotsFR(self, *args, **kwargs):
        m = len(self.signals)
        
        if m == 1: 
            return
            
        f = array(self.frequencies)
        amp = array([i.amplitude for i in self.signals])
        snr = array([self.window(i).SNR for i in self.signals])
        sinad = array([self.window(i).SINAD for i in self.signals])
        thd = array([self.window(i).THD for i in self.signals])
        
        print f
        print amp
        print snr
        print sinad
        print thd
        
        self['ft1'].curves['original'].setData(f, amp)
        self['ft1'].replot()
        
        self['ft2'].curves['snr'].setData(f, snr)
        self['ft2'].curves['sinad'].setData(f, sinad)
        self['ft2'].curves['thd'].setData(f, thd)
        self['ft2'].replot()

        
    
    ############################################################################
    ## Various
    ############################################################################
    def updateST(self, *args, **kwargs):
        I = int(self.ui.freqBar.value())
        self.ui.propertiesList.clear() 
        
        
        if self.signals[I].nsamples > 0:
            
            peaks = list(self.window().logHarmonicPeaksGenerator(2, 2 + self.ui.peaksBox.value()))
            
            items = [QTreeWidgetItem([i[0], i[1] % i[2]]) for i in self.signals[I].items()]
            self.ui.propertiesList.addTopLevelItems(items)
            
            items = [QTreeWidgetItem([i[0], i[1] % i[2]]) for i in self.window().items()]
            self.ui.propertiesList.addTopLevelItems(items)
            
            for x in xrange(len(peaks)):
                self.ui.propertiesList.addTopLevelItem(QTreeWidgetItem(["Harmonic no. %d" % (x +2), "%.6f dB" % peaks[x][2]]))
       
        self.redrawPlotsST()
        
    def updateTT(self, *args, **kwargs):
        I = int(self.ui.freqBar.value())
        self.ui.propertiesList.clear() 
        
        if self.signals[I].nsamples > 0  :
            items = [QTreeWidgetItem([i[0], i[1] % i[2]]) for i in self.signals[I].items()]
            self.ui.propertiesList.addTopLevelItems(items)
       
        self.redrawPlotsTT()
    
    ############################################################################
    ## Open file
    ############################################################################
    def slotOpenfile(self):
        fileName = str(QFileDialog.getOpenFileName(self, caption = "Open file", filter = "*.txt"))
        
        if fileName != "": 
            self.loadSignal(fileName)
    
    def loadSignal(self, fileName):
        print "Opening", fileName, len(fileName)
        self.signal = self.modes[self.mode][1](*readFile(fileName)) 
        self.update()
        
        
        
# scrivere la funzione update
# - deve creare self.signals utilizzando la catena selezionata e i dati letti dalla ui, e solamente dalla ui
# - se riceve True come parametro, allora carica self.signals
# - fa comunque il refresh della ui

# collegare la funzione update al pulsante update per fare il fetch dei dati, se ha senso farlo

# sistemare il grafico che mostra tutto
# precalcolare il possibile
# determinare quando usare ST o TT
# finire =) 

