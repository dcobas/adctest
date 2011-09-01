# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'source.ui'
#
# Created: Fri Aug 26 10:00:05 2011
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
        Dialog.resize(256, 232)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setFrameShape(QtGui.QFrame.NoFrame)
        self.label.setFrameShadow(QtGui.QFrame.Raised)
        self.label.setScaledContents(True)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.synth = QtGui.QRadioButton(Dialog)
        self.synth.setObjectName(_fromUtf8("synth"))
        self.verticalLayout.addWidget(self.synth)
        self.file = QtGui.QRadioButton(Dialog)
        self.file.setObjectName(_fromUtf8("file"))
        self.verticalLayout.addWidget(self.file)
        self.fc = QtGui.QRadioButton(Dialog)
        self.fc.setChecked(True)
        self.fc.setObjectName(_fromUtf8("fc"))
        self.verticalLayout.addWidget(self.fc)
        self.adc = QtGui.QRadioButton(Dialog)
        self.adc.setObjectName(_fromUtf8("adc"))
        self.verticalLayout.addWidget(self.adc)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Data Source", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Select a data source; the program will adapt to your choiche.", None, QtGui.QApplication.UnicodeUTF8))
        self.synth.setText(QtGui.QApplication.translate("Dialog", "Synthetic data", None, QtGui.QApplication.UnicodeUTF8))
        self.file.setText(QtGui.QApplication.translate("Dialog", "Read from file", None, QtGui.QApplication.UnicodeUTF8))
        self.fc.setText(QtGui.QApplication.translate("Dialog", "Full chain", None, QtGui.QApplication.UnicodeUTF8))
        self.adc.setText(QtGui.QApplication.translate("Dialog", "ADC only", None, QtGui.QApplication.UnicodeUTF8))

