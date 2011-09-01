# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selector.ui'
#
# Created: Thu Aug 25 15:05:30 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(734, 409)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.modules = QtGui.QTreeWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.modules.sizePolicy().hasHeightForWidth())
        self.modules.setSizePolicy(sizePolicy)
        self.modules.setObjectName(_fromUtf8("modules"))
        self.modules.header().setVisible(False)
        self.verticalLayout.addWidget(self.modules)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.modulesConfig = QtGui.QTreeWidget(Dialog)
        self.modulesConfig.setColumnCount(2)
        self.modulesConfig.setObjectName(_fromUtf8("modulesConfig"))
        self.horizontalLayout.addWidget(self.modulesConfig)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Module selection", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Select a module:", None, QtGui.QApplication.UnicodeUTF8))
        self.modules.headerItem().setText(0, QtGui.QApplication.translate("Dialog", "Modules", None, QtGui.QApplication.UnicodeUTF8))
        self.modulesConfig.headerItem().setText(0, QtGui.QApplication.translate("Dialog", "Parameter", None, QtGui.QApplication.UnicodeUTF8))
        self.modulesConfig.headerItem().setText(1, QtGui.QApplication.translate("Dialog", "Value", None, QtGui.QApplication.UnicodeUTF8))

