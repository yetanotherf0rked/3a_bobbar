import pygame
import thorpy
from ressources.constantes import *

class Gui:
    """ Gui : déclare une interface graphique"""
    def __init__(self):
        """ init : crée le menu"""
        # Déclaration d'une liste d'éléments
        self.elements = []
        # Déclaration d'un Boutton Quitter
        self.quitButton = thorpy.make_button("Quit", func=thorpy.functions.quit_func)
        # Déclaration d'un Dictionnaire de Sliders
        self.sliders = {}
        self.generateSliders()
        # On met les éléments (sliders puis boutton) dans la liste elements
        self.elements = [slider for slider in self.sliders.values()]
        self.elements.append(self.quitButton)
        # Regroupement des éléments dans une box
        self.box = thorpy.Box(elements=self.elements)
        # Regroupement des box dans un menu
        self.menu = thorpy.Menu(self.box)

    def generateSliders(self):
        """generateSliders : génère des sliders à partir des paramètres déclarés dans parameters.default{}"""
        for name,k in parameters.default.items():
            min = k[0]
            init = k[1]
            max = k[2]
            type = k[3]
            self.sliders[name] = thorpy.SliderX(length=100, limvals=(min, max), text=name, initial_value=init, type_=type)

    def update(self):
        """update : met à jour les paramètres et les visuels à chaque tick"""
        self.updateValues()
        self.box.blit()
        self.box.update()

    def updateValues(self):
        """updateValues : met à jour les valeurs des paramètres dans parametres.actual avec la méthode parametres.set()"""
        for name, slider in self.sliders.items():
            parameters.set(name, slider.get_value())