import model.config as config

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLOR_ELECTRON_BLUE = (9, 132, 227)
BEER = (242, 142, 28)
BEER_PALETTE = [(204,111,150),(204,125,35),(242,142,28),(255,200,80),(255,200,150),(255,215,0),(204,111,0)]


# Dimensions et Positions des Elements Graphiques
DIM_LOGO_X = 210
DIM_LOGO_Y = 210

DIM_MENU_X = 220 # min recommandé : 240

DIM_SLIDER_X = DIM_MENU_X - 80
DIM_SLIDER_Y = 7 # valeur par défaut : 20
DIM_SLIDER = (DIM_SLIDER_X, DIM_SLIDER_Y)

DIM_DRAGGER = (5, 20)
DIM_SLIDER_BOX = (DIM_MENU_X-10, 50)
# DIM_STATEBOX = (DIM_MENU_X-10, 100)
DIM_STAT_BOX = ((DIM_MENU_X-25)/2, 40)
# DIM_PLUSMINUSBUTTON = (20, 30)

POS_LOGO_X = int((DIM_MENU_X - DIM_LOGO_X)/2) # logo centré p/r à menu_surface
POS_LOGO_Y = 20 # marges
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
        """ À retenir :
                - une instance parameters de la classe Parameters est déclarée dans config.py
                - cette instance permet d'accéder aux paramètres depuis n'importe quel fichier .py
                - on déclare un nouveau paramètre avec make()
                - on accède au paramètre avec get()
                - on modifie le paramètre avec set()


            default :       Dictionnaire initialisateur des paramètres
                            Sert à automatiser l'initialisation des sliders
                            nom_du_paramètre:(valeur_min, valeur_initiale, valeur_max, type=int ou float,
                            show=False si l'on veut cacher le paramètre)

            actual :        Dictionnaire contenant les valeurs des paramètres en temps réel
                            Il est mis à jour avec la méthode gui.update_values()
                            nom_du_paramètre:valeur
        """

        # default : nom_du_paramètre:(valeur_min, valeur_initiale, valeur_max, type=int ou float, True : afficher le paramètre dans le menu)
        self.default = {}

        # actual : nom_du_paramètre:valeur
        self.actual = {}

        # Créez vos paramètres ici
        self.make("Food Number", 0, config.para.NB_FOOD, 250)
        self.make("Food Energy", 50, config.para.ENERGY_FOOD, 150)
        self.make("Spawn Energy", 50, config.para.ENERGY_SPAWN, 150)
        self.make("Energy Cost while Moving", 0.0, config.para.ENERGY_MOVE, 5.0, float)
        self.make("Energy Cost at Stay", 0.0, config.para.ENERGY_STAY, 5.0, float)
        # self.make("Max Energy", 50, config.para.ENERGY_MAX, 300)
        self.make("Mother Energy", 25, config.para.ENERGY_MOTHER, 75)
        self.make("Son Energy",25, config.para.ENERGY_SON, 75)

        # on initialise les valeurs d'Actual avec les valeurs initiales déclarées ci-dessus
        for k,v in self.default.items():
            self.actual[k] = v[1]

    def make(self, name, min, init, max, type=int, show=True):
        """Initialise un paramètre
             type = int ou float
             show = True génère un slider pour le paramètre
                  = False crée un paramètre mais ne génère pas de slider dans l'interface gui"""
        self.default[name] = (min, init, max, type, show)

    def get(self, param):
        """Retourne la valeur du paramètre dans Actual
            Exemple : bob.energy = parameters.get("Son Energy") renvoie la valeur actuelle du slider Son Energy"""
        return self.actual[param]

    def set(self, param, value):
        """Permet de mettre à jour un paramètre dans le dictionnaire Actual. Utilisée dans gui.update_values()"""
        self.actual[param] = value

# On déclare notre instance parameters
sliders = Sliders()
