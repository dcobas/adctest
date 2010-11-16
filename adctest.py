
# requirements: wxwindows.

import wx
from controller import Controller

app = wx.App(False)
Controller(app)
app.MainLoop()


