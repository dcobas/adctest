import wxversion
wxversion.ensureMinimal('2.6')
import wx

from Controller import Controller

app = wx.App(False)
controller = Controller(app)
app.MainLoop()


