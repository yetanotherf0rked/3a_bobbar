# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(300, 88, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(10, 550, 791, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(300, 230, 161, 71))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(280, 28, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.Day_Box = QtWidgets.QSpinBox(Form)
        self.Day_Box.setGeometry(QtCore.QRect(330, 138, 101, 31))
        self.Day_Box.setMinimum(1)
        self.Day_Box.setMaximum(100000)
        self.Day_Box.setObjectName("Day_Box")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 330, 351, 146))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.affichage = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.affichage.setFont(font)
        self.affichage.setChecked(False)
        self.affichage.setObjectName("affichage")
        self.gridLayout.addWidget(self.affichage, 0, 0, 1, 1)
        self.family_Reproduction = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.family_Reproduction.setFont(font)
        self.family_Reproduction.setChecked(False)
        self.family_Reproduction.setObjectName("family_Reproduction")
        self.gridLayout.addWidget(self.family_Reproduction, 1, 0, 1, 1)
        self.family_Agression = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.family_Agression.setFont(font)
        self.family_Agression.setChecked(False)
        self.family_Agression.setObjectName("family_Agression")
        self.gridLayout.addWidget(self.family_Agression, 2, 0, 1, 1)
        self.historique = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.historique.setFont(font)
        self.historique.setChecked(False)
        self.historique.setObjectName("historique")
        self.gridLayout.addWidget(self.historique, 0, 1, 1, 1)
        self.show_grpah = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.show_grpah.setFont(font)
        self.show_grpah.setChecked(False)
        self.show_grpah.setObjectName("show_grpah")
        self.gridLayout.addWidget(self.show_grpah, 1, 1, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(510, 250, 211, 71))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.TAILLE = QtWidgets.QSpinBox(self.layoutWidget1)
        self.TAILLE.setMinimum(1)
        self.TAILLE.setMaximum(100000)
        self.TAILLE.setObjectName("TAILLE")
        self.gridLayout_3.addWidget(self.TAILLE, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.horizontalSlider = QtWidgets.QSlider(self.layoutWidget1)
        self.horizontalSlider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.horizontalSlider.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.horizontalSlider.setMaximum(300)
        self.horizontalSlider.setPageStep(1)
        self.horizontalSlider.setProperty("value", 40)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setInvertedAppearance(False)
        self.horizontalSlider.setInvertedControls(False)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.horizontalSlider.setTickInterval(25)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout.addWidget(self.horizontalSlider)
        self.layoutWidget_2 = QtWidgets.QWidget(Form)
        self.layoutWidget_2.setGeometry(QtCore.QRect(510, 350, 211, 71))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)
        self.NB_POP = QtWidgets.QSpinBox(self.layoutWidget_2)
        self.NB_POP.setMinimum(1)
        self.NB_POP.setMaximum(100000)
        self.NB_POP.setObjectName("NB_POP")
        self.gridLayout_4.addWidget(self.NB_POP, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_4)
        self.horizontalSlider_2 = QtWidgets.QSlider(self.layoutWidget_2)
        self.horizontalSlider_2.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.horizontalSlider_2.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.horizontalSlider_2.setMaximum(300)
        self.horizontalSlider_2.setPageStep(1)
        self.horizontalSlider_2.setProperty("value", 40)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setInvertedAppearance(False)
        self.horizontalSlider_2.setInvertedControls(False)
        self.horizontalSlider_2.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.horizontalSlider_2.setTickInterval(25)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.verticalLayout_2.addWidget(self.horizontalSlider_2)
        self.layoutWidget_3 = QtWidgets.QWidget(Form)
        self.layoutWidget_3.setGeometry(QtCore.QRect(510, 450, 211, 71))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_5.addWidget(self.label_5, 0, 0, 1, 1)
        self.NB_FOOD = QtWidgets.QSpinBox(self.layoutWidget_3)
        self.NB_FOOD.setMinimum(1)
        self.NB_FOOD.setMaximum(100000)
        self.NB_FOOD.setObjectName("NB_FOOD")
        self.gridLayout_5.addWidget(self.NB_FOOD, 0, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_5)
        self.horizontalSlider_3 = QtWidgets.QSlider(self.layoutWidget_3)
        self.horizontalSlider_3.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.horizontalSlider_3.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.horizontalSlider_3.setMaximum(300)
        self.horizontalSlider_3.setPageStep(1)
        self.horizontalSlider_3.setProperty("value", 40)
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setInvertedAppearance(False)
        self.horizontalSlider_3.setInvertedControls(False)
        self.horizontalSlider_3.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.horizontalSlider_3.setTickInterval(25)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.verticalLayout_3.addWidget(self.horizontalSlider_3)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(450, 90, 351, 131))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.mut_mass = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.mut_mass.setObjectName("mut_mass")
        self.verticalLayout_4.addWidget(self.mut_mass)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.mut_velocity = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        self.mut_velocity.setObjectName("mut_velocity")
        self.verticalLayout_5.addWidget(self.mut_velocity)
        self.horizontalLayout.addWidget(self.groupBox_3)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.mut_memory = QtWidgets.QDoubleSpinBox(self.groupBox_5)
        self.mut_memory.setObjectName("mut_memory")
        self.verticalLayout_7.addWidget(self.mut_memory)
        self.horizontalLayout.addWidget(self.groupBox_5)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.mut_perception = QtWidgets.QDoubleSpinBox(self.groupBox_4)
        self.mut_perception.setObjectName("mut_perception")
        self.verticalLayout_6.addWidget(self.mut_perception)
        self.horizontalLayout.addWidget(self.groupBox_4)

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.normal)
        self.progressBar.valueChanged['int'].connect(Form.barMax)
        self.affichage.clicked.connect(Form.activate_button)
        self.horizontalSlider.valueChanged['int'].connect(self.TAILLE.setValue)
        self.TAILLE.valueChanged['int'].connect(self.horizontalSlider.setValue)
        self.horizontalSlider_2.valueChanged['int'].connect(self.NB_POP.setValue)
        self.NB_POP.valueChanged['int'].connect(self.horizontalSlider_2.setValue)
        self.horizontalSlider_3.valueChanged['int'].connect(self.NB_FOOD.setValue)
        self.NB_FOOD.valueChanged['int'].connect(self.horizontalSlider_3.setValue)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Jour de départ"))
        self.pushButton.setText(_translate("Form", "Lancer"))
        self.label.setText(_translate("Form", "BOB BAR"))
        self.affichage.setText(_translate("Form", "Affichage"))
        self.family_Reproduction.setText(_translate("Form", "Family Reproduction"))
        self.family_Agression.setText(_translate("Form", "Family Aggression"))
        self.historique.setText(_translate("Form", "Historique"))
        self.show_grpah.setText(_translate("Form", "Show Graph"))
        self.label_3.setText(_translate("Form", "Taille"))
        self.label_4.setText(_translate("Form", "Population"))
        self.label_5.setText(_translate("Form", "Food"))
        self.groupBox.setTitle(_translate("Form", "Mutation Rate"))
        self.groupBox_2.setTitle(_translate("Form", "Mass"))
        self.groupBox_3.setTitle(_translate("Form", "Velocity"))
        self.groupBox_5.setTitle(_translate("Form", "Memory"))
        self.groupBox_4.setTitle(_translate("Form", "Perception"))
