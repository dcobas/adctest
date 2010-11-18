import wx
import ConfigParser
import string
from wx.lib.pubsub import Publisher as pub

class Model:
    def __init__(self):
        self.myMoney = 0
        
    def ParseFile(self, path):
      
      config = ConfigParser.RawConfigParser()

      config.read(path)
      
      nbits = config.getint('SIGNAL', 'nbits')
      rate = config.getint('SIGNAL', 'rate')
      dataString = config.get('SIGNAL', 'data').split('\n')
      data = map(string.atoi, dataString)
     
      print "nbits: %d" % nbits
      print "rate: %d" % rate
      print "data: "
      print data 

    def addMoney(self, value):
        self.myMoney += value
        #now tell anyone who cares that the value has been changed
        pub.sendMessage("MONEY CHANGED", self.myMoney)

    def removeMoney(self, value):
        self.myMoney -= value
        #now tell anyone who cares that the value has been changed
        pub.sendMessage("MONEY CHANGED", self.myMoney)

