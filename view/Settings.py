from PyQt5 import QtWidgets, QtCore

from view.ui_Settings import Ui_Settings

from math import exp, log

import ressources.config


class SettingsWindow(QtWidgets.QWidget, Ui_Settings):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.config = ressources.config.para
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setEnabled(False)
        self.initial_Config()
        self.setWindowTitle("Settings")

    def initial_Config(self):
        self.show_Minimap.setChecked(self.config.show_Minimap)
        self.show_Perception.setChecked(self.config.show_Perception)
        self.show_Bord_Case.setChecked(self.config.show_Bord_Case)
        self.show_Nature.setChecked(self.config.show_Nature)
        self.show_Food_ProgressBar.setChecked(self.config.show_Food_ProgressBar)

    def update_Config(self):
        self.config.show_Minimap = self.show_Minimap.isChecked()
        self.config.show_Perception = self.show_Perception.isChecked()
        self.config.show_Bord_Case = self.show_Bord_Case.isChecked()
        self.config.show_Nature = self.show_Nature.isChecked()
        self.config.show_Food_ProgressBar = self.show_Food_ProgressBar.isChecked()


        """
        MOVE = 0
        BRAIN = 1

        add=lambda x,y: x+y
        sou=lambda x,y: x-y
        mul=lambda x,y: x+y
        div=lambda x,y: x/y

        def formule_consommation(type):
            #data = [principale, formule0, c1, c2, c3, formule1, d1, d2, d3]
            # c1 * f0(c2*b) ^ c3 {+, -, x, / en fonction de principale} d1 * f0(d2*b) ^ d3 
            
            if type == MOVE:
                p0, f0, c1, c2, c3, f1, d1, d2, d3 = config.
            elif type == BRAIN:
                p0, f0, c1, c2, c3, f1, d1, d2, d3 = config.
            else:
                print("formule_consommation: error type")
                return lambda x, y:0

            return lambda x, y:p0((c1*f0(c2*x))**c3, (d1*f1(d2*y))**d3)"""
        add = lambda x, y: x+y
        sou = lambda x, y: x-y
        mul = lambda x, y: x*y
        div = lambda x, y: x/y

        velocity_function = [lambda x,y: exp(x*y), lambda x,y:log(abs(x*y) + 1), pow][self.move_function0.currentIndex()]
        velocity_transform = lambda x: self.move_coeff0.value()*velocity_function(x, self.move_coeff1.value())

        main_operation = [add, sou, mul, div][self.move_function1.currentIndex()]

        mass_function = [lambda x,y: exp(x*y), lambda x,y:log(abs(x*y) + 1), pow][self.move_function2.currentIndex()]
        mass_transform = lambda x: self.move_coeff2.value()*mass_function(x, self.move_coeff3.value())

        self.config.move_consommation = lambda velocity, mass: main_operation(velocity_transform(velocity), mass_transform(mass))

    def gshow(self):
        pass

    def gshow(self):
        pass