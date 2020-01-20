import os
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
import qdarkstyle

import ressources.config
from controller import *
from view.Choice import *

# Affiche la fenêtre au centre
os.environ["SDL_VIDEO_CENTERED"] = "1"


class Prems(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.config = ressources.config.para

    def normal(self):
        self.update_Config()
        Controller(simul=self.Day_Box.value(), bar=self.progressBar)

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



app = QApplication(sys.argv)

window = Prems()
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
window.show()

app.exec()
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
