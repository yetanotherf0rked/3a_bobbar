from ressources.constantes import *
import numpy as np
import pygame

class Soleil():

    def __init__(self):
        # Chargement du Soleil
        soleil = pygame.image.load(image_SOLEIL).convert_alpha()
        self.image = pygame.transform.scale(soleil, (100, 100))
        self.blit = None

    def y_function(self,x,cx,cy):
        a = (cy + 100) / ((80 - cx) ** 2)
        return a * (x - cx) ** 2 + 50

    def updateListeX(self,cx):
        self.ListeX = np.linspace(80, 2 * cx - 80, TICK_DAY)

    def Pos(self,tick,cx,cy):
        x = self.ListeX[tick % TICK_DAY]
        y = self.y_function(x, cx, cy)
        return (x,y)