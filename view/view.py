import pygame
from random import randint
from pygame.locals import RESIZABLE
from ressources.config import *
from .gui import *
from model import *

class View:

    def __init__(self):
        self.initView()
        self.run = False
        # 2 Attributs permettant de se déplacer dans la fenêtre
        self.depx = 0
        self.depy = 0

    def initView(self):

        # Initialisation de pygame
        pygame.init()

        #Calcul de la taille de l'écran
        info = pygame.display.Info()
        self.width, self.height = info.current_w, info.current_h

        self.dim_menu = (220 , int(self.height))
        simu_x, simu_y = self.width - self.dim_menu[0], int(self.height)
        self.dim_simu = (simu_x, simu_y)

        # Ouverture de la fenêtre Pygame
        self.fenetre = pygame.display.set_mode((self.width, self.height),RESIZABLE)

        # On distingue deux surfaces
        self.menu_surface = pygame.Surface(self.dim_menu)
        self.simu_surface = pygame.Surface(self.dim_simu)

        # Initialisation de la GUI
        self.gui = Gui(self.menu_surface)

        #Chargement de la food
        food = pygame.image.load(image_FOOD).convert_alpha()
        self.food = pygame.transform.scale(food, (40, 40))
        # # Chargement des Bob
        # self.perso = pygame.image.load(image_BOB).convert_alpha()

        #Création d'un soleil
        self.soleil = Soleil()

    # Fonction d'affichage
    def affichage(self, grille, tick):
        self.run = True

        #Resize des surfaces:
        self.dim_menu = (220, int(self.height))
        simu_x, simu_y = self.width - self.dim_menu[0], int(self.height)
        self.dim_simu = (simu_x, simu_y)
        pygame.transform.scale(self.menu_surface, self.dim_menu)
        pygame.transform.scale(self.simu_surface, self.dim_simu)

        # Simu Update
        cote_x = simu_x/2 - 50
        cote_y = cote_x/2.5
        PosX_init = 50
        PosY_init = simu_y - 2*cote_y - 125

        #Affichage du fond
        rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.simu_surface, (30, 200 - tick % 100, 255), rect)

        # Update et affichage Soleil
        self.soleil.updateListeX(cote_x)
        Pos = self.soleil.Pos(tick, cote_x, cote_y,PosX_init,PosY_init,self.depx,self.depy)
        self.soleil.blit = self.simu_surface.blit(self.soleil.image, Pos)

        #Affichage du sol
        pygame.draw.polygon(self.simu_surface, (159, 158, 159), [(PosX_init + self.depx,PosY_init + cote_y +self.depy), (PosX_init + cote_x + self.depx,PosY_init + 2*cote_y+self.depy), (PosX_init + cote_x + self.depx,PosY_init + 2* cote_y + 50 +self.depy), (PosX_init + self.depx,PosY_init + cote_y + 50 +self.depy)])
        pygame.draw.polygon(self.simu_surface, (159, 158, 159), [(2* cote_x + PosX_init + self.depx,PosY_init + cote_y +self.depy), (PosX_init + cote_x + self.depx,PosY_init + 2*cote_y +self.depy), (PosX_init + cote_x + self.depx,PosY_init + 2*cote_y +50 +self.depy), (PosX_init + 2* cote_x + self.depx,PosY_init + cote_y + 50 +self.depy)])

        # Affichage du sol
        caseliste = []
        for y in range(TAILLE):
            xdec, ydec = cote_x / TAILLE, cote_y / TAILLE
            if y == 0:
                # Affichages des lignes extérieurs du haut
                pygame.draw.line(self.simu_surface, (255, 155, 65), (PosX_init + cote_x - xdec * y+ self.depx, PosY_init + ydec * y+self.depy),(PosX_init + 2* cote_x - xdec * y+ self.depx, PosY_init + cote_y + ydec * y+self.depy),5)
                pygame.draw.line(self.simu_surface, (255, 155, 65), (PosX_init + cote_x + xdec * y+ self.depx, PosY_init + ydec * y+self.depy),(PosX_init + xdec * y+ self.depx, PosY_init + cote_y + ydec * y+self.depy),5)
            for x in range(TAILLE):
                grille[x][y].draw(self.simu_surface, xdec, ydec, PosX_init, PosY_init, self.depx, self.depy, cote_x)
                n = min(5,int(grille[x][y].food // parameters.get("Food Energy")))
                if not(n ==0):
                    Pos = Case(0,0).bobCase(n, x, y, xdec, ydec)
                    for i in range(n):
                        PosX, PosY = Pos[i]
                        #Affichage de la food
                        self.simu_surface.blit(self.food, (PosX_init + cote_x - 20 + PosX + self.depx, PosY_init - 30 + PosY + self.depy))
                #Ajout de tout les bobs de la case à bobliste
                if grille[x][y].place != []:
                    l = [bob for bob in grille[x][y].place]
                    l.sort(key = lambda x:x.masse, reverse = True)
                    caseliste.append(l)

        #Affichages des lignes extérieurs du bas
        pygame.draw.line(self.simu_surface, (255, 155, 65), (PosX_init+self.depx, PosY_init + cote_y + self.depy),(PosX_init + cote_x + self.depx, PosY_init + 2* cote_y + self.depy),5)
        pygame.draw.line(self.simu_surface, (255,155,65), (PosX_init + 2* cote_x + self.depx, PosY_init + cote_y + self.depy),(PosX_init + cote_x + self.depx,PosY_init + 2* cote_y + self.depy),5)

        # Affichage des Bobs
        self.bobliste = []
        for case in caseliste:
            n = min(5,len(case))
            liste = case[0:n]
            x, y = liste[0].x, liste[0].y
            Pos = Case(0,0).bobCase(n,x,y,xdec,ydec)
            for i in range(n):
                bob = liste[i]
                size = int(32*bob.masse**2 -16*bob.masse+16)
                if bob.bobController.select:
                    perso = pygame.transform.scale(bob.redImage, (32, size))
                else:
                    perso = pygame.transform.scale(bob.image, (32,size))
                PosX , PosY = Pos[i]
                bob.blit = self.simu_surface.blit(perso, (PosX_init + cote_x - 16 + PosX + self.depx,PosY_init + 7 - size + PosY + self.depy))
                self.bobliste.append(bob)
        # Affichage des surfaces dans la fenêtre
        self.fenetre.blit(self.simu_surface, (self.dim_menu[0], 0))
        self.fenetre.blit(self.menu_surface, (0, 0))

        # GUI update
        self.gui.update(update_stats(grille, self.bobliste, tick))

        # Update
        pygame.display.flip()
        self.run = False