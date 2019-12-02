import thorpy
from ressources.constantes import *

class Gui:
    """ Gui : déclare une interface graphique"""

    def __init__(self):
        thorpy.set_theme("human")
        # Liste contenant tous les éléments du Menu
        self.elements = []
        self.generateMenu()
        self.setStyle()

    def generateMenu(self):
        """initialise les éléments du menu"""

        # Génère pour chaque paramètre une box contenant le nom du paramètre et son slider associé et les ajoute à la liste elements
        self.generateSliders()

        # Pour les paramètres flottants, on arrondit le pas du slider à 1 décimale
        for slider in self.sliders.values():
            slider._round_decimals = 1

        # Boutton Quitter
        self.quitButton = thorpy.make_button("Quit", func=thorpy.functions.quit_func())
        self.elements.append(self.quitButton)

        # Regroupement de tous les éléments dans une box
        thorpy.style.DEF_COLOR = BLACK
        self.box = thorpy.Box(elements=self.elements, size=DIM_MENU)

        # Regroupement de la box dans un menu (même s'il n'y en a qu'un)
        self.menu = thorpy.Menu(self.box)

    def generateSliders(self):
        """generateSliders : génère des sliders à partir des paramètres déclarés dans parameters.default{}"""
        self.sliders = {}
        self.titles = []
        for name,k in parameters.default.items():
            # On génère les titres des paramètres avec la méthode OneLineText de Thorpy
            self.titles.append(thorpy.OneLineText(name))
            # On génère les sliders avec la méthode SliderX de Thorpy
            min = k[0]
            init = k[1]
            max = k[2]
            type = k[3]
            self.sliders[name] = thorpy.SliderX(length=DIM_SLIDER_X, limvals=(min, max), text="", initial_value=init, type_=type)
            # On crée une box composée du titre du paramètre et du slider associé et on stocke le tout dans la liste éléments
            self.elements.append(thorpy.Box(elements=[self.titles[-1], self.sliders[name]], size=DIM_SLIDER_BOX))

    def setStyle(self):
        # Box principale
        self.box.set_main_color(BLACK)

        # Boxs
        for box in self.elements:
            box.set_main_color(BLACK)

        # Titres
        for title in self.titles:
            self.setFontStyle(title, FONT_COLOR, FONT_SIZE, FONT)

        # Sliders
        for slider in self.sliders.values():
            # slider.get_slider()._height = 1
            slider.get_dragger().set_main_color(WHITE)
            slider.get_dragger().set_size(DIM_SLIDER_DRAGGER)
            slider.get_slider().set_main_color(WHITE)
            slider.get_slider().set_size((slider.get_slider().get_size()[0],DIM_SLIDER_Y))
            self.setFontStyle(slider._value_element, FONT_COLOR, FONT_SIZE, FONT)

        # Boutton Quitter
        # self.quitButton.set_main_color(BLACK)
        self.setFontStyle(self.quitButton, FONT_COLOR, FONT_SIZE, FONT)
        self.quitButton.set_font_color_hover(WHITE)

    def setFontStyle(self, element, font_color, font_size, font):
        element.set_font_color(font_color)
        element.set_font_size(font_size)
        element.set_font(font)

    def update(self):
        """update : met à jour les paramètres et les visuels à chaque tick"""
        self.updateValues()
        self.box.blit()
        self.box.update()

    def updateValues(self):
        """updateValues : met à jour les valeurs des paramètres dans parametres.actual avec la méthode parametres.set()"""
        for name, slider in self.sliders.items():
            parameters.set(name, slider.get_value())
