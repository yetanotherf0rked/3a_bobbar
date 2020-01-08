# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Choice.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 252, 161, 71))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(540, 250, 161, 71))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 20, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.Day_Box = QtWidgets.QSpinBox(self.centralwidget)
        self.Day_Box.setGeometry(QtCore.QRect(350, 130, 101, 31))
        self.Day_Box.setMinimum(1)
        self.Day_Box.setMaximum(100000)
        self.Day_Box.setObjectName("Day_Box")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(330, 90, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(0, 530, 791, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.show_Minimap = QtWidgets.QCheckBox(self.centralwidget)
        self.show_Minimap.setGeometry(QtCore.QRect(50, 390, 85, 21))
        self.show_Minimap.setChecked(False)
        self.show_Minimap.setObjectName("show_Minimap")
        self.affichage = QtWidgets.QCheckBox(self.centralwidget)
        self.affichage.setGeometry(QtCore.QRect(50, 420, 85, 21))
        self.affichage.setChecked(False)
        self.affichage.setObjectName("affichage")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.normal)
        self.pushButton_2.clicked.connect(MainWindow.close)
        self.progressBar.valueChanged['int'].connect(MainWindow.barMax)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Normal"))
        self.pushButton_2.setText(_translate("MainWindow", "Game of BoB"))
        self.label.setText(_translate("MainWindow", "BOB BAR"))
        self.label_2.setText(_translate("MainWindow", "Jour de départ"))
        self.show_Minimap.setText(_translate("MainWindow", "Minimap"))
        self.affichage.setText(_translate("MainWindow", "Affichage"))

