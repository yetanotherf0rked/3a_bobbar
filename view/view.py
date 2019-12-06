import pygame
from random import randint
from pygame.locals import RESIZABLE
from ressources.config import *
from .gui import *

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

        # Déclaration des couples de dimensions en fonction de la taille de l'écran
        DIM_FENETRE = (self.width, self.height)
        DIM_MENU_SURFACE = (DIM_MENU_X, self.height)
        DIM_SIMU_SURFACE = (self.width - DIM_MENU_X, self.height)

        # Ouverture de la fenêtre Pygame
        if FULLSCREEN:
            self.fenetre = pygame.display.set_mode(DIM_FENETRE, pygame.FULLSCREEN)
        else:
            self.fenetre = pygame.display.set_mode(DIM_FENETRE, RESIZABLE)

        fond = pygame.image.load(image_FOND).convert_alpha()
        self.fond = pygame.transform.scale(fond, DIM_FENETRE)

        # On distingue deux surfaces
        self.menu_surface = pygame.Surface(DIM_MENU_SURFACE)
        self.simu_surface = pygame.Surface(DIM_SIMU_SURFACE)

        # Initialisation de la GUI
        self.gui = Gui(self.menu_surface)

        # Chargement et collage du fond
        # self.sol = pygame.image.load(image_SOL).convert_alpha()
        for i in range(1,7):
            exec("terre" +str(i)+ "= pygame.image.load(image_EARTH"+str(i)+").convert_alpha()")
            exec("self.terre"+str(i)+" = pygame.transform.scale(terre"+str(i)+" , (40,40))")
        food = pygame.image.load(image_FOOD).convert_alpha()
        self.food = pygame.transform.scale(food, (40, 40))

        #Initialisation grilleFond avec le fond random
        self.grilleFond = []
        for y in range(TAILLE):
            liste = []
            for x in range(TAILLE):
                i = randint(1,6)
                eval("liste.append(self.terre" + str(i) + ")")
            self.grilleFond.append(liste)

        # Chargement et collage des Bob
        self.perso = pygame.image.load(image_BOB).convert_alpha()
        # self.perso = pygame.transform.scale(perso , (25,25))

    # Fonction d'affichage
    def affichage(self, grille, listebob, tick):
        self.run = True

        # GUI update
        self.gui.update(update_stats(grille, listebob, tick))

        # Simu Update
        self.simu_surface.blit(self.fond, (0, 0))

        # Affichage du sol
        for y in range(TAILLE):
            for x in range(TAILLE):
                self.simu_surface.blit(self.grilleFond[x][y], (int(self.width/2)-30 + self.depx + x * 18 - 18 * y,self.depy+ 8 + y* 13.7 + x * 13.7))
                if not(grille[x][y].food ==0):
                    self.simu_surface.blit(self.food, (int(self.width/2) + self.depx -30 + x * 18 - 18 * y,self.depy-5 + y * 13.7 + x * 13.7))

        # Affichage des Bobs
        for bob in listebob:
            x, y = bob.x, bob.y
            perso = pygame.transform.scale(self.perso, (32,int(32*bob.masse**2 -16*bob.masse+16)))
            self.simu_surface.blit(perso, (int(self.width/2) + self.depx -26 + x * 18 - 18 * y,self.depy + 2 + y * 13.7 + x * 13.7))

        # Affichage des surfaces dans la fenêtre
        self.fenetre.blit(self.simu_surface, POS_SURFACE_SIMU)
        self.fenetre.blit(self.menu_surface, POS_SURFACE_MENU)

        # GUI update
        self.gui.update(update_stats(grille, listebob, tick))

        print(tick)
        # Update
        pygame.display.flip()
        self.run = False