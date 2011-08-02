# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Thu Jul 28 16:47:53 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1036, 737)
        MainWindow.setAnimated(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1036, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuSignal = QtGui.QMenu(self.menubar)
        self.menuSignal.setObjectName(_fromUtf8("menuSignal"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockWidget = QtGui.QDockWidget(MainWindow)
        self.dockWidget.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidget.setObjectName(_fromUtf8("dockWidget"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label_3 = QtGui.QLabel(self.dockWidgetContents)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_5.addWidget(self.label_3)
        self.modeBox = QtGui.QComboBox(self.dockWidgetContents)
        self.modeBox.setEditable(False)
        self.modeBox.setObjectName(_fromUtf8("modeBox"))
        self.verticalLayout_5.addWidget(self.modeBox)
        self.singleToneBox1 = QtGui.QVBoxLayout()
        self.singleToneBox1.setObjectName(_fromUtf8("singleToneBox1"))
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setObjectName(_fromUtf8("label"))
        self.singleToneBox1.addWidget(self.label)
        self.windowBox = QtGui.QComboBox(self.dockWidgetContents)
        self.windowBox.setObjectName(_fromUtf8("windowBox"))
        self.singleToneBox1.addWidget(self.windowBox)
        self.verticalLayout_5.addLayout(self.singleToneBox1)
        self.singleToneBox2 = QtGui.QHBoxLayout()
        self.singleToneBox2.setObjectName(_fromUtf8("singleToneBox2"))
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.singleToneBox2.addWidget(self.label_2)
        self.peaksBox = QtGui.QSpinBox(self.dockWidgetContents)
        self.peaksBox.setMinimum(0)
        self.peaksBox.setMaximum(20)
        self.peaksBox.setProperty(_fromUtf8("value"), 5)
        self.peaksBox.setObjectName(_fromUtf8("peaksBox"))
        self.singleToneBox2.addWidget(self.peaksBox)
        self.verticalLayout_5.addLayout(self.singleToneBox2)
        self.propertiesList = QtGui.QTreeWidget(self.dockWidgetContents)
        self.propertiesList.setAlternatingRowColors(True)
        self.propertiesList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.propertiesList.setUniformRowHeights(True)
        self.propertiesList.setAnimated(True)
        self.propertiesList.setHeaderHidden(False)
        self.propertiesList.setColumnCount(2)
        self.propertiesList.setObjectName(_fromUtf8("propertiesList"))
        self.propertiesList.headerItem().setText(1, _fromUtf8("Value"))
        self.propertiesList.header().setCascadingSectionResizes(True)
        self.propertiesList.header().setDefaultSectionSize(180)
        self.propertiesList.header().setHighlightSections(True)
        self.propertiesList.header().setMinimumSectionSize(50)
        self.propertiesList.header().setStretchLastSection(True)
        self.verticalLayout_5.addWidget(self.propertiesList)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setIconVisibleInMenu(True)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.menuSignal.addAction(self.actionOpen)
        self.menuSignal.addSeparator()
        self.menuSignal.addAction(self.actionQuit)
        self.menubar.addAction(self.menuSignal.menuAction())
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionQuit)
        self.label_3.setBuddy(self.modeBox)
        self.label.setBuddy(self.windowBox)
        self.label_2.setBuddy(self.peaksBox)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "ADC Characterization Toolkit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSignal.setTitle(QtGui.QApplication.translate("MainWindow", "Signal", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "&Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "&Window Function", None, QtGui.QApplication.UnicodeUTF8))
        self.windowBox.setStatusTip(QtGui.QApplication.translate("MainWindow", "Choose a signal window", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Ha&rmonics:", None, QtGui.QApplication.UnicodeUTF8))
        self.peaksBox.setStatusTip(QtGui.QApplication.translate("MainWindow", "How many harmonic peaks you want", None, QtGui.QApplication.UnicodeUTF8))
        self.peaksBox.setSuffix(QtGui.QApplication.translate("MainWindow", " peak(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.propertiesList.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Property", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open..", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
