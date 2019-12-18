# Tick par jour 100
TICK_DAY = 100
# Population initiale 200
NB_POP = 50
# Taille de la carte 100
TAILLE = 40
#Nourriture sur la carte 200
NB_FOOD = 100
#Energy par food 100
ENERGY_FOOD = 100
#Energy par spawn de Bob 100
ENERGY_SPAWN = 100
#Cout d'un déplacement 1 -> velocity**2
ENERGY_MOVE = 1
#Cout sans déplacement 0.5
ENERGY_STAY = 0.5
#Energy_max d'un Bob 200
ENERGY_MAX = 200
#Energy après naissance 50
ENERGY_MOTHER = 50
#Energy enfant 50
ENERGY_SON = 50
#Taux de mutation de la vitesse
MUT_VELOCITY = 0.1
#Taux de mutation de la masse
MUT_MASSE = 0.1
#taux de mutation de la perception
MUT_PERCEPT=1
#taux de mutation de la memoire
MUT_MEMORY = 1
#Deplacement step
DEP_STEP = 20
#Energie min nescessaire pour la reproduction sexuée
ENERGY_MIN_REPRO = 150
#energie enfant de la reproduction sexuée
ENERGY_SON_REPRO = 100
#Energie dépensée lors de la reproduction sexuée
ENERGY_REPRO = 150

FAMILY_REPRODUCTION = False
FAMILY_AGGRESSION = False

DIFF_AGE_FOR_REPRODUCTION = 500  # valeur en tick

# Chargement des images
image_BOB = "ressources/images/polar_bear_white2.png"
image_FOOD = "ressources/images/biere.png"
image_LOGO = "ressources/images/logo_round_210.png"
image_EARTH1 = "ressources/images/terre1 clair.png"
image_EARTH2 = "ressources/images/terre2 clair.png"
image_EARTH3 = "ressources/images/terre3 clair.png"
image_EARTH4 = "ressources/images/terre4 clair.png"
image_EARTH5 = "ressources/images/terre 1.png"
image_EARTH7 = "ressources/images/Grass.png"
image_EARTH6 = "ressources/images/terre 3.png"
image_EARTH_WOW = "ressources/images/terrespec.png"
image_REDBOB = "ressources/images/polar_bear_red.png"
image_SOLEIL = "ressources/images/Soleil300x300.png"
image_LUNE = "ressources/images/lune.png"
image_EMPTY_BEER = "ressources/images/empty_beer_icon.png"

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

DIM_MENU_X = 240 # min recommandé : 240

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

# FULLSCREEN
FULLSCREEN = False

#Affichage de la perception de chaque bob
WATCH_PERCEPTION = False

#Affichage minimap
MINIMAP = True

class Parameters:

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
        self.make("Food Number", 0, NB_FOOD, 250)
        self.make("Food Energy", 50, ENERGY_FOOD, 150)
        self.make("Spawn Energy", 50, ENERGY_SPAWN, 150)
        self.make("Energy Cost while Moving", 0.0, ENERGY_MOVE, 5.0, float)
        self.make("Energy Cost at Stay", 0.0, ENERGY_STAY, 5.0, float)
        # self.make("Max Energy", 50, ENERGY_MAX, 300)
        self.make("Mother Energy", 25, ENERGY_MOTHER, 75)
        self.make("Son Energy",25, ENERGY_SON, 75)

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
parameters = Parameters()