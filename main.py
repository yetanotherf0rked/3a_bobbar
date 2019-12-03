import os
from controller import *
from Choice import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget


# Affiche la fenêtre au centre
os.environ["SDL_VIDEO_CENTERED"] = "1"
controller = Controller()

# class Prems(QMainWindow, Ui_MainWindow):
#
#     def __init__(self):
#
#         QMainWindow.__init__(self)
#         self.setupUi(self)
#
#
#
# app = QApplication(sys.argv)
#
# window = Prems()
# window.show()
#
# app.exec()