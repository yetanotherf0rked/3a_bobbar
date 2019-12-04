from controller.parameters import *
parameters = Parameters()

# Tick par jour 100
TICK_DAY = 100
# Population initiale 200
NB_POP = 50
# Taille de la carte 100
TAILLE = 40
#Nourriture sur la carte 200
NB_FOOD = 200
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

# Chargement des images
image_FOND = "ressources/images/wall.jpg"
image_SOL = "ressources/images/isometric_pixel_0046.png"
image_BOB = "ressources/images/polar_bear_white2.png"
image_FOOD = "ressources/images/biere.png"
image_LOGO = "ressources/images/logov2.png"
image_EARTH1 = "ressources/images/terre1 clair.png"
image_EARTH2 = "ressources/images/terre2 clair.png"
image_EARTH3 = "ressources/images/terre3 clair.png"
image_EARTH4 = "ressources/images/terre4 clair.png"
image_EARTH5 = "ressources/images/terre 1.png"
image_EARTH7 = "ressources/images/Grass.png"
image_EARTH6 = "ressources/images/terre 3.png"

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Dimensions et Positions des Elements Graphiques
DIM_WINDOW_X = 960 * 2
DIM_WINDOW_Y = 540 * 2
DIM_WINDOW = (DIM_WINDOW_X, DIM_WINDOW_Y)

DIM_MENU_X = 220
DIM_MENU_Y = DIM_WINDOW_Y
DIM_MENU = (DIM_MENU_X, DIM_WINDOW_Y)

DIM_SIMU = (DIM_WINDOW_X - DIM_MENU_X, DIM_WINDOW_Y)

DIM_SLIDER_X = 150
DIM_SLIDER_Y = 7 # valeur par défaut : 20
DIM_SLIDER = (DIM_SLIDER_X, DIM_SLIDER_Y)

DIM_DRAGGER = (5, 20)
DIM_SLIDER_BOX = (210, 50)
DIM_STATEBOX = (210, 100)
DIM_PLUSMINUSBUTTON = (20, 30)

POS_LOGO = (0, 0)
POS_PARAMETRES = (0, 221)
POS_SURFACE_SIMU = (221, 0)
POS_SURFACE_MENU = (0, 0)

# Default Font Style
FONT_COLOR = WHITE
FONT_SIZE = 10
FONT = "verdana"