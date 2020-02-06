from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

from view.ui_Settings import Ui_Settings

from math import exp, log

import ressources.config


class SettingsWindow(QtWidgets.QWidget, Ui_Settings):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.config = ressources.config.para
        self.setupUi(self)
        rx = QRegExp("[0-9()+\-*/.]{0,}")
        self.move_lineEdit.setValidator(QRegExpValidator(rx))
        self.brain_lineEdit.setValidator(QRegExpValidator(rx))
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setEnabled(False)
        self.initial_Config()
        self.setWindowTitle("Settings")
        # self.update_consommation_label()

    def restart(self):
        self.config.restart = True

    def initial_Config(self):
        self.show_Minimap.setChecked(self.config.show_Minimap)
        self.show_Perception.setChecked(self.config.show_Perception)
        self.show_Bord_Case.setChecked(self.config.show_Bord_Case)
        self.show_Nature.setChecked(self.config.show_Nature)
        self.show_Food_ProgressBar.setChecked(self.config.show_Food_ProgressBar)
        self.animationY.setChecked(self.config.g_animation)
        self.animationN.setChecked(not self.config.g_animation)
        self.abcissa_tick.setChecked(True)
        self.gpop.setChecked(True)
        self.update_rate.setRange(1,200)
        self.update_rate.setValue(self.config.g_update_rate)
        if self.config.weather == "Sandstorm":
            self.Sandstorm.setChecked(True)
        elif self.config.weather == "Sun":
            self.Sun.setChecked(True)
        elif self.config.weather == "Hail":
            self.Hail.setChecked(True)
        elif self.config.weather == "Fogue":
            self.Fogue.setChecked(True)
        elif  self.config.weather == "Rain":
            self.Rain.setChecked(True)


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


        brain_c0 = str(self.brain_coeff0.value())
        brain_c1 = str(self.brain_coeff1.value())
        brain_c2 = str(self.brain_coeff2.value())
        brain_c3 = str(self.brain_coeff3.value())

        brain_main = ["+", "-", "*", "/"][self.brain_function1.currentIndex()]

        brain_f0 = ["exp({}*{})", "log(1 + |{}*{}|)", "{}^{}"][self.brain_function0.currentIndex()].format("perception", brain_c1)

        brain_f2 = ["exp({}*{})", "log(1 + |{}*{}|)", "{}^{}"][self.brain_function2.currentIndex()].format("memory_points", brain_c3)

        self.brain_label.setText("bob.energy_brain = {}*{} {} {}*{}".format(brain_c0, brain_f0, brain_main, brain_c2, brain_f2))

        move_c0 = str(self.move_coeff0.value())
        move_c1 = str(self.move_coeff1.value())
        move_c2 = str(self.move_coeff2.value())
        move_c3 = str(self.move_coeff3.value())

        move_main = ["+", "-", "*", "/"][self.move_function1.currentIndex()]

        move_f0 = ["exp({}*{})", "log(1 + |{}*{}|)", "{}^{}"][self.move_function0.currentIndex()].format("velocity", move_c1)

        move_f2 = ["exp({}*{})", "log(1 + |{}*{}|)", "{}^{}"][self.move_function2.currentIndex()].format("masse", move_c3)

        self.move_label.setText("bob.energy_move = {}*{} {} {}*{}".format(move_c0, move_f0, move_main, move_c2, move_f2))

        self.config.change_consommation = True



    def update_Config(self):
        self.config.show_Minimap = self.show_Minimap.isChecked()
        self.config.show_Perception = self.show_Perception.isChecked()
        self.config.show_Bord_Case = self.show_Bord_Case.isChecked()
        self.config.show_Nature = self.show_Nature.isChecked()
        self.config.show_Food_ProgressBar = self.show_Food_ProgressBar.isChecked()
        if self.Sandstorm.isChecked():
            self.config.weather = "Sandstorm"
        elif self.Sun.isChecked():
            self.config.weather = "Sun"
        elif self.Hail.isChecked():
            self.config.weather = "Hail"
        elif self.Fogue.isChecked():
            self.config.weather = "Fogue"
        elif self.Rain.isChecked():
            self.config.weather = "Rain"
        self.update_graph()
        


    def update_graph(self):
        x = ""
        if self.abcissa_tick.isChecked() :
            x="ticks"
        else:
            x="days"
        self.config.g_parameters={
                            'x':x,
                            'pop':self.gpop.isChecked(),
                            'mass':self.mass_av.isChecked(),
                            'velocity':self.velo_av.isChecked(),
                            'memory':self.memory_av.isChecked(),
                            'perception':self.perc_av.isChecked(),
                            'food':self.gfood.isChecked(),
                            'age':self.age_av.isChecked()}
        self.config.g_update_rate = self.update_rate.value()
        self.config.g_animation=self.animationY.isChecked()
        

        self.config.g_updated=True

    def gshow(self):
        self.update_graph()
        self.config.show_graph = True
        
    
    
