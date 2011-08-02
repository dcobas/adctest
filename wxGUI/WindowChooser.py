# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="federico"
__date__ ="$Jul 8, 2011 3:48:20 PM$"
import wx
from wx.lib.pubsub import Publisher as pub

from WindowParameter import WindowParameter

class WindowPicker(wx.Panel):
    def __init__(self, windows):
        wx.Panel.__init__(self, windows)

        # create a DropBox
        self.windowLabel = wx.StaticText( self, -1, "Window:")

        self.windows = windows
        self.allWindows  = windows.keys()
        self.currentWindow = self.allWindows[0]
        self.windowBox = wx.ComboBox(self, 500, self.currentWindow, wx.DefaultPosition, (120,30),
            allWindows, wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT )

        self.slices_label = wx.StaticText(self, -1, "Slices:")
        self.slices_ctrl = wx.SpinCtrl(self, -1, "1", wx.DefaultPosition, (100,30))
        self.slices_ctrl.SetRange(1,10)
        self.spinboxes = []

        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.Add(self.windowLabel, 0.5, wx.EXPAND)
        self.vsizer.Add(self.windowBox, 0.5, wx.EXPAND)
        self.vsizer.Add(self.windowBox, 0.5, wx.EXPAND)

        self.updateView()

    def updateView(self):
        if self.windowBox.GetValue() == self.currentWindow:
            return

        self.currentWindow = self.windowBox.GetValue()
        window = self.windows[self.currentWindow]

        # hide and show spinners accordingly
        for i in self.spinboxes:
            self.vsizer.Remove(i)

        self.spinboxes = [WindowParameter(self, i, window) for i in window.parameters]
        for i in self.spinboxes:
            self.vsizer.Add(i, 0.5, wx.EXPAND)
        

    def get(self):
        window = self.windows[self.currentWindow]
        parameters = [i.get() for i in self.spinboxes]

        return window, parameters