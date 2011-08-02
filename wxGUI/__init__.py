__author__="federico"
__date__ ="$Jul 11, 2011 5:22:02 PM$"

import wxversion

# We need at least version 2.8 
wxversion.ensureMinimal('2.8')

def start():
    import wx
    import Controller

    # Create an application
    app = wx.App(False)

    # Create our controller and bind it to the app
    controller = Controller.Controller(app)

    # Start the main loop
    app.MainLoop()

