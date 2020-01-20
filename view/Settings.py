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
        Settings.resize(400, 300)
        self.pushButton = QtWidgets.QPushButton(Settings)
        self.pushButton.setGeometry(QtCore.QRect(160, 120, 80, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Settings)
        self.pushButton.clicked.connect(Settings.close)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Form"))
        self.pushButton.setText(_translate("Settings", "PushButton"))

