# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Settings.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(671, 703)
        self.show_Bord_Case = QtWidgets.QCheckBox(Settings)
        self.show_Bord_Case.setGeometry(QtCore.QRect(30, 40, 131, 21))
        self.show_Bord_Case.setObjectName("show_Bord_Case")
        self.show_Minimap = QtWidgets.QCheckBox(Settings)
        self.show_Minimap.setGeometry(QtCore.QRect(30, 60, 85, 21))
        self.show_Minimap.setObjectName("show_Minimap")
        self.checkBox_3 = QtWidgets.QCheckBox(Settings)
        self.checkBox_3.setGeometry(QtCore.QRect(30, 80, 85, 21))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(Settings)
        self.checkBox_4.setGeometry(QtCore.QRect(30, 100, 85, 21))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_5 = QtWidgets.QCheckBox(Settings)
        self.checkBox_5.setGeometry(QtCore.QRect(30, 120, 85, 21))
        self.checkBox_5.setObjectName("checkBox_5")
        self.buttonBox = QtWidgets.QDialogButtonBox(Settings)
        self.buttonBox.setGeometry(QtCore.QRect(250, 620, 166, 24))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Settings)
        self.buttonBox.rejected.connect(Settings.hide)
        self.buttonBox.accepted.connect(Settings.hide)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Form"))
        self.show_Bord_Case.setText(_translate("Settings", "Show Bord Case"))
        self.show_Minimap.setText(_translate("Settings", "Minimap"))
        self.checkBox_3.setText(_translate("Settings", "CheckBox"))
        self.checkBox_4.setText(_translate("Settings", "CheckBox"))
        self.checkBox_5.setText(_translate("Settings", "CheckBox"))

