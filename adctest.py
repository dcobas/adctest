import wxversion

# We need at least version 2.8 
wxversion.ensureMinimal('2.8')

# We can start importing modules
import wx
import UI.Controller

# Create an application
app = wx.App(False)

# Create our controller and bind it to the app
controller = UI.Controller.Controller(app)

# Start the main loop
app.MainLoop()


