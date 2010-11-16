import wx
from wx.lib.pubsub import Publisher as pub

class Model:
    def __init__(self):
        self.myMoney = 0

    def addMoney(self, value):
        self.myMoney += value
        #now tell anyone who cares that the value has been changed
        pub.sendMessage("MONEY CHANGED", self.myMoney)

    def removeMoney(self, value):
        self.myMoney -= value
        #now tell anyone who cares that the value has been changed
        pub.sendMessage("MONEY CHANGED", self.myMoney)

