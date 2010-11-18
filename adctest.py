# FIXME the following two lines raise an error
# import wxversion
# wxversion.ensureMinimal('2.8')
import wx

from Controller import Controller

app = wx.App(False)
Controller(app)
app.MainLoop()


