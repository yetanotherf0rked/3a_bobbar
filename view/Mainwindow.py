from threading import Thread

from PyQt5 import QtWidgets

import ressources.config
from controller import Controller
from view.Settings import SettingsWindow
from view.ui_Mainwindow import Ui_Form


class MainWindow(QtWidgets.QWidget, Ui_Form):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.config = ressources.config.para
        self.settings = SettingsWindow()
        self.setWindowTitle("Projet BobBar")
        self.initial_Config()

    def normal(self):
        self.update_Config()
        self.settings.show()
        self._thread = Thread(target=Controller,
                              args=(self.Day_Box.value(),self.progressBar,self.settings))
        self._thread.start()

    def barMax(self):
        if self.progressBar.value() == 100:
            self.close()


    def update_Config(self):
        self.config.historique = self.historique.isChecked()
        self.config.family_Reproduction = self.family_Reproduction.isChecked()
        self.config.family_Agression = self.family_Agression.isChecked()
        self.config.affichage = self.affichage.isChecked()
        self.config.TAILLE = self.TAILLE.value()
        self.config.show_graph_simul = self.show_grpah.isChecked()
        self.config.NB_POP = self.NB_POP.value()
        self.config.NB_FOOD = self.NB_FOOD.value()
        self.config.TICK_DAY=self.TICK_DAY.value()

        self.config.MUT_MASSE=self.mut_mass.value()
        self.config.MUT_VELOCITY=self.mut_velocity.value()
        self.config.MUT_MEMORY=self.mut_memory.value()
        self.config.MUT_PERCEPT=self.mut_perception.value()
       

    def activate_button(self):  
        self.historique.setEnabled(self.affichage.isChecked())


    def update_dayBox(self):
       self.show_grpah.setEnabled((self.Day_Box.value()!=1))
       print(self.Day_Box.value())

    def initial_Config(self):
        self.affichage.setChecked(self.config.affichage)
        self.activate_button()
        self.update_dayBox()
        if self.affichage.isChecked():
            self.historique.setChecked(self.config.historique)

        self.family_Reproduction.setChecked(self.config.family_Reproduction)
        self.family_Agression.setChecked(self.config.family_Agression)
        self.TAILLE.setValue(self.config.TAILLE)
        
        self.NB_POP.setValue(self.config.NB_POP)
        self.NB_FOOD.setValue(self.config.NB_FOOD)
        self.TICK_DAY.setValue(self.config.TICK_DAY)

        self.mut_mass.setValue(self.config.MUT_MASSE)
        self.mut_mass.setRange(0,5)
        self.mut_mass.setSingleStep(0.1)
        self.mut_velocity.setValue(self.config.MUT_VELOCITY)
        self.mut_velocity.setSingleStep(0.1)
        self.mut_velocity.setRange(0,5)
        self.mut_memory.setValue(self.config.MUT_MEMORY)
        self.mut_memory.setSingleStep(0.1)
        self.mut_memory.setRange(0,2)
        self.mut_perception.setValue(self.config.MUT_PERCEPT)
        self.mut_perception.setSingleStep(1)
        self.mut_perception.setRange(0,5)

        self.REPRO.setChecked(self.config.REPRO)
        self.PARTH.setChecked(self.config.PARTH)

