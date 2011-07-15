import wx
from wx.lib.pubsub import Publisher as pub

from Model import Model
from View import View

class Controller:
    """ a 'middleman' between the View (visual aspects) and the Model (information) of the application.
        It ensures decoupling between both.
    """
    def __init__(self, app):
        # initialize the model and view
        # * The model handles all the data, and signal-related operations
        # * The view handles all the data visualization
        self.model = Model()
        self.view = View()

        # subscribe to messages sent by the view
        pub.subscribe(self.parse_file, "FILE PATH CHANGED")
        pub.subscribe(self.reprocess_fft, "FFT CONTROLS CHANGED")
        
        # subscribe to messages sent by the model
        pub.subscribe(self.signal_changed, "SIGNAL CHANGED")
        pub.subscribe(self.signal_changed, "FFT CHANGED")

        self.view.Show()
        
    def parse_file(self, message):
        """
        Handles "FILE PATH CHANGED" messages, send by the View. It tells the model to parse a new file.
        message.data should contain the path of the new file
        """
        #try:
        self.model.parse_file(message.data)
          
        #except Exception as exception:
        #    self.view.show_exception('Error reading file', 'The following error happened while reading the file:\n%s' % str(exception))
        #    raise exception
        
    def reprocess_fft(self, message):
        """
        Handler "FFT CONTROLS CHANGED" messages from the View. It tells the model to re-process the fft.
        message.data should contain the array [window, slices, max_peaks]
        """
        self.model.reprocess_fft(* message.data)
        
    
    def signal_changed(self, message):
        """
        Handles "SIGNAL CHANGED" messages sent by the model. Tells the view to update itself.
        message is ignored
        """
        self.view.signal_changed(self.model)
    
    def fft_changed(self, message):
        """
        Handles "FFT CHANGED" messages sent by the model. Tells the view to update itself.
        message is ignored
        """
        self.view.fft_changed(self.model)
    

        

