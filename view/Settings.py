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


    def update_consommation_label(self):
        add = lambda x, y: x+y
        sou = lambda x, y: x-y
        mul = lambda x, y: x*y
        div = lambda x, y: x/y

        # Update de la fonction de consommation de l'énergie lors du mouvement

        velocity_function = [lambda x,y: exp(x*y), lambda x,y:log(abs(x*y) + 1), pow][self.move_function0.currentIndex()]
        velocity_transform = lambda x: self.move_coeff0.value()*velocity_function(x, self.move_coeff1.value())

        move_main_operation = [add, sou, mul, div][self.move_function1.currentIndex()]

        mass_function = [lambda x,y: exp(x*y), lambda x,y:log(abs(x*y) + 1), pow][self.move_function2.currentIndex()]
        mass_transform = lambda x: self.move_coeff2.value()*mass_function(x, self.move_coeff3.value())

        self.config.move_consommation = lambda velocity, mass: move_main_operation(velocity_transform(velocity), mass_transform(mass))

        # Update de la fonction de consommation de l'énergie lors de l'utilisation du cerveau

        perception_function = [lambda x,y: exp(x*y), lambda x,y:log(abs(x*y) + 1), pow][self.brain_function0.currentIndex()]
        perception_transform = lambda x: self.brain_coeff0.value()*perception_function(x, self.brain_coeff1.value())

        brain_main_operation = [add, sou, mul, div][self.brain_function1.currentIndex()]

        memory_points_function = [lambda x,y: exp(x*y), lambda x,y:log(abs(x*y) + 1), pow][self.brain_function2.currentIndex()]
        memory_points_transform = lambda x: self.brain_coeff2.value()*memory_points_function(x, self.brain_coeff3.value())

        self.config.brain_consommation = lambda perception, memory_points: brain_main_operation(perception_transform(perception), memory_points_transform(memory_points))

        self.brain_label.setText("mettre la bonne formule (brain)")

        self.move_label.setText("mettre la bonne formule (move)")

    def update_Config(self):
        self.config.show_Minimap = self.show_Minimap.isChecked()
        self.config.show_Perception = self.show_Perception.isChecked()
        self.config.show_Bord_Case = self.show_Bord_Case.isChecked()
        self.config.show_Nature = self.show_Nature.isChecked()
        self.config.show_Food_ProgressBar = self.show_Food_ProgressBar.isChecked()

        

    def gshow(self):
        pass

    def gshow(self):
        pass