import wx
from wx.lib.pubsub import Publisher as pub

class View(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Main View")

        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, label="My Money")
        ctrl = wx.TextCtrl(self)
        sizer.Add(text, 0, wx.EXPAND | wx.ALL)
        sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL)

        self.moneyCtrl = ctrl
        ctrl.SetEditable(False)
        
        self.add = wx.Button(self, label="Add Money")
        self.remove = wx.Button(self, label="Remove Money")
        sizer.Add(self.add, 0, wx.EXPAND | wx.ALL)
        sizer.Add(self.remove, 0, wx.EXPAND | wx.ALL)
        
        self.SetSizer(sizer)

    def SetMoney(self, money):
        self.moneyCtrl.SetValue(str(money))
