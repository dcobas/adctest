#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="federico"
__date__ ="$Jul 15, 2011 2:20:38 PM$"
import wx, os
from wx.lib.pubsub import Publisher as pub


class FileChooser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # buttons / controls
        path_label = wx.StaticText(self, -1, "Choose a signal file:")
        self.path_ctrl = wx.TextCtrl(self)
        self.open_button = wx.Button(self, -1, "...", wx.DefaultPosition, wx.Size(30,30))
        self.parse_button = wx.Button(self, -1, "Parse file", wx.DefaultPosition, wx.Size(120,30))

        # Bind actions to the two buttons
        self.open_button.Bind(wx.EVT_BUTTON, self.open_dialog)
        self.parse_button.Bind(wx.EVT_BUTTON, self.send_path_changed_message)

        # sizer for the textbox and buttons
        ctrls_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ctrls_sizer.Add(self.path_ctrl, 1, wx.EXPAND)
        ctrls_sizer.Add(self.open_button, 0, wx.EXPAND)
        ctrls_sizer.Add(self.parse_button, 0, wx.EXPAND)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(path_label, 0.5, wx.EXPAND)
        vsizer.Add(ctrls_sizer, 0.5, wx.EXPAND)
        self.SetSizer(vsizer)

        # jdgc: pa abreviar
        # fasara: using os.path facilities
        defaultPath = os.path.join(os.getcwd(), 'samples', 'data.txt')
        self.path_ctrl.SetValue(defaultPath)
        self.send_path_changed_message()

    def send_path_changed_message(self, evt=None):
        """ Sends a message to the Controller saying that the file path has been changed and it's ready to be reloaded.
            Called right after using the '...' button and choosing a file, and also when pressing the 'Parse file' button.
        """
        pub.sendMessage("FILE PATH CHANGED", self.path_ctrl.GetValue())

    def open_dialog(self, evt=None):
        """ Shows and controls the File Opening dialog """

        prevPath = self.path_ctrl.GetValue()

        if len(prevPath) > 0:
           defaultDir = os.path.dirname(prevPath)
        else:
           defaultDir = os.getcwd()

        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=defaultDir,
            defaultFile="",
            wildcard="All files (*.*)|*.*",
            style=wx.OPEN
            )

        # Show the dialog and retrieve the user response. If it is the OK response,
        # Parse the data.
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.path_ctrl.SetValue(path)
            self.send_path_changed_message()
        dlg.Destroy()

