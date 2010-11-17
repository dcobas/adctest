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
        self.Bind(wx.EVT_BUTTON, self.OpenFileDialog, self.fileOpenButton)
               
        
        filePathControlsSizer = wx.BoxSizer(wx.HORIZONTAL)
        filePathControlsSizer.Add(self.filePathCtrl, 1, wx.EXPAND)
        filePathControlsSizer.Add(self.fileOpenButton, 0, wx.EXPAND)
        
        filePathSizer = wx.BoxSizer(wx.VERTICAL)
        filePathSizer.Add(filePathLabel, 0, wx.EXPAND)
        filePathSizer.Add(filePathControlsSizer, 0, wx.EXPAND)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(filePathSizer, 1, wx.EXPAND)
        
        self.padding.Add(sizer, 1, wx.EXPAND)

    def OpenFileDialog(self, evt):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard="All files (*.*)|*.*",
            style=wx.OPEN
            )

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print('Path selected: %s' % path)
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
    
    

