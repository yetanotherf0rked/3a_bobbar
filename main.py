import os
from controller import *
from model import Config
from view.Choice import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import model.config


# Affiche la fenêtre au centre
os.environ["SDL_VIDEO_CENTERED"] = "1"


class Prems(QMainWindow, Ui_MainWindow):

    def __init__(self):

        QMainWindow.__init__(self)
        self.setupUi(self)
        self.config = model.config.para

    def normal(self):
        self.update_Config()
        Controller(simul=self.Day_Box.value(), bar = self.progressBar)

    def barMax(self):
        if self.progressBar.value() == 100:
            self.close()

    def update_Config(self):
        if self.show_Minimap.isChecked():
            self.config.show_Minimap = True
        if self.affichage.isChecked():
            self.config.affichage = True

app = QApplication(sys.argv)

window = Prems()
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
