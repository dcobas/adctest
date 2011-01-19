import wx
from wx.lib.pubsub import Publisher as pub

import os.path

import Plot # for graphs

from FFTSignal import FFTSignal # so we can use FFTSignal.WINDOW_TYPES

class Tab(wx.Panel):
    """ Superclass of all 'main panels' (accesible via the 3 different tabs) in the application.
        It defines a sizer called 'self.padding' that can be used to have a uniform 15-pixels
        border around the contents of all elements in each panel.
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        bdr = wx.BoxSizer(wx.VERTICAL)
        self.padding = wx.BoxSizer(wx.VERTICAL)
        bdr.Add(self.padding, 1, wx.EXPAND|wx.ALL, 15)
        self.SetSizer(bdr)


class Tab1(Tab):
    """ The 'signal loading panel'.
        It contains some basic controls and buttons for loading and displaying signals.
    """
    def __init__(self, parent):
        Tab.__init__(self, parent)
        
        # buttons / controls
        path_label = wx.StaticText(self, -1, "Choose a signal file:")
        self.path_ctrl = wx.TextCtrl(self)
        self.open_button = wx.Button(self, -1, "...", wx.DefaultPosition, wx.Size(30,30))
        self.parse_button = wx.Button(self, -1, "Parse file", wx.DefaultPosition, wx.Size(120,30))
        
        # matplotlib canvas
        self.signal_plot = Plot.Signal(self)
        
        # Bind actions to the two buttons
        self.open_button.Bind(wx.EVT_BUTTON, self.open_dialog)
        self.parse_button.Bind(wx.EVT_BUTTON, self.send_path_changed_message)
        
        # sizer for the textbox and buttons
        ctrls_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ctrls_sizer.Add(self.path_ctrl, 1, wx.EXPAND)
        ctrls_sizer.Add(self.open_button, 0, wx.EXPAND)
        ctrls_sizer.Add(self.parse_button, 0, wx.EXPAND)

        self.padding.Add(path_label, 0, wx.EXPAND)
        self.padding.Add(ctrls_sizer, 0, wx.EXPAND)
        self.padding.Add(self.signal_plot, 1, wx.EXPAND)

        # jdgc: pa abreviar
        self.path_ctrl.SetValue('/home/dcobas/projects/adctest/samples/complex.txt')
        self.send_path_changed_message()
    
    def signal_changed(self, model):
        """ Encodes what has to be done when a new signal has been loaded (the plot has to be updated)
        """
        self.signal_plot.update(model.data)
    
    def send_path_changed_message(self, evt=None):
        """ Sends a message to the Controller saying that the file path has been changed and it's ready to be reloaded.
            Called right after using the '...' button and choosing a file, and also when pressing the 'Parse file' button.
        """
        pub.sendMessage("FILE PATH CHANGED", self.path_ctrl.GetValue())

    def open_dialog(self, evt=None):
        """ Shows and controls the File Opening dialog """
        
        prevPath = self.path_ctrl.GetValue()
        
        if len(prevPath) > 0:
           defaultDir = os.path.dirname(prevPath)
        else:
           defaultDir = os.getcwd()
        
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=defaultDir, 
            defaultFile="",
            wildcard="All files (*.*)|*.*",
            style=wx.OPEN
            )

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # Parse the data.
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.path_ctrl.SetValue(path)
            self.send_path_changed_message()
        dlg.Destroy()
        
class Tab2(Tab):
    """ The 'INL / DNL / Histogram' panel.
        It contains the INL, DNL and Histogram graphs, as well as a couple labels displaying the Max INL and DNL.
    """

    def __init__(self, parent):
        Tab.__init__(self, parent)
        
        # buttons / controls
        self.max_INL_label = wx.StaticText(self, -1, "Max INL: 0%")
        self.max_DNL_label = wx.StaticText(self, -1, "Max DNL: 0%")

        # plots
        self.INL_plot = Plot.DNL(self)
        self.DNL_plot = Plot.INL(self)
        self.histogram_plot = Plot.Histogram(self)
        
        # Put label on top of INL graph
        INL_sizer = wx.BoxSizer(wx.VERTICAL)
        INL_sizer.Add(self.max_INL_label, 0, wx.EXPAND)
        INL_sizer.Add(self.INL_plot, 1, wx.EXPAND)
        
        # Put label on top of DNL graph
        DNL_sizer = wx.BoxSizer(wx.VERTICAL)
        DNL_sizer.Add(self.max_DNL_label, 0, wx.EXPAND)
        DNL_sizer.Add(self.DNL_plot, 1, wx.EXPAND)
        
        # Put INL to the left and DNL to the right
        INLDNL_sizer = wx.BoxSizer(wx.HORIZONTAL)
        INLDNL_sizer.Add(INL_sizer, 1, wx.EXPAND)
        INLDNL_sizer.Add(DNL_sizer, 1, wx.EXPAND)
        
        # Put INL/DNL on the top, Histogram to the bottom
        self.padding.Add(INLDNL_sizer, 1, wx.EXPAND)
        self.padding.Add(self.histogram_plot, 1, wx.EXPAND)
    
    def signal_changed(self, model):
        """ Encodes what has to be done when a new signal has been loaded (update all the plots and labels)
        """

        self.max_INL_label.SetLabel("Max INL: %d%%" % round(model.max_INL * 100, 0))
        self.max_DNL_label.SetLabel("Max DNL: %d%%" % round(model.max_DNL * 100, 0))
        self.INL_plot.update(model.INL)
        self.DNL_plot.update(model.DNL)
        self.histogram_plot.update(model.histogram, model.ideal_histogram)


class Tab3(Tab):
    """ The 'FFT' panel.
        It contains the FFT graph, as well as several numeric values.
    """
    def __init__(self, parent):
        Tab.__init__(self, parent)  
        
        # Controls
        window_label = wx.StaticText( self, -1, "Window:")
        self.window_ctrl = wx.ComboBox( self, 500, FFTSignal.WINDOW_TYPES[1], wx.DefaultPosition, (120,30), 
            FFTSignal.WINDOW_TYPES,
            wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT
        )
        
        slices_label = wx.StaticText(self, -1, "Slices:")
        self.slices_ctrl = wx.SpinCtrl(self, -1, "1", wx.DefaultPosition, (100,30))
        self.slices_ctrl.SetRange(1,10)
        
        max_peaks_label = wx.StaticText(self, -1, "Max peaks:")
        self.max_peaks_ctrl = wx.SpinCtrl(self, -1, "5", wx.DefaultPosition, (100,30))
        self.max_peaks_ctrl.SetRange(1,10)
        
        # Control bindings
        self.Bind(wx.EVT_SPINCTRL, self.send_fft_controls_changed_message, self.slices_ctrl)
        self.Bind(wx.EVT_SPINCTRL, self.send_fft_controls_changed_message, self.max_peaks_ctrl)
        self.Bind(wx.EVT_COMBOBOX, self.send_fft_controls_changed_message, self.window_ctrl)
        
        # Plot
        self.fft_plot = Plot.FFT(self)
        
        # SFDR, THD, SINAD, SNR, Noise floor, Process Gain 'static' labels (titles)
        SFDR_label = wx.StaticText(self, -1, "SFDR:")
        THD_label = wx.StaticText(self, -1, "THD:")
        SINAD_label = wx.StaticText(self, -1, "SINAD:")
        SNR_label = wx.StaticText(self, -1, "SNR:")
        noise_floor_label = wx.StaticText(self, -1, "Noise Floor:")
        process_gain_label = wx.StaticText(self, -1, "Process Gain:")
        
        # SFDR, THD, SINAD, SNR, Noise floor, Process Gain 'dynamic' labels (values)
        self.SFDR_label = wx.StaticText(self, -1, "0", wx.DefaultPosition, (50,30) )
        self.THD_label = wx.StaticText(self, -1, "0", wx.DefaultPosition, (50,30))
        self.SINAD_label = wx.StaticText(self, -1, "0", wx.DefaultPosition, (50,30))
        self.SNR_label = wx.StaticText(self, -1, "0", wx.DefaultPosition, (50,30))
        self.noise_floor_label = wx.StaticText(self, -1, "0", wx.DefaultPosition, (50,30))
        self.process_gain_label = wx.StaticText(self, -1, "0", wx.DefaultPosition, (50,30))
        
        # Put control labels to the left, controls to the right
        grid_sizer = wx.GridSizer(9, 2, 2, 2)  # rows, cols, vgap, hgap

        grid_sizer.AddMany([
            (window_label, 0),       (self.window_ctrl, 0, wx.ALIGN_RIGHT),
            (slices_label, 0),       (self.slices_ctrl, 0, wx.ALIGN_RIGHT),
            (max_peaks_label, 0),    (self.max_peaks_ctrl, 0, wx.ALIGN_RIGHT),
            
             # separator
            ((50,30)),               ((50,30)),
            
            (SFDR_label, 0),         (self.SFDR_label, 0),
            (THD_label, 0),          (self.THD_label, 0),
            (SINAD_label, 0),        (self.SINAD_label, 0),
            (SNR_label, 0),          (self.SNR_label, 0),
            (noise_floor_label, 0),  (self.noise_floor_label, 0),
            (process_gain_label, 0), (self.process_gain_label, 0)
        ])
        
        # Put the grid inside a vertical sizer so it doesn't scale vertically
        grid_container_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_container_sizer.Add(grid_sizer, 0, wx.EXPAND)
        
        # Put plot to the left of the grid sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(grid_container_sizer, 1)
        sizer.Add(self.fft_plot, 2, wx.EXPAND)
        
        self.padding.Add(sizer, 1, wx.EXPAND)
    
    def send_fft_controls_changed_message(self, evt):
        """ Sends a message to the Controller saying that the fft controls have been changed.
            Called whenever one of the controls is changed.
            Evt is ignored.
        """
        message = [self.window_ctrl.GetValue(), self.slices_ctrl.GetValue(), self.max_peaks_ctrl.GetValue()]
        pub.sendMessage("FFT CONTROLS CHANGED", message)
     
    def fft_changed(self, model):
        """ Encodes what has to be done when a new signal has been loaded or the fft controls have changed
            (on this tab, update the plot and labels)
        """
        self.fft_plot.update(model.fft, model.harmonic_peaks)
        self.SFDR_label.SetLabel(str(model.SFDR))
        self.THD_label.SetLabel(str(model.THD))
        self.SINAD_label.SetLabel(str(model.SINAD))
        self.SNR_label.SetLabel(str(model.SNR))
        self.noise_floor_label.SetLabel(str(model.noise_floor))
        self.process_gain_label.SetLabel(str(model.process_gain))
        
class View(wx.Frame):
    """ Contains the visual information - how the different windows, buttons, etc look and work.
        It doesn't perform any actions over the information (the Model) directly. Instead, it sends
        messages that are captured by the Controller, which in turn invokes methods on the model.
        This kind of decoupling facilitates making visual changes without affecting the underlying logic.
    """

    def __init__(self):
        wx.Frame.__init__(self, None, title="Main View")
        
        self.SetMinSize(wx.Size(800, 600))

        # Create the 3 tabs
        notebook = wx.Notebook(self)
        self.tab1 = Tab1(notebook)
        self.tab2 = Tab2(notebook)
        self.tab3 = Tab3(notebook)
        notebook.AddPage(self.tab1, "Signal") 
        notebook.AddPage(self.tab2, "INL / DNL / Histogram")
        notebook.AddPage(self.tab3, "FFT / Spectral Analysis")

        # add a sizer that contains all the panes/tabs of the application (so they resize appropiately)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)
        
        # auto-fit the window to the minimum required by the graphs contained on it.
        self.Fit()    

    def show_exception(self, title, message):
        """ Shows a message dialog announcing that an error has ocurred. Currently it only shows if there's an 
            issue while parsing a signal definition file
        """
        dlg = wx.MessageDialog(self, message, title, wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
    
    def signal_changed(self, model):
        """ Controls what happens when a new signal definition file is loaded (the views have to be refreshed)
        """
        self.tab1.signal_changed(model)
        self.tab2.signal_changed(model)
        self.fft_changed(model)

    def fft_changed(self, model):
        self.tab3.fft_changed(model)
        
    
    

