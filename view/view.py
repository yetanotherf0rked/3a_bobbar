import pygame
from random import randint
from pygame.locals import RESIZABLE
from ressources.constantes import *


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
        fond = pygame.image.load(image_FOND).convert_alpha()
        self.fond = pygame.transform.scale(fond,(self.width,self.height))

        # Chargement et collage du fond
        # self.sol = pygame.image.load(image_SOL).convert_alpha()
        for i in range(1,7):
            exec("terre" +str(i)+ "= pygame.image.load(image_EARTH"+str(i)+").convert_alpha()")
            exec("self.terre"+str(i)+" = pygame.transform.scale(terre"+str(i)+" , (40,40))")
        food = pygame.image.load(image_FOOD).convert_alpha()
        self.food = pygame.transform.scale(food , (40,40))

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
    def affichage(self,grille,listebob):
        self.run = True
        # Affichage du fond
        self.fenetre.fill((0, 0, 0))
        self.fenetre.blit(self.fond , (0 , 0))
        # Affichage du sol
        for y in range(TAILLE):
            for x in range(TAILLE):
                self.fenetre.blit(self.grilleFond[x][y], (int(self.width/2)-30 + self.depx + x * 18 - 18 * y,self.depy+ 8 + y* 13.7 + x * 13.7))
                if not(grille[x][y].food ==0):
                    self.fenetre.blit(self.food, (int(self.width/2) + self.depx -30 + x * 18 - 18 * y,self.depy-5 + y * 13.7 + x * 13.7))
        # Affichage des Bobs
        for bob in listebob:
            x, y = bob.x, bob.y
            perso = pygame.transform.scale(self.perso, (32,int(32*bob.masse**2 -16*bob.masse+16)))
            self.fenetre.blit(perso, (int(self.width/2) + self.depx -26 + x * 18 - 18 * y,self.depy + 2 + y * 13.7 + x * 13.7))
        # Update
        pygame.display.flip()
        self.run = False