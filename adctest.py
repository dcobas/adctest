import wxversion
wxversion.ensureMinimal('2.8')
import wx

from Controller import Controller

app = wx.App(False)
controller = Controller(app)
app.MainLoop()


