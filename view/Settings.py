from PyQt5 import QtWidgets, QtCore

from view.ui_Settings import Ui_Settings

import ressources.config


class SettingsWindow(QtWidgets.QWidget, Ui_Settings):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.config = ressources.config.para
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setEnabled(False)
        self.initial_Config()
        self.setWindowTitle("Settings")

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

    def update_Config(self):
        self.config.show_Minimap = self.show_Minimap.isChecked()
        self.config.show_Perception = self.show_Perception.isChecked()
        self.config.show_Bord_Case = self.show_Bord_Case.isChecked()
        self.config.show_Nature = self.show_Nature.isChecked()
        self.config.show_Food_ProgressBar = self.show_Food_ProgressBar.isChecked()
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
        
        self.config.g_animation=self.animationY.isChecked()
        

        self.config.g_updated=True

    def gshow(self):
        self.update_graph()
        self.config.show_graph = True
        
    
    
