from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

from view.ui_Settings import Ui_Settings

from math import exp, log, pow, sqrt

import ressources.config


class SettingsWindow(QtWidgets.QWidget, Ui_Settings):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.config = ressources.config.para
        self.setupUi(self)
        self.rx = QRegExp("(log|exp|pow|sqrt|masse|velocity|perception|memory|[0-9]|\\.|\\*|\\-|\\+|\\(|\\)|\\/|\\,)*")
        self.move_lineEdit.setValidator(QRegExpValidator(self.rx))
        self.brain_lineEdit.setValidator(QRegExpValidator(self.rx))
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setEnabled(False)
        self.initial_Config()
        self.setWindowTitle("Settings")

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

    def masse(self):
        if self.tab_7.isHidden():
            if self.test_lineEdit(self.move_lineEdit):
                self.move_lineEdit.setText(self.move_lineEdit.text()+"masse")
                self.move_lineEdit.setFocus()
        elif self.test_lineEdit(self.brain_lineEdit):
            self.brain_lineEdit.setText(self.brain_lineEdit.text()+"masse")
            self.brain_lineEdit.setFocus()

    def velocity(self):
        if self.tab_7.isHidden():
            if self.test_lineEdit(self.move_lineEdit):
                self.move_lineEdit.setText(self.move_lineEdit.text()+"velocity")
                self.move_lineEdit.setFocus()
        elif self.test_lineEdit(self.brain_lineEdit):
            self.brain_lineEdit.setText(self.brain_lineEdit.text()+"velocity")
            self.brain_lineEdit.setFocus()

    def perception(self):
        if self.tab_7.isHidden():
            if self.test_lineEdit(self.move_lineEdit):
                self.move_lineEdit.setText(self.move_lineEdit.text()+"perception")
                self.move_lineEdit.setFocus()
        elif self.test_lineEdit(self.brain_lineEdit):
            self.brain_lineEdit.setText(self.brain_lineEdit.text()+"perception")
            self.brain_lineEdit.setFocus()

    def memory(self):
        if self.tab_7.isHidden():
            if self.test_lineEdit(self.move_lineEdit):
                self.move_lineEdit.setText(self.move_lineEdit.text()+"memory")
                self.move_lineEdit.setFocus()
        elif self.test_lineEdit(self.brain_lineEdit):
            self.brain_lineEdit.setText(self.brain_lineEdit.text()+"memory")
            self.brain_lineEdit.setFocus()

    def sqrt_button(self):
        if self.tab_7.isHidden():
            if self.test_lineEdit(self.move_lineEdit):
                self.move_lineEdit.setText(self.move_lineEdit.text()+"sqrt()")
                self.move_lineEdit.setFocus()
        elif self.test_lineEdit(self.brain_lineEdit):
            self.brain_lineEdit.setText(self.brain_lineEdit.text()+"sqrt()")
            self.brain_lineEdit.setFocus()

    def exp_button(self):
        if self.tab_7.isHidden():
            if self.test_lineEdit(self.move_lineEdit):
                self.move_lineEdit.setText(self.move_lineEdit.text()+"exp()")
                self.move_lineEdit.setFocus()
        elif self.test_lineEdit(self.brain_lineEdit):
            self.brain_lineEdit.setText(self.brain_lineEdit.text()+"exp()")
            self.brain_lineEdit.setFocus()

    def pow_button(self):
        if self.tab_7.isHidden():
            if self.test_lineEdit(self.move_lineEdit):
                self.move_lineEdit.setText(self.move_lineEdit.text()+"pow()")
                self.move_lineEdit.setFocus()
        elif self.test_lineEdit(self.brain_lineEdit):
            self.brain_lineEdit.setText(self.brain_lineEdit.text()+"pow()")
            self.brain_lineEdit.setFocus()

    def log_button(self):
        if self.tab_7.isHidden():
            if self.test_lineEdit(self.move_lineEdit):
                self.move_lineEdit.setText(self.move_lineEdit.text()+"log()")
                self.move_lineEdit.setFocus()
        elif self.test_lineEdit(self.brain_lineEdit):
            self.brain_lineEdit.setText(self.brain_lineEdit.text()+"log()")
            self.brain_lineEdit.setFocus()

    def update_consommation_label(self):
        if self.tab_7.isHidden():
            exec("self.config.move_consommation = lambda velocity, masse:" + self.move_lineEdit.text())
            self.label_4.setText(self.move_lineEdit.text())
        else:
            exec("self.config.brain_consommation = lambda perception, memory:" + self.brain_lineEdit.text())
            self.label_3.setText(self.brain_lineEdit.text())
        self.config.change_consommation = True

    def test_lineEdit(self,lineEdit):
        text = lineEdit.text()
        if text =="":
            return True
        if text[-1] == "0" or text[-1] == "1" or text[-1] == "2" or text[-1] == "3" or text[-1] == "4" or text[-1] == "5" or text[-1] == "6" or text[-1] == "7" or text[-1] == "8" or text[-1] == "9" or text[-1] == "+" or text[-1] == "-" or text[-1] == "/" or text[-1] == "*" or text[-1] == ")" or text[-1] == "(":
            return True
        if text[-6:] == "memory" or text[-10:] == "perception" or text[-8:] == "velocity" or text[-5:] == "masse":
            return True
        return False

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
        
    
    
