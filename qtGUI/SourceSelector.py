from PyQt4.QtCore import *
from PyQt4.QtGui import *

import PAGE
from PAGE.Utilities import *
import Source

from numpy import *
from PyQt4.Qwt5 import QwtPlotGrid  

#FIXME: pressing tab while editing crashes everything

class SourceSelector(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.ui =  Source.Ui_Dialog()
        self.ui.setupUi(self)
    
    def answer(self):
        if self.ui.synth.isChecked():
            return 'synth'
        elif self.ui.file.isChecked():
            return 'file'
        elif self.ui.fc.isChecked():
            return 'fc'
        elif self.ui.adc.isChecked():
            return 'adc'
    
def test():
    import sys
    import PyQt4.QtCore
    import PyQt4.QtGui
    
    # Create a Qt application 
    app = PyQt4.QtGui.QApplication(sys.argv)
    
    mw = ModuleSelector()
    mw.show()
    
    # Enter Qt application main loop
    app.exec_()

if __name__ == '__main__':
    test()
