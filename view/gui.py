import thorpy
import pygame
from ressources.constantes import *

class Gui:
    """ Gui : initialise l'interface utilisateur"""

    def __init__(self, menuSurface):
        thorpy.set_theme("human")
        # Liste contenant tous les éléments du Menu
        self.elements = []
        # Génère les éléments du Menu
        self.generateMenu()
        # Permet de modifier le style des éléments
        self.setStyle()
        # On définit menuSurface comme la surface de l'interface GUI
        self.assignSurface(self.menu, menuSurface)
        self.update()
        # On charge et affiche le logo
        self.logo = pygame.image.load(image_LOGO).convert_alpha()
        menuSurface.blit(self.logo, POS_LOGO)
        # Puis on affiche le menu
        self.box.set_topleft(POS_PARAMETRES)

    def generateMenu(self):
        """initialise les éléments du menu"""
        # Génère pour chaque paramètre une box contenant le nom du paramètre et son slider associé et les ajoute à
        # la liste elements
        self.generateSliders()

        # Boutton Quitter
        self.guiQuit = False
        self.quitButton = thorpy.make_button("Quit", func=self.quitButtonPressed)
        self.elements.append(self.quitButton)

        # Boutton Pause
        self.guiPause = False
        self.pauseButton = thorpy.make_button("Play/Pause", func=self.pauseButtonPressed)
        self.elements.append(self.pauseButton)

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
            if k[4]: # Si le paramètre SHOW est à TRUE
                # On génère les titres des paramètres avec la méthode OneLineText de Thorpy (on n'utilisera pas le champ
                # texte de SliderX car il est difficilement personnalisable)
                self.titles.append(thorpy.OneLineText(name))
                # On génère les sliders avec la méthode SliderX de Thorpy
                min = k[0]
                init = k[1]
                max = k[2]
                type = k[3]
                self.sliders[name] = thorpy.SliderX(length=DIM_SLIDER_X, limvals=(min, max), text="",
                                                    initial_value=init, type_=type)
                # Pour les paramètres flottants, on arrondit le pas du slider à 1 décimale
                self.sliders[name]._round_decimals = 1
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

        # Sliders : Un objet thorpy.SliderX est composé d'un élément textuel pour le titre (mis à "" car difficilement
        # personnalisable), d'un Slider(thorpy.SliderX.get_slider()), d'un dragger (thorpy.SliderX.get_dragger())
        # et d'un élément textuel pour la valeur (thorpy.SliderX._value_element)
        for slider in self.sliders.values():
            slider.get_dragger().set_main_color(WHITE)
            slider.get_dragger().set_size(DIM_DRAGGER)
            slider.get_slider().set_main_color(WHITE)
            slider.get_slider().set_size(DIM_SLIDER)
            self.setFontStyle(slider._value_element, FONT_COLOR, FONT_SIZE, FONT)

        # Boutton Quitter
        self.setFontStyle(self.quitButton, FONT_COLOR, FONT_SIZE, FONT)
        self.quitButton.set_font_color_hover(WHITE)

        # Boutton Pause
        self.setFontStyle(self.pauseButton, FONT_COLOR, FONT_SIZE, FONT)
        self.pauseButton.set_font_color_hover(WHITE)

    def setFontStyle(self, element, font_color, font_size, font):
        element.set_font_color(font_color)
        element.set_font_size(font_size)
        element.set_font(font)

    def assignSurface(self, mon_menu, ma_surface):
        for element in mon_menu.get_population():
            element.surface = ma_surface

    def update(self):
        """update : met à jour les paramètres et les visuels à chaque tick"""
        self.updateValues()
        self.box.blit()
        self.box.update()

    # def updateDayAndTick(self, menuSurface):
    #     self.i = 0
    #     # met à jour le day et le tick
    #     thorpy.set_theme("human")
    #     # Element textuel pour afficher le tick et le day
    #     self.dayAndTick = thorpy.make_text("Day: " + str(self.i) + "\nTick: " + str(self.i), FONT_SIZE, WHITE)
    #     self.i += 1
    #     self.boxDayAndTick = thorpy.Box(elements=[self.dayAndTick])
    #     self.menuDayAndTick = thorpy.Menu(self.boxDayAndTick)
    #     self.assignSurface(self.menuDayAndTick, menuSurface)
    #     self.box.set_topleft((0, 0))
    #     self.boxDayAndTick.blit()
    #     self.boxDayAndTick.update()


    def updateValues(self):
        """updateValues : met à jour les valeurs des paramètres dans parametres.actual avec la méthode parametres.set()"""
        for name, slider in self.sliders.items():
            parameters.set(name, slider.get_value())

    def quitButtonPressed(self):
        """quitButtonPressed : appelée quand on clique sur le Boutton Quit"""
        self.guiQuit = True

    def pauseButtonPressed(self):
        self.guiPause = not self.guiPause