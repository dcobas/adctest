# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="federico"
__date__ ="$Jul 8, 2011 4:42:35 PM$"

import wx
from wx.lib.pubsub import Publisher as pub

class WindowParameter(wx.Panel):
    def __init__(self, parent, name, window):
        wx.Panel.__init__(self, parent)

        self.label = wx.StaticText(self, -1, "%s:" % name)
        self.spin = wx.SpinCtrl(self, -1, "1", wx.DefaultPosition, (100,30))

        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.Add(self.label, 0.5, wx.EXPAND)
        self.vsizer.Add(self.spin, 0.5, wx.EXPAND)
        self.SetSizer(vsizer)

    def get(self):
        return self.spin.GetValue()

        
