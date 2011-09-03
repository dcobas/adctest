__author__ = "Federico Asara"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Federico Asara", "Juan David Gonzalez Cobas"]
__license__ = "GPL2"
__version__ = "1.0.0"
__maintainer__ = "Federico Asara"
__email__ = "federico.asara@gmail.com"
__status__ = "Production"

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import PAGE
from PAGE.Utilities import *
import Selector

from numpy import *
from PyQt4.Qwt5 import QwtPlotGrid  

#FIXME: pressing tab while editing crashes everything

class ModuleSelector(QDialog):
    names = {'waveforms':0, 'generators':1, 'adcs':2}
    decisionTable = (PAGE.waveforms, PAGE.generators, PAGE.adcs)
    
    def __init__(self, parent = None, kind = 0):
        if type(kind) is str:
            kind = self.names[kind]
        
        QDialog.__init__(self, parent)
        
        self.ui =  Selector.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.table = self.decisionTable[kind]
        
        self.mods = [[self.table[i].name, str(i)] for i in range(len(self.table))]
        self.modc = [[(j, i.target._parameters[j]) for j in i.target._parameters] for i in self.table]
        
        items = [QTreeWidgetItem(i) for i in self.mods]
        self.ui.modules.addTopLevelItems(items)
        
        self.ui.modules.itemSelectionChanged.connect(self.slotUpdateConf)
        self.ui.modulesConfig.itemDoubleClicked.connect(self.slotEditParameter)
        
        self.dele = QItemDelegate()
        self.ui.modulesConfig.setItemDelegate(self.dele)
        self.dele.closeEditor.connect(self.slotCloseEditor)

    
    def slotCloseEditor(self, editor, *args, **kwargs):
        self.ui.modulesConfig.closePersistentEditor(*self.edItem)
        
        
    
    def slotEditParameter(self, item, column, *args, **kwargs):
        self.edItem = item, 1
        
        # we don't always need to edit
        key = str(item.text(2))
        index = int(self.ui.modules.currentItem().text(1))
        target = self.table[index].target
        params = dict(target._parameters)
        
        if type(params[key][3]) is str:
            if params[key][3] == 'file':
                fileName = str(QFileDialog.getOpenFileName(self, caption = "Select device", directory = '/dev', filter = "*"))
                if fileName != "": 
                    item.setText(1, filename)
                
                return 

        
        self.ui.modulesConfig.openPersistentEditor(*self.edItem)
        
    
    def generatePrefs(self):
        index = int(self.ui.modules.currentItem().text(1))
        target = self.table[index].target
        
        params = dict(target._parameters)
        output = {}
        
        lim = self.ui.modulesConfig.topLevelItemCount()
        i = 0
        
        temp = self.ui.modulesConfig.topLevelItem(0)
        
        while (temp is not None and temp != 0 ):
            key = str(temp.text(2))
            value = str(temp.text(1))
            # name = str(temp.text(0))
            
            ttt = params[key]
            output[key] = ttt[3](value) if (ttt[3] is not str and ttt[3] != 'file') else value
            
            i += 1
            temp = self.ui.modulesConfig.topLevelItem(i)
        
        
        return target, output
    
    def slotUpdateConf(self, *args, **kwargs):
        s = self.ui.modules.currentItem()
        i = self.ui.modules.indexFromItem(s).row()
        
        temp = self.modc[i]
        self.ui.modulesConfig.clear()
        for i in temp:
            y = QTreeWidgetItem([i[1][0], str(i[1][2]), i[0]],  Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
            self.ui.modulesConfig.addTopLevelItem(y)
        

def test():
    import sys
    import PyQt4.QtCore
    import PyQt4.QtGui
    
    # Create a Qt application 
    app = PyQt4.QtGui.QApplication(sys.argv)
    
    iii = []
    for i in range(3):
        mw = ModuleSelector(kind = i)
        mw.show()
        iii.append(mw)
    
    # Enter Qt application main loop
    app.exec_()
    
    for i in iii:
        print i.generatePrefs()

if __name__ == '__main__':
    test()
