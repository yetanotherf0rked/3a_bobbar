import thorpy
import pygame
from ressources.constantes import *

class Gui:
    """ Gui : initialise l'interface utilisateur"""

    def __init__(self, menuSurface):
        # Thème par défaut
        thorpy.set_theme("human")

        # Liste contenant tous les éléments du Menu
        self.elements = []

        # Génère les éléments du Menu
        self.generateMenu()

        # On modifie le style des éléments
        self.setStyle()

        # On définit menuSurface comme la surface de l'interface GUI
        self.assignSurface(self.menu, menuSurface)

        # On charge et affiche le logo
        self.logo = pygame.image.load(image_LOGO).convert_alpha()
        menuSurface.blit(self.logo, (0, 0))

        # Puis on affiche le menu
        self.box.set_topleft(POS_PARAMETRES)
        self.update()

    def generateMenu(self):
        """initialise les éléments du menu"""

        # Day, Tick & Population
        self.setStateBox()

        # Génère pour chaque paramètre son slider associé
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

    def update(self):
        """update : met à jour les paramètres et les visuels à chaque tick"""
        self.box.update()
        self.updateValues()
        self.box.blit()
        self.box.update()

    def setStateBox(self):
        """Affiche l'état de la simulation (days, ticks, population) et les outils graphiques pour se déplacer
        de tick en tick et de day en day"""

        # Style
        thorpy.set_theme("human")
        thorpy.style.FONT_COLOR = WHITE
        thorpy.style.DEF_COLOR = BLACK

        # Elements Textuels
        dayText = thorpy.make_text("Day", FONT_SIZE, WHITE)
        tickText = thorpy.make_text("Tick", FONT_SIZE, WHITE)
        popText = thorpy.make_text("Population", FONT_SIZE, WHITE)
        dayNumber = thorpy.make_text("0", FONT_SIZE, WHITE)
        tickNumber = thorpy.make_text("00", FONT_SIZE, WHITE)
        popNumber = thorpy.make_text("00", FONT_SIZE, WHITE)
        self.boxDayDisplay = thorpy.Box(elements=[dayText, dayNumber]) # size 100,50
        self.boxTickDisplay = thorpy.Box(elements=[tickText, tickNumber]) # size 100,50
        self.boxPopDisplay = thorpy.Box(elements=[popText, popNumber])

        # Boutons + et - pour contrôler les ticks dans le mode Pause
        buttonDayPlus = thorpy.make_button("+", func=self.buttonDayPlusPressed)
        buttonDayMinus = thorpy.make_button("-", func=self.buttonDayMinusPressed)
        buttonTickPlus = thorpy.make_button("+", func=self.buttonTickPlusPressed)
        buttonTickMinus = thorpy.make_button("-", func=self.buttonTickMinusPressed)

        # On les désactive pour l'instant
        buttonDayPlus.set_active(False)
        buttonDayMinus.set_active(False)
        buttonTickPlus.set_active(False)
        buttonTickMinus.set_active(False)

        # On resize les boutons
        buttonDayPlus.set_size(size=DIM_PLUSMINUSBUTTON)
        buttonDayMinus.set_size(size=DIM_PLUSMINUSBUTTON)
        buttonTickPlus.set_size(size=DIM_PLUSMINUSBUTTON)
        buttonTickMinus.set_size(size=DIM_PLUSMINUSBUTTON)

        # Style
        thorpy.set_theme("human")

        # On rassemble DAY et TICK horizontalement
        boxH = thorpy.make_group(elements=[buttonDayMinus, self.boxDayDisplay, buttonDayPlus,buttonTickMinus,
                                            self.boxTickDisplay, buttonTickPlus], mode="h")

        # On rassemble tout
        self.stateBox = thorpy.Box(elements=[boxH,self.boxPopDisplay], size=DIM_STATEBOX)

        # On rajoute la box finale dans la liste éléments
        self.elements.append(self.stateBox)

    def updateStateBox(self, day, tick, pop):
        # générer de nouveaux éléments textuels avec les nouvelles valeurs
        newPopElement = thorpy.make_text(str(pop), FONT_SIZE, WHITE)
        newTickElement = thorpy.make_text(str(tick % TICK_DAY), FONT_SIZE, WHITE)
        newDayElement = thorpy.make_text(str(day), FONT_SIZE, WHITE)

        # remplacer l'ancienne valeur
        self.boxDayDisplay.replace_element(self.boxDayDisplay.get_elements()[1], newDayElement)
        self.boxTickDisplay.replace_element(self.boxTickDisplay.get_elements()[1], newTickElement)
        self.boxPopDisplay.replace_element(self.boxPopDisplay.get_elements()[1], newPopElement)

        # Update
        self.stateBox.update()
        self.stateBox.blit()
        self.stateBox.update()

    def generateSliders(self):
        """ Génère des sliders à partir des paramètres déclarés dans parameters.default{}
            Vérifie si l'argument SHOW est bien égal à True avant de créer le slider"""
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
        """Modifie le style des éléments déjà déclarés"""
        # Box principale
        self.box.set_main_color(BLACK)

        # Boxs
        for box in self.elements:
            box.set_main_color(BLACK)

        # Titres
        for title in self.titles:
            self.setFontStyle(title, FONT_COLOR, FONT_SIZE, FONT)

        # De la personnalisation des Sliders : Un objet thorpy.SliderX est composé
        # - d'un élément textuel pour le titre (que l'on n'utilisera pas car difficilement personnalisable)
        # - d'un Slider(thorpy.SliderX.get_slider())
        # - d'un dragger (thorpy.SliderX.get_dragger())
        # - et d'un élément textuel pour la valeur (thorpy.SliderX._value_element)
        # Chaque attribut de ces constituants est personnalisble

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
        """Prend en argument un élément textuel et lui affecte une police (str),
        une couleur ((R,G,B)) et une taille (int)"""
        element.set_font_color(font_color)
        element.set_font_size(font_size)
        element.set_font(font)

    def assignSurface(self, mon_menu, ma_surface):
        """Très importante : assigne une surface aux éléments d'un menu"""
        for element in mon_menu.get_population():
            element.surface = ma_surface

    def updateValues(self):
        """updateValues : met à jour les valeurs des paramètres dans parametres.actual
        avec la méthode parametres.set()"""
        for name, slider in self.sliders.items():
            parameters.set(name, slider.get_value())

    def quitButtonPressed(self):
        """quitButtonPressed : appelée quand on clique sur le Bouton Quit"""
        self.guiQuit = True

    def pauseButtonPressed(self):
        """pauseButtonPressed : appelée quand on clique sur le Bouton Pause"""
        self.guiPause = not self.guiPause

    def buttonDayPlusPressed(self):
        pass

    def buttonDayMinusPressed(self):
        pass

    def buttonTickPlusPressed(self):
        pass

    def buttonTickMinusPressed(self):
        pass