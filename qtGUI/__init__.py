__author__="Federico Asara"
__date__ ="$Jul 11, 2011 5:22:02 PM$"

def start():
    import sys
    import PyQt4.QtCore
    import PyQt4.QtGui
    import MainWindow
    
    # Create a Qt application 
    app = PyQt4.QtGui.QApplication(sys.argv)
    
    mw = MainWindow.MainWindow()
    mw.show()
    
    # Enter Qt application main loop
    app.exec_()

