import os
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
import qdarkstyle

import ressources.config
from controller import *
from view.Choice import *
from view.Settings import *
from threading import Thread

# Affiche la fenêtre au centre
os.environ["SDL_VIDEO_CENTERED"] = "1"


class MainWindow(QtWidgets.QWidget, Ui_Form):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.config = ressources.config.para
        self.settings = SettingsWindow()

    def normal(self):
        self.update_Config()
        self.settings.show()
        # self.controller = Controller(self.Day_Box.value(), self.progressBar,settings = self.settings)
        self._thread = Thread(target=Controller,
                              args=(self.Day_Box.value(),self.progressBar,self.settings))
        self._thread.start()

    def barMax(self):
        if self.progressBar.value() == 100:
            self.close()


    def update_Config(self):
        self.config.show_Minimap = self.show_Minimap.isChecked()
        self.config.fullscreen = self.fullscreen.isChecked()
        self.config.show_Perception = self.show_Perception.isChecked()
        self.config.show_Bord_Case = self.show_Bord_Case.isChecked()
        self.config.historique = self.historique.isChecked()
        self.config.family_Reproduction = self.family_Reproduction.isChecked()
        self.config.family_Agression = self.family_Agression.isChecked()
        self.config.affichage = self.affichage.isChecked()
        self.config.TAILLE = self.taille.intValue()
        self.config.show_graph = self.show_grpah.isChecked()

    def activate_button(self):
        self.show_Minimap.setEnabled(self.affichage.isChecked())
        self.fullscreen.setEnabled(self.affichage.isChecked())
        self.show_Perception.setEnabled(self.affichage.isChecked())
        self.show_Bord_Case.setEnabled(self.affichage.isChecked())
        self.historique.setEnabled(self.affichage.isChecked())

class SettingsWindow(QtWidgets.QWidget, Ui_Settings):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

app = QApplication(sys.argv)
mainwindow = MainWindow()
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
mainwindow.show()
app.exec_()
# Controller()

# #execution sans argument -> affichage vue
# # python main.py [option..]
# #  a : affichage
# #  d : debug
# #  s : simulation de n tour passsé à la suite pour stats
# if len(sys.argv)>1 :
#     controller = Controller(sys.argv[1], int(sys.argv[2]) if len(sys.argv)>2 else 1000)
# else :
#      controller = Controller()
