# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="federico"
__date__ ="$Jul 8, 2011 3:48:20 PM$"
import wx
from wx.lib.pubsub import Publisher as pub

class SliceChooser(wx.Panel):
    def __init__(self, windows):
        wx.Panel.__init__(self, windows)

        self.slices_label = wx.StaticText(self, -1, "Slices:")
        self.slices_ctrl = wx.SpinCtrl(self, -1, "1", wx.DefaultPosition, (100,30))
        self.slices_ctrl.SetRange(1,10)

        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.Add(self.slices_label, 0.5, wx.EXPAND)
        self.vsizer.Add(self.slices_ctrl, 0.5, wx.EXPAND)

    def get(self):
        return self.slices_ctrl.Get_Value()