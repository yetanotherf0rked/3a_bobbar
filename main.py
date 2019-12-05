import os
import sys
from controller import *


# Affiche la fenêtre au centre
os.environ["SDL_VIDEO_CENTERED"] = "1"

#execution sans argument -> affichage vue 
# python main.py [option..]
#  a : affichage
#  d : debug
#  s : simulation de n tour passsé à la suite
if len(sys.argv)>1 :
    controller = Controller(sys.argv[1], int(sys.argv[2]) if len(sys.argv)>2 else 1000)
else :
     controller = Controller()