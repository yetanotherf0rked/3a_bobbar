import os
import sys

from PyQt5.QtWidgets import QApplication
import qdarkstyle

from view.Mainwindow import MainWindow

# To center the window
os.environ["SDL_VIDEO_CENTERED"] = "1"

app = QApplication(sys.argv)
mainwindow = MainWindow()
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
mainwindow.show()
app.exec_()