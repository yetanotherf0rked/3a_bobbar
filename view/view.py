import pygame
from random import randint
from pygame.locals import RESIZABLE
from ressources.constantes import *
from .gui import *

class View:

    def __init__(self):
        self.initView()
        self.run = False
        # 2 Attributs permettant de ce déplacer dans la fenêtre.
        self.depx = 0
        self.depy = 0

    def initView(self):
        # Initialisation de pygame
        pygame.init()
        #Calcul de la taille de l'écran
        info = pygame.display.Info()
        self.width,self.height = info.current_w,info.current_h

        # Ouverture de la fenêtre Pygame
        self.fenetre = pygame.display.set_mode((self.width, self.height),RESIZABLE)

        # On distingue deux surfaces
        self.menu_surface = pygame.Surface(DIM_MENU)
        self.simu_surface = pygame.Surface(DIM_SIMU)

        # Initialisation de la GUI
        self.gui = Gui(self.menu_surface)

        #Chargement de la food
        food = pygame.image.load(image_FOOD).convert_alpha()
        self.food = pygame.transform.scale(food, (40, 40))
        # Chargement et collage des Bob
        self.perso = pygame.image.load(image_BOB).convert_alpha()

    # Fonction d'affichage
    def affichage(self,grille,listebob):
        self.run = True

        # GUI update
        self.gui.update()

        # Simu Update
        rect = pygame.Rect(0,0,self.width,self.height)
        pygame.draw.rect(self.simu_surface,(40,233,242),rect)
        pygame.draw.polygon(self.simu_surface, (38, 37, 42), [(50+ self.depx,500+self.depy),(850+ self.depx,100+self.depy),(1650+ self.depx,500+self.depy),(850+ self.depx,900+self.depy)]) #1600*800
        pygame.draw.polygon(self.simu_surface, (159, 158, 159), [(50+ self.depx, 500+self.depy), (850+ self.depx, 900+self.depy), (850+ self.depx, 950+self.depy), (50+ self.depx, 550+self.depy)])
        pygame.draw.polygon(self.simu_surface, (159, 158, 159), [(1650+ self.depx, 500+self.depy), (850+ self.depx, 900+self.depy), (850+ self.depx, 950+self.depy), (1650+ self.depx, 550+self.depy)])

        # Affichage du sol
        bobliste = []
        for y in range(TAILLE):
            xdec, ydec = 800 / TAILLE, 800 / (2 * TAILLE)
            if y == 0:
                pygame.draw.line(self.simu_surface, (255, 155, 65), (850 - xdec * y+ self.depx, 100 + ydec * y+self.depy),(1650 - xdec * y+ self.depx, 500 + ydec * y+self.depy),5)
                pygame.draw.line(self.simu_surface, (255, 155, 65), (850 + xdec * y+ self.depx, 100 + ydec * y+self.depy),(50 + xdec * y+ self.depx, 500 + ydec * y+self.depy),5)
            #Lignes Haut-Gauche
            pygame.draw.line(self.simu_surface, (228, 226, 232), (850 - xdec * y+ self.depx, 100 + ydec * y+self.depy),(1650 - xdec * y+ self.depx, 500 + ydec * y+self.depy))
            #Lignes Haut-Droite
            pygame.draw.line(self.simu_surface, (228, 226, 232), (850 + xdec * y+ self.depx, 100 + ydec * y+self.depy), (50 + xdec * y+ self.depx, 500 + ydec * y+self.depy))
            for x in range(TAILLE):
                if not(grille[x][y].food ==0):
                    self.simu_surface.blit(self.food, (850 - 20 + xdec * (x - y) + self.depx, 100 - 30 + ydec * (x + y + 1) + self.depy))
                for bob in grille[x][y].place:
                    bobliste.append(bob)
        pygame.draw.line(self.simu_surface, (255, 155, 65), (50+self.depx, 500+self.depy),(850+self.depx, 900+self.depy),5)
        pygame.draw.line(self.simu_surface, (255,155,65), (1650+self.depx, 500+self.depy),(850+self.depx,900+self.depy),5)
        # Affichage des Bobs
        for bob in bobliste:
            x, y = bob.x, bob.y
            size = int(32*bob.masse**2 -16*bob.masse+16)
            perso = pygame.transform.scale(self.perso, (32,size))
            self.simu_surface.blit(perso, (850 - 16 + xdec * (x - y) + self.depx,107 - size + ydec * (x + y + 1) + self.depy))
        # Affichage des surfaces dans la fenêtre
        self.fenetre.blit(self.simu_surface, POS_SURFACE_SIMU)
        self.fenetre.blit(self.menu_surface, POS_SURFACE_MENU)

        # Update
        pygame.display.flip()
        self.run = False