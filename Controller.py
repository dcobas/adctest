# FIXME the following two lines raise an error
# import wxversion
# wxversion.ensureMinimal('2.8')
import wx
from wx.lib.pubsub import Publisher as pub

from Model import Model
from View import View

class Controller:
    def __init__(self, app):
        # initialize the model and view
        # * The model handles all the data, and signal-related operations
        # * The view handles all the data visualization
        self.model = Model()
        self.view = View()

        self.view.tab1.fileParseButton.Bind(wx.EVT_BUTTON, self.FilePathChanged)
        
        # subscribe to all "SIGNAL CHANGED" messages from the Model
        pub.subscribe(self.SignalChanged, "SIGNAL CHANGED")

        self.view.Show()
        
    def FilePathChanged(self, evt):
        """
        This method is the handler for "FILE PATH CHANGED" messages, which pubsub will call as messages are sent from the model.
        """
        try:
            self.model.parse_file(self.view.tab1.filePathCtrl.GetValue())
          
        except Exception as exception:
            self.view.ShowException('Error reading file', 'The following error happened while reading the file:\n%s' % str(exception))
            # ensure that the SIGNAL CHANGED event is raised no matter what. This will 'blank' the view, as the model has no data
            pub.sendMessage("SIGNAL CHANGED")
    
    def SignalChanged(self, message):
        """
        This method is the handler for "SIGNAL CHANGED" messages, which pubsub will call as messages are sent from the model.
        """
        self.view.SignalChanged(self.model)

