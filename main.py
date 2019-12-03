import os
from controller import *
from view.Choice import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


# Affiche la fenêtre au centre
os.environ["SDL_VIDEO_CENTERED"] = "1"



class Prems(QMainWindow, Ui_MainWindow):

    def __init__(self):

        QMainWindow.__init__(self)
        self.setupUi(self)

    def normal(self):
        controller = Controller()


app = QApplication(sys.argv)

window = Prems()
window.show()

app.exec()