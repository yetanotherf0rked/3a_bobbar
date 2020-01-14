"""
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

DISTANCE_TO_BE_IN_SAME_FAMILY = 3

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

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLOR_ELECTRON_BLUE = (9, 132, 227)

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

"""

class Config():

    def __init__(self):
        self.show_Minimap = False
        self.fullscreen = False
        self.show_Perception = False
        self.show_Bord_Case = False
        self.historique = False
        self.family_Reproduction = False
        self.family_Agression = False
        self.affichage = False
        self.show_graph = False

        # Tick par jour 100
        self.TICK_DAY = 100
        # Population initiale 200
        self.NB_POP = 100
        # Taille de la carte 100
        self.TAILLE = 40
        # Nourriture sur la carte 200
        self.NB_FOOD = 200
        # Energy par food 100
        self.ENERGY_FOOD = 100
        # Energy par spawn de Bob 100
        self.ENERGY_SPAWN = 100
        # Cout d'un déplacement 1 -> velocity**2
        self.ENERGY_MOVE = 1
        # Cout sans déplacement 0.5
        self.ENERGY_STAY = 0.5
        # Energy_max d'un Bob 200
        self.ENERGY_MAX = 200
        # Energy après naissance 50
        self.ENERGY_MOTHER = 50
        # Energy enfant 50
        self.ENERGY_SON = 50
        # Taux de mutation de la vitesse
        self.MUT_VELOCITY = 0.1
        # Taux de mutation de la masse
        self.MUT_MASSE = 0.1
        # taux de mutation de la perception
        self.MUT_PERCEPT = 1
        # taux de mutation de la memoire
        self.MUT_MEMORY = 1
        # Deplacement step
        self.DEP_STEP = 20
        # Energie min nescessaire pour la reproduction sexuée
        self.ENERGY_MIN_REPRO = 150
        # energie enfant de la reproduction sexuée
        self.ENERGY_SON_REPRO = 100
        # Energie dépensée lors de la reproduction sexuée
        self.ENERGY_REPRO = 150

        self.DIFF_AGE_FOR_REPRODUCTION = 500  # valeur en tick
        self.DISTANCE_TO_BE_IN_SAME_FAMILY=2

        # Chargement des images
        self.image_BOB = "ressources/images/polar_bear_white2.png"
        self.image_FOOD = "ressources/images/biere.png"
        self.image_LOGO = "ressources/images/logo_round_210.png"
        self.image_EARTH1 = "ressources/images/terre1 clair.png"
        self.image_EARTH2 = "ressources/images/terre2 clair.png"
        self.image_EARTH3 = "ressources/images/terre3 clair.png"
        self.image_EARTH4 = "ressources/images/terre4 clair.png"
        self.image_EARTH5 = "ressources/images/terre 1.png"
        self.image_EARTH7 = "ressources/images/Grass.png"
        self.image_EARTH6 = "ressources/images/terre 3.png"
        self.image_EARTH_WOW = "ressources/images/terrespec.png"
        self.image_REDBOB = "ressources/images/polar_bear_red.png"
        self.image_SOLEIL = "ressources/images/Soleil300x300.png"
        self.image_LUNE = "ressources/images/lune.png"
        self.image_EMPTY_BEER = "ressources/images/empty_beer_icon.png"


para = Config()
