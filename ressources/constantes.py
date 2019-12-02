from controller.parameters import *

parameters = Parameters()

# Tick par jour 100
TICK_DAY = 100
# Population initiale 200
NB_POP = 50
# Taille de la carte 100
TAILLE = 40

# Chargement des images
image_SOL = "ressources/images/isometric_pixel_0046.png"
image_BOB = "ressources/images/polar_bear_white2.png"
image_FOOD = "ressources/images/biere.png"
image_LOGO = "ressources/images/logov2.png"

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Dimensions
DIM_WINDOW_X = 960 * 2
DIM_WINDOW_Y = 540 * 2
DIM_WINDOW = (DIM_WINDOW_X, DIM_WINDOW_Y)
DIM_LOGO_X = 220
DIM_LOGO_Y = 220
DIM_LOGO = (DIM_LOGO_X, DIM_LOGO_Y)
DIM_MENU_X = 220
DIM_MENU_Y = DIM_WINDOW_Y - DIM_LOGO_Y
DIM_MENU = (DIM_MENU_X, DIM_MENU_Y)
DIM_SIMU_X = DIM_WINDOW_X - DIM_MENU_X
DIM_SIMU_Y = DIM_WINDOW_Y
DIM_SIMU = (DIM_SIMU_X, DIM_SIMU_Y)
DIM_SLIDER_X = 150
DIM_SLIDER_Y = 7
DIM_SLIDER_DRAGGER_X = 5
DIM_SLIDER_DRAGGER_Y = 20
DIM_SLIDER_DRAGGER = (DIM_SLIDER_DRAGGER_X, DIM_SLIDER_DRAGGER_Y)
DIM_SLIDER_BOX_X = 200
DIM_SLIDER_BOX_Y = 50
DIM_SLIDER_BOX = (DIM_SLIDER_BOX_X, DIM_SLIDER_BOX_Y)
POS_SURFACE_LOGO = (0, 0)
POS_SURFACE_MENU = (0, 221)
POS_SURFACE_SIMU = (221, 0)
# Default Font Style
FONT_COLOR = WHITE
FONT_SIZE = 10
FONT = "verdana"