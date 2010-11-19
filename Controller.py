# FIXME the following two lines raise an error
# import wxversion
# wxversion.ensureMinimal('2.8')
import wx
from wx.lib.pubsub import Publisher as pub

from Model import Model
from View import View

class Controller:
    def __init__(self, app):
        self.model = Model()

        #set up the first frame which displays the current Model value
        self.view = View(None)
        #self.view.SetMoney(self.model.myMoney)
        
        self.view.tab1.fileParseButton.Bind(wx.EVT_BUTTON, self.ParseFile)

        #subscribe to all "SIGNAL CHANGED" messages from the Model
        pub.subscribe(self.FileLoaded, "FILE PATH CHANGED")
        pub.subscribe(self.SignalChanged, "SIGNAL CHANGED")

        self.view.Show()
        
    def ParseFile(self, evt):
        try:
            self.model.ParseFile(self.view.tab1.filePathCtrl.GetValue())
          
        except Exception as exception:
            pub.sendMessage("SIGNAL CHANGED")
            self.view.ShowException('Error reading file', 'The following error happened while reading the file:\n%s' % str(exception))
        
    def FileLoaded(self, message):
        """
        This method is the handler for "FILE PATH CHANGED" messages, which pubsub will call as messages are sent from the model.
        """
        self.ParseFile(None)
    
    def SignalChanged(self, message):
        """
        This method is the handler for "SIGNAL CHANGED" messages, which pubsub will call as messages are sent from the model.
        """
        self.view.SignalChanged(self.model)

