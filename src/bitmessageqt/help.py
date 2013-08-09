# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'help.ui'
#
# Created: Fri Aug  9 16:54:32 2013
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_helpDialog(object):
    def setupUi(self, helpDialog):
        helpDialog.setObjectName(_fromUtf8("helpDialog"))
        helpDialog.resize(335, 96)
        self.formLayout = QtGui.QFormLayout(helpDialog)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelHelpURI = QtGui.QLabel(helpDialog)
        self.labelHelpURI.setOpenExternalLinks(True)
        self.labelHelpURI.setObjectName(_fromUtf8("labelHelpURI"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelHelpURI)
        self.label = QtGui.QLabel(helpDialog)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout.setItem(2, QtGui.QFormLayout.LabelRole, spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(helpDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.buttonBox)

        self.retranslateUi(helpDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), helpDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), helpDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(helpDialog)

    def retranslateUi(self, helpDialog):
        helpDialog.setWindowTitle(_translate("helpDialog", "Help", None))
        self.labelHelpURI.setText(_translate("helpDialog", "<a href=\"http://Bitmessage.org/wiki/PyBitmessage_Help\">http://Bitmessage.org/wiki/PyBitmessage_Help</a>", None))
        self.label.setText(_translate("helpDialog", "As Bitmessage is a collaborative project, help can be found online in the Bitmessage Wiki:", None))

