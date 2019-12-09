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

# app.exec()
controller = Controller()

#execution sans argument -> affichage vue
# python main.py [option..]
#  a : affichage
#  d : debug
#  s : simulation de n tour passsé à la suite
if len(sys.argv)>1 :
    controller = Controller(sys.argv[1], int(sys.argv[2]) if len(sys.argv)>2 else 1000)
else :
     controller = Controller()