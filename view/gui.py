import pygame
import thorpy

import ressources.config
from ressources.sliders import *
from view.debug import *
from view.button import Button


class Gui:
    """ Gui : initialise l'interface utilisateur
        Les différents éléments sont stockés dans des objets thorpy.Box

        Hiérarchie des boxs :

        --- Box: box prinxcipale self.main_box (the father of all the boxes)
        ------ Box: Box Titre Stats
        --------- Texte: Titre Stats
        ------ Box: box des stats self.stats_box. Pour tous les deux stats :
        --------- Box: box horizontale (regroupe deux box stats)
        ------------ Box: box stat (correspond à 1 stat)
        --------------- Texte: Nom du stat
        --------------- Texte: valeur du stat
        ...
        ------ Box: Box Titre Paramètres
        --------- Texte: Titre Paramètres
        ------ Box: box des sliders. Pour chaque paramètre :
        --------- Texte: Titre du paramètre
        --------- Slider.
        ...
        ------ Boutton  Quitter
        ------ Boutton Pause
    """

    def __init__(self, menu_surface):
        self.isupdate = False
        self.config = ressources.config.para

        #  For zoom and position
        self.show_reset = False

        # Thème par défaut
        thorpy.set_theme("human")

        # Génère les éléments du Menu
        self.generate_menu()

        # On modifie le style des éléments
        self.set_style()

        # On définit menu_surface comme la surface de l'interface GUI
        self.assign_surface(self.menu, menu_surface)

        # Puis on affiche le menu
        self.main_box.set_topleft(POS_SURFACE_MENU)

        # On met à jour
        self.main_box.blit()
        self.main_box.update()

    def generate_menu(self):
        """initialise les éléments du menu"""

        # Liste contenant tous les éléments du Menu
        self.elements = []

        # Logo
        img = thorpy.Image(path=self.config.image_LOGO)
        self.elements.append(img)

        # On génère la box des stats
        self.init_stats_box()

        # On génère pour chaque paramètre son slider associé
        self.generate_sliders()

        # Bouton Settings
        self.settings_button = thorpy.make_button("Settings", func=self.settings_button_pressed)
        self.settings_button.set_main_color(BLACK)
        self.elements.append(self.settings_button)

        # Bouton Pause
        self.gui_pause = False
        self.pause_button = thorpy.make_button("Play/Pause", func=self.pause_button_pressed)
        self.pause_button.set_main_color(BLACK)
        self.elements.append(self.pause_button)

        # Bouton Quitter
        self.gui_quit = False
        self.quit_button = thorpy.make_button("Quit", func=self.quit_button_pressed)
        self.quit_button.set_main_color(BLACK)
        self.elements.append(self.quit_button)

        #  Color palette to show velocity
        thorpy.set_theme("human")
        self.color_palette = thorpy.ColorSetter.make()
        self.elements.append(self.color_palette)

        # Regroupement de tous les éléments dans une box
        thorpy.style.DEF_COLOR = BLACK
        self.main_box = thorpy.Background(color=((0, 0, 0, 100)), elements=self.elements)
        thorpy.store(self.main_box, x=DIM_MENU_X / 2, y=0, mode="v", align="center")
        reaction1 = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                    reac_func=self.react_slider,
                                    event_args={"id": thorpy.constants.EVENT_SLIDE},
                                    reac_name="my reaction to slide event")
        self.main_box.add_reaction(reaction1)
        self.main_box.add_lift(axis="vertical")
        self.main_box.refresh_lift()

        # Affectation de la box à un menu (même s'il n'y en a qu'une box) : important pour la gestion d'events
        self.menu = thorpy.Menu(self.main_box)

    def update(self, stats):
        """update : met à jour les paramètres et les visuels à chaque tick"""
        if self.isupdate:
            self.update_values()  # pour les paramètres
            self.isupdate = False
        self.update_stats_box(stats)
        self.main_box.blit()
        self.main_box.update()

    def init_stats_box(self):
        """Initialise la box d'affichage des stats
        Dépend du debug.py"""

        # Titre du Menu Statistics
        thorpy.set_theme("classic")
        menu_title = thorpy.make_text("Statistics", font_color=BLACK)
        thorpy.style.DEF_COLOR = (COLOR_ELECTRON_BLUE)
        menu_title_box = thorpy.Box(elements=[menu_title], size=[DIM_MENU_X - 25, 25])
        menu_title_box.set_main_color(COLOR_ELECTRON_BLUE)
        thorpy.set_theme("human")
        self.elements.append(menu_title_box)

        # Liste elements_stats, sert à accéder aux éléments et à les mettre à jour dans update_stats_box
        self.elements_stats = []

        # Elements Textuels des stats (champ pour le texte, champ pour la valeur), on les regroupe dans des boxs
        for stat in init_stats():
            text = thorpy.make_text(stat)
            value = thorpy.make_text("")
            stat_box = thorpy.Box(elements=[text, value], size=DIM_STAT_BOX)
            stat_box.set_main_color(BLACK)
            self.elements_stats.append(stat_box)
            # text.set_topleft(POS_STAT_TITLE)
            # value.set_topleft(POS_STAT_VALUE)

        # On les regroupe horizontalement deux par deux en faisant attention au cas impair
        boxesH = []
        for i in range(0, len(self.elements_stats), 2):
            if i + 1 != len(self.elements_stats):
                boxesH.append(thorpy.make_group(elements=[self.elements_stats[i],
                                                          self.elements_stats[i + 1]], mode="h"))
            else:
                boxesH.append(self.elements_stats[i])

        # Style : bordures blanches
        thorpy.style.DEF_COLOR = BLACK

        # On rassemble les boxs horizontales dans une box stats_boxs
        self.stats_box = thorpy.Box(elements=boxesH)

        # On rajoute cette box dans la liste éléments
        self.elements.append(self.stats_box)

    def update_stats_box(self, stats):
        """"Met à jour l'affichage des stats
        Dépend de debug.py"""

        # On génère les éléments textuels avec les nouvelles valeurs
        for k in range(len(stats)):
            value = stats[k]
            new_value_text = ""
            # Si value est un tuple de type (moy, max, min)
            if type(value) == tuple:
                for i in range(len(value)):
                    new_value_text += '%.2f' % value[i] + "  "
            # Si c'est un float
            elif type(value) == float:
                new_value_text += '%.2f' % value[i]
            # Si c'est un int
            else:
                new_value_text += str(value)
            # rajouter exception si ce n'est ni un tuple, ni un float, ni un int ???

            # On remplace par le nouveau text
            self.elements_stats[k].get_elements()[1].set_text(new_value_text)

            # On le reset au-dessous du titre du stat
            self.elements_stats[k].get_elements()[1].stick_to(self.elements_stats[k].get_elements()[0],
                                                              target_side="bottom", self_side="top")

    def generate_sliders(self):
        """ Génère des sliders à partir des paramètres déclarés dans sliders_Config.default{}
            Vérifie si l'argument SHOW est bien égal à True avant de créer le slider"""
        # Titre du Menu Paramètres
        thorpy.set_theme("classic")
        menu_title = thorpy.make_text("sliders_Config")
        thorpy.style.DEF_COLOR = (COLOR_ELECTRON_BLUE)
        menu_title_box = thorpy.Box(elements=[menu_title], size=[DIM_MENU_X - 25, 25])
        menu_title_box.set_main_color(COLOR_ELECTRON_BLUE)
        self.elements.append(menu_title_box)

        # Thème
        thorpy.set_theme("human")

        # Dictionnaire de sliders
        self.sliders = {}

        # Tableau de la box de sliders (générés avec la méthode thorpy.OneLineText)
        box_sliders = []

        # On parcourt tous les paramètres contenus dans sliders_Config.default ayant l'argument SHOW=True (k[4])
        for name, k in sliders_Config.default.items():
            if k[4]:  # Si l'argument SHOW est à TRUE

                # On génère les titres des paramètres
                if k[-1] != "":
                    box_sliders.append(thorpy.make_text(k[-1]))
                else:
                    box_sliders.append(thorpy.make_text(name))

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
                box_sliders.append(self.sliders[name])

        thorpy.set_theme("human")
        thorpy.style.DEF_COLOR = BLACK
        box_sliders = thorpy.Box(box_sliders)
        self.elements.append(box_sliders)

    def set_style(self):
        """Modifie le style des éléments déjà déclarés"""

        # Box principale
        self.main_box.set_main_color(BLACK)

        for slider in self.sliders.values():
            slider.get_dragger().set_main_color(WHITE)
            slider.get_dragger().set_size(DIM_DRAGGER)
            slider.get_slider().set_main_color(WHITE)
            slider.get_slider().set_size(DIM_SLIDER)
            self.set_font_style(slider._value_element, FONT_COLOR, FONT_SIZE, FONT)

        # Obliger de redonner les valeurs ici sinon elles sont toute incrémentées d'un cran
        for name, k in sliders_Config.default.items():
            eval("self.sliders[name].set_value(self.config.%s)" % name)

        # Boutton Quitter
        self.set_font_style(self.quit_button, FONT_COLOR, FONT_SIZE, FONT)
        self.quit_button.set_font_color_hover(WHITE)

        # Boutton Pause
        self.set_font_style(self.pause_button, FONT_COLOR, FONT_SIZE, FONT)
        self.pause_button.set_font_color_hover(WHITE)

        # Toutes les boxs
        for element in self.main_box.get_descendants():
            if element.get_text() != "":
                self.set_font_style(element, FONT_COLOR, FONT_SIZE, FONT)
        for element in self.main_box.get_elements():
            element.set_main_color((9, 132, 227, 100))

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
            exec("self.config.%s=%s" % (name, slider.get_value()))

    def quit_button_pressed(self):
        """quit_button_pressed : appelée quand on clique sur le Bouton Quit"""
        self.gui_quit = True

    def settings_button_pressed(self):
        """settings_button_pressed : appelée quand on clique sur le Bouton Settings"""
        self.config.settings = True

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

    def progress_bar(self, pos, size, progress, screen, bar_color, bg=False, bg_color=BLACK, vertical=False,
                     reverse=False, round=False, radius=20):
        """
        Draws a progress bar /!\ This function works for the project but not all cases are treated
        :param pos sets position of progress bar
        :param size sets size of progress bar
        :param progress is the current progress, between 0 and 1
        :param screen is the screen where the bar should be drawn
        :param bg is background, if is necessary
        :param vertical is wether you want vertical or horizontal bar
        :param reverse make the bar drawing backward (100% -> 0%)
        :param round sets if you want round rectangles or not
        :param radius is the radius of angles if round is True
        """
        if progress < 0:
            progress = 0

        # Useful for life bars
        if bg:
            self.round_rect(screen, pygame.Rect(pos, size), bg_color, radius)

        inner_pos = pos
        if reverse and vertical:
            """
            This case is particular, because pos represent the top left corner, and rect is drawn from pos
            We have to reduce size and lower position to get what we want
            """
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

    # The 2 functions below come from an existing project
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

    def react_slider(self,event):
        self.isupdate = True

    def draw_reset_button(self, screen):
        self.zoom_position = Button("Reset", (screen.get_width() * 0.91, screen.get_height()*0.45),
                                    self.reset_pressed, BEER, BLACK, (150,70), font_size=20)
        self.zoom_position.draw(screen)

    def reset_pressed(self):
        self.reset = True
