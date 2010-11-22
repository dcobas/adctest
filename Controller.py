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

        # subscribe to all "FILE PATH CHANGED" messages from the View
        pub.subscribe(self.parse_file, "FILE PATH CHANGED")
        
        # subscribe to all "SIGNAL CHANGED" messages from the Model
        pub.subscribe(self.signal_changed, "SIGNAL CHANGED")

        self.view.Show()
        
    def parse_file(self, message):
        """
        This method is the handler for "FILE PATH CHANGED" messages, which pubsub will call as messages are sent from the model.
        """
        #try:
        self.model.parse_file(message.data)
          
        #except Exception as exception:
        #    self.view.show_exception('Error reading file', 'The following error happened while reading the file:\n%s' % str(exception))
    
    def signal_changed(self, message):
        """
        This method is the handler for "SIGNAL CHANGED" messages, which pubsub will call as messages are sent from the model.
        """
        self.view.signal_changed(self.model)

