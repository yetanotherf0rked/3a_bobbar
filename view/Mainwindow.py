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
        self.config.TAILLE = self.taille.intValue()
        self.config.show_graph = self.show_grpah.isChecked()

    def activate_button(self):
        self.historique.setEnabled(self.affichage.isChecked())

    def initial_Config(self):
        self.affichage.setChecked(self.config.affichage)
        self.activate_button()
        if self.affichage.isChecked():
            self.historique.setChecked(self.config.historique)
        self.family_Reproduction.setChecked(self.config.family_Reproduction)
        self.family_Agression.setChecked(self.config.family_Agression)
        self.horizontalSlider.setValue(self.config.TAILLE)
        self.show_grpah.setChecked(self.config.show_graph)