import thorpy
import pygame
from ressources.constantes import *
from .gradient import Gradient

class Gui:

    """ Gui : initialise l'interface utilisateur
        Les différents éléments (excepté le logo) sont stockés dans des objets thorpy.Box

        Hiérarchie des boxs :

        --- self.main_box : the father of all the boxes (affecté au menu self.main_menu, lui-même affecté à la surface menu_surface)
        ------ self.state_box : box verticale affichant l'état de la simulation (day, tick, pop) et les boutons + et -
        --------- boxH : box horizontale contenant les boutons +/1 et les états de day et tick
        ------------ button_day_minus
        ------------ button_day_plus
        ------------ button_tick_minus
        ------------ button_tick_plus
        ------------ self.box_day_display : contient deux éléments textuels : "Day" et sa valeur que l'on met à jour
        --------------- day_text
        --------------- day_number
        ------------ self.box_tick_display
        --------------- tick_text
        --------------- tick_number
        --------- self.box_pop_display
        ------------ pop_text
        ------------ pop_number
        ------ Box pour chaque paramètre
        --------- Titre du paramètre
        --------- Slider
        ------ Boutton Quitter
        ------ Boutton Pause
    """

    def __init__(self, menu_surface):
        # Thème par défaut
        thorpy.set_theme("human")

        # Génère les éléments du Menu
        self.generate_menu()

        # On modifie le style des éléments
        self.set_style()

        # On définit menu_surface comme la surface de l'interface GUI
        self.assign_surface(self.menu, menu_surface)

        # On charge et affiche le logo
        self.logo = pygame.image.load(image_LOGO).convert_alpha()
        menu_surface.blit(self.logo, (0, 0))

        # Puis on affiche le menu
        self.main_box.set_topleft(POS_PARAMETRES)
        self.update()

    def generate_menu(self):
        """initialise les éléments du menu"""

        # Liste contenant tous les éléments du Menu
        self.elements = []

        # On génère la box affichant l'état de Day, Tick & Population
        self.set_state_box()

        # On génère pour chaque paramètre son slider associé
        self.generate_sliders()

        # Boutton Quitter
        self.gui_quit = False
        self.quit_button = thorpy.make_button("Quit", func=self.quit_button_pressed)
        self.elements.append(self.quit_button)

        # Boutton Pause
        self.gui_pause = False
        self.pause_button = thorpy.make_button("Play / Pause", func=self.pause_button_pressed)
        self.elements.append(self.pause_button)

        # Regroupement de tous les éléments dans une box
        thorpy.style.DEF_COLOR = BLACK
        self.main_box = thorpy.Box(elements=self.elements, size=DIM_MENU)

        # Affectation de la box à un menu (même s'il n'y en a qu'une box) : important pour la gestion d'events
        self.menu = thorpy.Menu(self.main_box)

    def update(self):
        """update : met à jour les paramètres et les visuels à chaque tick"""
        self.main_box.update()
        self.update_values() # pour les paramètres
        self.main_box.blit()
        self.main_box.update()

    def set_state_box(self):
        """Affiche l'état de la simulation (days, ticks, population) et les outils graphiques pour se déplacer
        de tick en tick et de day en day"""

        # Style
        # thorpy.set_theme("human")
        thorpy.style.FONT_COLOR = WHITE
        thorpy.style.DEF_COLOR = BLACK

        # Elements Textuels (champ pour le texte, champ pour la valeur), on les regroupe dans des boxs
        day_text = thorpy.make_text("Day", FONT_SIZE, WHITE)
        tick_text = thorpy.make_text("Tick", FONT_SIZE, WHITE)
        pop_text = thorpy.make_text("Population", FONT_SIZE, WHITE)
        day_number = thorpy.make_text("__", FONT_SIZE, WHITE)
        tick_number = thorpy.make_text("__", FONT_SIZE, WHITE)
        pop_number = thorpy.make_text("___", FONT_SIZE, WHITE)
        self.box_day_display = thorpy.Box(elements=[day_text, day_number])
        self.box_tick_display = thorpy.Box(elements=[tick_text, tick_number])
        self.box_pop_display = thorpy.Box(elements=[pop_text, pop_number])

        # Boutons + et - pour contrôler les ticks dans le mode Pause
        button_day_plus = thorpy.make_button("+", func=self.button_day_plus_pressed)
        button_day_minus = thorpy.make_button("-", func=self.button_day_minus_pressed)
        button_tick_plus = thorpy.make_button("+", func=self.button_tick_plus_pressed)
        button_tick_minus = thorpy.make_button("-", func=self.button_tick_minus_pressed)

        # On les désactive pour l'instant
        button_day_plus.set_active(False)
        button_day_minus.set_active(False)
        button_tick_plus.set_active(False)
        button_tick_minus.set_active(False)

        # On resize les boutons
        button_day_plus.set_size(size=DIM_PLUSMINUSBUTTON)
        button_day_minus.set_size(size=DIM_PLUSMINUSBUTTON)
        button_tick_plus.set_size(size=DIM_PLUSMINUSBUTTON)
        button_tick_minus.set_size(size=DIM_PLUSMINUSBUTTON)

        # Style
        thorpy.set_theme("human")

        # On rassemble DAY et TICK horizontalement dans BoxH
        boxH = thorpy.make_group(elements=[button_day_minus, self.box_day_display, button_day_plus,button_tick_minus,
                                            self.box_tick_display, button_tick_plus], mode="h")

        # On rassemble boxH et box_pop_display dans une box finale : state_box
        self.state_box = thorpy.Box(elements=[boxH,self.box_pop_display], size=DIM_STATEBOX)

        # On rajoute la box finale dans la liste éléments
        self.elements.append(self.state_box)

    def update_state_box(self, day, tick, pop):
        """"Met à jour l'affichage du day, du tick et de la population"""

        # On génère de nouveaux éléments textuels avec les nouvelles valeurs
        new_pop_element = thorpy.make_text(str(pop), FONT_SIZE, WHITE)
        new_tick_element = thorpy.make_text(str(tick % TICK_DAY), FONT_SIZE, WHITE)
        new_day_element = thorpy.make_text(str(day), FONT_SIZE, WHITE)

        # On remplace l'ancienne valeur avec la nouvelle avec la méthode thorpy.Box.replace_element(old, new)
        # ici old correspond au 2ème champ textuel de chaque box, on le get avec get_elements()[1]
        self.box_day_display.replace_element(self.box_day_display.get_elements()[1], new_day_element)
        self.box_tick_display.replace_element(self.box_tick_display.get_elements()[1], new_tick_element)
        self.box_pop_display.replace_element(self.box_pop_display.get_elements()[1], new_pop_element)

        # On met à jour l'affichage de la box
        self.state_box.update()
        self.state_box.blit()
        self.state_box.update()

    def generate_sliders(self):
        """ Génère des sliders à partir des paramètres déclarés dans parameters.default{}
            Vérifie si l'argument SHOW est bien égal à True avant de créer le slider"""

        # Dictionnaire de sliders
        self.sliders = {}

        # Tableau d'éléments textuels (générés avec la méthode thorpy.OneLineText)
        self.titles = []

        # On parcourt tous les paramètres contenus dans parameters.default ayant l'argument SHOW=True (k[4])
        for name,k in parameters.default.items():
            if k[4]: # Si l'argument SHOW est à TRUE

                # On génère les titres des paramètres avec la méthode OneLineText de Thorpy
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

                # On regroupe le titre et le slider dans une box que l'on rajoute à notre liste self.elements
                self.elements.append(thorpy.Box(elements=[self.titles[-1], self.sliders[name]], size=DIM_SLIDER_BOX))

    def set_style(self):
        """Modifie le style des éléments déjà déclarés"""

        # Box principale
        self.main_box.set_main_color(BLACK)

        # Boxs
        for box in self.elements:
            box.set_main_color(BLACK)

        # Titres
        for title in self.titles:
            self.set_font_style(title, FONT_COLOR, FONT_SIZE, FONT)

        # De la personnalisation des Sliders : Un objet thorpy.SliderX est composé
        # - d'un élément textuel pour le titre (que l'on n'utilisera pas car difficilement personnalisable)
        # - d'un Slider(thorpy.SliderX.get_slider())
        # - d'un dragger (thorpy.SliderX.get_dragger())
        # - et d'un élément textuel pour la valeur (thorpy.SliderX._value_element)
        # Chaque attribut de ces constituants est personnalisable

        for slider in self.sliders.values():
            slider.get_dragger().set_main_color(WHITE)
            slider.get_dragger().set_size(DIM_DRAGGER)
            slider.get_slider().set_main_color(WHITE)
            slider.get_slider().set_size(DIM_SLIDER)
            self.set_font_style(slider._value_element, FONT_COLOR, FONT_SIZE, FONT)

        # Boutton Quitter
        self.set_font_style(self.quit_button, FONT_COLOR, FONT_SIZE, FONT)
        self.quit_button.set_font_color_hover(WHITE)

        # Boutton Pause
        self.set_font_style(self.pause_button, FONT_COLOR, FONT_SIZE, FONT)
        self.pause_button.set_font_color_hover(WHITE)

    def set_font_style(self, element, font_color, font_size, font):
        """Prend en argument un élément textuel et lui affecte une police (str),
        une couleur ((R,G,B)) et une taille (int)"""
        element.set_font_color(font_color)
        element.set_font_size(font_size)
        element.set_font(font)

    def assign_surface(self, mon_menu, ma_surface):
        """Très importante : assigne une surface aux éléments d'un menu"""
        for element in mon_menu.get_population():
            element.surface = ma_surface

    def update_values(self):
        """update_values : met à jour les valeurs des paramètres dans parametres.actual
        avec la méthode parametres.set()"""
        for name, slider in self.sliders.items():
            parameters.set(name, slider.get_value())

    def quit_button_pressed(self):
        """quit_button_pressed : appelée quand on clique sur le Bouton Quit"""
        self.gui_quit = True

    def pause_button_pressed(self):
        """pause_button_pressed : appelée quand on clique sur le Bouton Pause"""
        self.gui_pause = not self.gui_pause

    def button_day_plus_pressed(self):
        pass

    def button_day_minus_pressed(self):
        pass

    def button_tick_plus_pressed(self):
        pass

    def button_tick_minus_pressed(self):
        pass

    def progress_bar(self, pos, size, progress, screen, bar_color, border=False, border_color=WHITE, vertical=False, reverse=False, round=False, radius=20):
        """
        Draws a progress bar
        param pos sets position of progress bar
        param size sets size of progress bar
        param progress is the current progress
        param screen is the screen where the bar should be drawn
        param border is border, if is necessary
        param vertical is wether you want vertical or horizontal bar
        param reverse make the bar drawing backward (100% -> 0%)
        param round sets if you want round rectangles or not
        param radius is the radius of angles if round is True
        """
        if progress < 0:
            progress = 0

        if border:
            pygame.draw.rect(screen, border_color, ((pos[0] + 3, pos[1] + 3), (size[0] + 3, size[1] + 3)))

        inner_pos = pos
        if reverse and vertical:
            changed_size = size[1] - (size[1] * progress)
            inner_pos = (pos[0], pos[1] + changed_size)
            inner_size = (size[0], size[1] * progress)
        elif not reverse and vertical:
            inner_size = (size[0], progress)
        elif not reverse and not vertical:
            inner_size = (size[0] * progress, size[1])
        if round:
            self.round_rect(screen, pygame.Rect(inner_pos, inner_size), bar_color, radius)
        else:
            pygame.draw.rect(screen, bar_color, pygame.Rect(inner_pos, inner_size))

    def round_rect(self, surface, rect, color, rad=20):
        """
        Draw a rect with rounded corners to surface.  Argument rad can be specified
        to adjust curvature of edges (given in pixels).  An optional border
        width can also be supplied; if not provided the rect will be filled.
        Both the color and optional interior color (the inside argument) support
        alpha.
        """
        rect = pygame.Rect(rect)
        zeroed_rect = rect.copy()
        zeroed_rect.topleft = 0, 0
        image = pygame.Surface(rect.size).convert_alpha()
        image.fill((0, 0, 0, 0))
        self._render_region(image, zeroed_rect, color, rad)
        surface.blit(image, rect)

    def _render_region(self, image, rect, color, rad):
        """Helper function for round_rect."""
        corners = rect.inflate(-2 * rad, -2 * rad)
        for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
            pygame.draw.circle(image, color, getattr(corners, attribute), rad)
        image.fill(color, rect.inflate(-2 * rad, 0))
        image.fill(color, rect.inflate(0, -2 * rad))

