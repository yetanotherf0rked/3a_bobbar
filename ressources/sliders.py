import ressources.config as config

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (169, 169, 169)
COLOR_ELECTRON_BLUE = (9, 132, 227)
COLOR_ELECTRON_BLUE_ALPHA = (9, 132, 227, 100)
BEER = (242, 142, 28)
BEER_PALETTE = [(204, 111, 150), (204, 125, 35), (242, 142, 28), (255, 200, 80), (255, 200, 150), (255, 215, 0),
                (204, 111, 0)]

# Dimensions et Positions des Elements Graphiques
DIM_LOGO_X = 210
DIM_LOGO_Y = 210

DIM_MENU_X = 220  # min recommandé : 240

DIM_SLIDER_X = DIM_MENU_X - 80
DIM_SLIDER_Y = 7  # valeur par défaut : 20
DIM_SLIDER = (DIM_SLIDER_X, DIM_SLIDER_Y)

DIM_DRAGGER = (5, 20)
DIM_SLIDER_BOX = (DIM_MENU_X - 10, 50)
DIM_STAT_BOX = ((DIM_MENU_X - 25) / 2, 40)

POS_LOGO_X = int((DIM_MENU_X - DIM_LOGO_X) / 2)  # logo centré p/r à menu_surface
POS_LOGO_Y = 20  # marges
POS_LOGO = (POS_LOGO_X, POS_LOGO_Y)
POS_SURFACE_SIMU = (DIM_MENU_X + 1, 0)
POS_SURFACE_MENU = (0, 0)
POS_STAT_TITLE = (7, 5)
POS_STAT_VALUE = (7, 20)

# Default Font Style
FONT_COLOR = WHITE
FONT_SIZE = 11
FONT = "verdana"


class Sliders:

    def __init__(self):
        """ Automatise la création des sliders
                - on déclare un nouveau paramètre avec make()
                - on accède au paramètre avec get()
        """

        # Dictionnaire contenant les paramètres à initialiser
        self.default = {}

        # Créez vos paramètres ici
        self.make("NB_FOOD", 0, config.para.NB_FOOD, 500, info="Food Number")
        self.make("ENERGY_FOOD", 0, config.para.ENERGY_FOOD, 150, info="Food Energy")
        self.make("ENERGY_SPAWN", 0, config.para.ENERGY_SPAWN, 150, info="Spawn Energy")
        self.make("ENERGY_MAX", 0, config.para.ENERGY_MAX, 500, info="Energy max for Bob")
        self.make("ENERGY_MOTHER", 0, config.para.ENERGY_MOTHER, 75, info="Mother Energy")
        self.make("ENERGY_SON", 0, config.para.ENERGY_SON, 75, info="Son Energy")

    def make(self, name, min, init, max, type=int, show=True, info=""):
        """Crée un paramètre et l'ajoute au dictionnaire
                :param name: string contenant le nom de la variable à mettre à jour (voir config.py)
                :param min: valeur minimale (int ou float)
                :param init: valeur initiale (int ou float)
                :param max: valeur maximale (int ou float)
                :param type: int ou float
                :param show: True pour afficher le slider, False pour cacher le slider
                :param info: string contenant le label à afficher au-dessus du slider
                """
        self.default[name] = (min, init, max, type, show, info)

    def get_info(self, name):
        """
        Retourne le nom de la variable contenant le paramètre
        :param name: string contenant le nom de la variable
        """
        if self.default[name][-1] != "":
            return self.default[name][-1]
        else:
            return name


# On déclare notre instance parameters
sliders_Config = Sliders()
