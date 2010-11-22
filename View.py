import wx
from wx.lib.pubsub import Publisher as pub

import os.path

import Plot # for graphs

class Tab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        bdr = wx.BoxSizer(wx.VERTICAL)
        self.padding = wx.BoxSizer(wx.VERTICAL)
        bdr.Add(self.padding, 1, wx.EXPAND|wx.ALL, 15)
        self.SetSizer(bdr)


class Tab1(Tab):
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
    
    def signal_changed(self, model):
        self.signal_plot.update(model.data)
    
    def send_path_changed_message(self, evt=None):
        pub.sendMessage("FILE PATH CHANGED", self.path_ctrl.GetValue())

    def open_dialog(self, evt=None):
        
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
        self.max_INL_label.SetLabel("Max INL: %d %%" % round(model.max_INL * 100, 0))
        self.max_DNL_label.SetLabel("Max DNL: %d %%" % round(model.max_DNL * 100, 0))
        self.INL_plot.update(model.INL)
        self.DNL_plot.update(model.DNL)
        self.histogram_plot.update(model.histogram, model.ideal_histogram)


class Tab3(Tab):

    def __init__(self, parent):
        Tab.__init__(self, parent)  
        
        
class View(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Main View")
        
        self.SetMinSize(wx.Size(800, 600))

        notebook = wx.Notebook(self)

        self.tab1 = Tab1(notebook)
        self.tab2 = Tab2(notebook)
        self.tab3 = Tab3(notebook)
        notebook.AddPage(self.tab1, "Signal") 
        notebook.AddPage(self.tab2, "INL / DNL / Histogram")
        notebook.AddPage(self.tab3, "FFT / Spectral Analysis")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)
        self.Fit()    

    def show_exception(self, title, message):
        dlg = wx.MessageDialog(self, message, title, wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
    
    def signal_changed(self, model):
        self.tab1.signal_changed(model)
        self.tab2.signal_changed(model)
        # TODO: add the same form tab2 and tab3, and implement the changes
        
    
    

