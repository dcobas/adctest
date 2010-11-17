
# requirements: wxwindows.

import wx
from Controller import Controller

app = wx.App(False)
Controller(app)
app.MainLoop()


