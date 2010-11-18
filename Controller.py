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

        #set up the second frame which allows the user to modify the Model's value
        #self.view.add.Bind(wx.EVT_BUTTON, self.AddMoney)
        #self.view.remove.Bind(wx.EVT_BUTTON, self.RemoveMoney)
        #subscribe to all "MONEY CHANGED" messages from the Model
        #to subscribe to ALL messages (topics), omit the second argument below
        pub.subscribe(self.MoneyChanged, "MONEY CHANGED")

        self.view.Show()
    def ParseFile(self, evt):
        try:
            self.model.ParseFile(self.view.tab1.filePathCtrl.GetValue())
          
        except Exception as exception:
            self.view.ShowException('Error reading file', 'The following error happened while reading the file:\n%s' % str(exception))
        
        

    def RemoveMoney(self, evt):
        self.model.removeMoney(10)

    def MoneyChanged(self, message):
        """
        This method is the handler for "MONEY CHANGED" messages,
        which pubsub will call as messages are sent from the model.

        We already know the topic is "MONEY CHANGED", but if we
        didn't, message.topic would tell us.
        """
        self.view.SetMoney(message.data)

