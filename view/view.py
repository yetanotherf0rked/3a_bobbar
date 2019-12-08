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

        self.dim_menu = (int(self.width * 0.1) , int(self.height))
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
        # Chargement et collage des Bob
        self.perso = pygame.image.load(image_BOB).convert_alpha()

    # Fonction d'affichage
    def affichage(self,grille):
        self.run = True

        #Resize des surfaces:
        self.dim_menu = (int(self.width * 0.1) , int(self.height))
        simu_x, simu_y = self.width - self.dim_menu[0], int(self.height)
        self.dim_simu = (simu_x, simu_y)
        pygame.transform.scale(self.menu_surface, self.dim_menu)
        pygame.transform.scale(self.simu_surface, self.dim_simu)

        # GUI update
        self.gui.update()

        # Simu Update
        cote_x = simu_x/2 - 50
        cote_y = simu_y/2 - 100
        rect = pygame.Rect(0,0,self.width,self.height)
        pygame.draw.rect(self.simu_surface,(40,233,242),rect)
        pygame.draw.polygon(self.simu_surface, (38, 37, 42), [(50 + self.depx,50 + cote_y +self.depy),(50 + cote_x + self.depx, 50 + self.depy),(50 + 2* cote_x + self.depx, 50 + cote_y + self.depy),(50 + cote_x + self.depx,50 + 2*cote_y+ self.depy)]) #1600*800
        pygame.draw.polygon(self.simu_surface, (159, 158, 159), [(50 + self.depx,50 + cote_y +self.depy), (50 + cote_x + self.depx,50 + 2*cote_y+self.depy), (50 + cote_x + self.depx,50 + 2* cote_y + 50 +self.depy), (50 + self.depx,50 + cote_y + 50 +self.depy)])
        pygame.draw.polygon(self.simu_surface, (159, 158, 159), [(2* cote_x + 50 + self.depx,50 + cote_y +self.depy), (50 + cote_x + self.depx,50 + 2*cote_y +self.depy), (50 + cote_x + self.depx,50 + 2*cote_y +50 +self.depy), (50 + 2* cote_x + self.depx,50 + cote_y + 50 +self.depy)])

        # Affichage du sol
        bobliste = []
        for y in range(TAILLE):
            xdec, ydec = cote_x / TAILLE, cote_y / TAILLE
            if y == 0:
                # Affichages des lignes extérieurs du haut
                pygame.draw.line(self.simu_surface, (255, 155, 65), (50 + cote_x - xdec * y+ self.depx, 50 + ydec * y+self.depy),(50 + 2* cote_x - xdec * y+ self.depx, 50 + cote_y + ydec * y+self.depy),5)
                pygame.draw.line(self.simu_surface, (255, 155, 65), (50 + cote_x + xdec * y+ self.depx, 50 + ydec * y+self.depy),(50 + xdec * y+ self.depx, 50 + cote_y + ydec * y+self.depy),5)

            #Lignes Haut-Gauche
            pygame.draw.line(self.simu_surface, (228, 226, 232), (50 + cote_x - xdec * y+ self.depx, 50 + ydec * y+self.depy),(50 + 2* cote_x - xdec * y+ self.depx, 50 + cote_y + ydec * y+self.depy))

          #Lignes Haut-Droite
            pygame.draw.line(self.simu_surface, (228, 226, 232), (50 + cote_x + xdec * y+ self.depx, 50 + ydec * y+self.depy), (50 + xdec * y+ self.depx, 50 + cote_y + ydec * y+self.depy))

            for x in range(TAILLE):
                n = min(5,int(grille[x][y].food // parameters.get("Food Energy")))
                if not(n ==0):
                    Pos = self.bobCase(n, x, y, xdec, ydec)
                    for i in range(n):
                        PosX, PosY = Pos[i]
                        #Affichage de la food
                        self.simu_surface.blit(self.food, (50 + cote_x - 20 + PosX + self.depx, 50 - 30 + PosY + self.depy))
                #Ajout de tout les bobs de la case à bobliste
                if grille[x][y].place != []:
                    # print("Grille = ",grille[x][y].place)
                    l = [bob for bob in grille[x][y].place]
                    l.sort(key = lambda x:x.masse, reverse = True)
                    bobliste.append(l)

        #Affichages des lignes extérieurs du bas
        pygame.draw.line(self.simu_surface, (255, 155, 65), (50+self.depx, 50 + cote_y + self.depy),(50 + cote_x + self.depx, 50 + 2* cote_y + self.depy),5)
        pygame.draw.line(self.simu_surface, (255,155,65), (50 + 2* cote_x + self.depx, 50 + cote_y + self.depy),(50 + cote_x + self.depx,50 + 2* cote_y + self.depy),5)

        # print(bobliste)
        # Affichage des Bobs
        for case in bobliste:
            n = min(5,len(case))
            liste = case[0:n]
            # print(liste)
            x, y = liste[0].x, liste[0].y
            Pos = self.bobCase(n,x,y,xdec,ydec)
            for i in range(n):
                size = int(32*liste[i].masse**2 -16*liste[i].masse+16)
                perso = pygame.transform.scale(self.perso, (32,size))
                PosX , PosY = Pos[i]
                self.simu_surface.blit(perso, (50 + cote_x - 16 + PosX + self.depx,57 - size + PosY + self.depy))
        # Affichage des surfaces dans la fenêtre
        self.fenetre.blit(self.simu_surface, (self.dim_menu[0], 0))
        self.fenetre.blit(self.menu_surface, (0, 0))

        # Update
        pygame.display.flip()
        self.run = False


    def bobCase(self,n,x,y,xdec,ydec):
        if n == 1:
            return [(xdec * (x - y),ydec * (x + y + 1))]
        if n == 2:
            return [(xdec * (x - y - 1/4),ydec * (x + y + 1 - 1/4)),
                    (xdec * (x - y + 1/4),ydec * (x + y + 1 + 1/4))]
        if n == 3:
            return [(xdec * (x - y),ydec * (x + y + 1 - 1/4)),
                    (xdec * (x - y - 1/4),ydec * (x + y + 1 + 1/4)),
                    (xdec * (x - y + 1/4),ydec * (x + y + 1 + 1/4))]
        if n == 4:
            return [(xdec * (x - y - 1 / 4), ydec * (x + y + 1 - 1 / 4)),
                    (xdec * (x - y + 1 / 4), ydec * (x + y + 1 - 1 / 4)),
                    (xdec * (x - y - 1 / 4), ydec * (x + y + 1 + 1 / 4)),
                    (xdec * (x - y + 1 / 4), ydec * (x + y + 1 + 1 / 4))]
        if n == 5:
            return [(xdec * (x - y - 1 / 4), ydec * (x + y + 1 - 1 / 4)),
                    (xdec * (x - y + 1 / 4), ydec * (x + y + 1 - 1 / 4)),
                    (xdec * (x - y), ydec * (x + y + 1)),
                    (xdec * (x - y - 1 / 4), ydec * (x + y + 1 + 1 / 4)),
                    (xdec * (x - y + 1 / 4), ydec * (x + y + 1 + 1 / 4))]