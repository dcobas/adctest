__author__ = "Federico Asara"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Federico Asara", "Juan David Gonzalez Cobas"]
__license__ = "GPL2"
__version__ = "1.0.0"
__maintainer__ = "Federico Asara"
__email__ = "federico.asara@gmail.com"
__status__ = "Production"

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

