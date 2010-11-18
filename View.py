import wx
import os
from wx.lib.pubsub import Publisher as pub

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
        
        filePathLabel = wx.StaticText(self, -1, "Please choose a signal file")
        self.filePathCtrl = wx.TextCtrl(self)
        self.fileOpenButton = wx.Button(self, -1, "...", wx.DefaultPosition, wx.Size(30,30))
        self.fileParseButton = wx.Button(self, -1, "Go!", wx.DefaultPosition)
        self.fileOpenButton.Bind(wx.EVT_BUTTON, self.OpenFileDialog)
        
        # sizer for the textbox and button
        filePathCtrlsSizer = wx.BoxSizer(wx.HORIZONTAL)
        filePathCtrlsSizer.Add(self.filePathCtrl, 1, wx.EXPAND)
        filePathCtrlsSizer.Add(self.fileOpenButton, 0, wx.EXPAND)
        
        # sizer that aligns the Parse button to the right
        goButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        goButtonSizer.Add(self.fileParseButton, 0, wx.EXPAND)
        
        # sizer includes controls + label on top
        filePathSizer = wx.BoxSizer(wx.VERTICAL)
        filePathSizer.Add(filePathLabel, 0, wx.EXPAND)
        filePathSizer.Add(filePathCtrlsSizer, 0, wx.EXPAND)
        filePathSizer.Add(self.fileParseButton, 0, wx.ALIGN_CENTER )

        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(filePathSizer, 1, wx.EXPAND)
        
        self.padding.Add(sizer, 1, wx.EXPAND)

    def OpenFileDialog(self, evt):
        
        prevPath = self.filePathCtrl.GetValue()
        
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
            self.filePathCtrl.SetValue(path)
        dlg.Destroy()
    
    
        
class Tab2(Tab):

    def __init__(self, parent):
        Tab.__init__(self, parent)

class Tab3(Tab):

    def __init__(self, parent):
        Tab.__init__(self, parent)  
        
        
class View(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Main View")

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

    def ShowException(self, title, message):
        dlg = wx.MessageDialog(self, message, title, wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
    
    

