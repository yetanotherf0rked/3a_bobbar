import pygame
from random import randint
from ressources.constantes import *


class View:

    def __init__(self):
        self.initView()
        self.run = False

    def initView(self):
        # Initialisation de pygame
        pygame.init()

        # Ouverture de la fenêtre Pygame
        self.fenetre = pygame.display.set_mode((960 * 2, 540 * 2))
        fond = pygame.image.load(image_FOND).convert_alpha()
        self.fond = pygame.transform.scale(fond,(self.width,self.height))

        # Chargement et collage du fond
        # self.sol = pygame.image.load(image_SOL).convert_alpha()
        for i in range(1,7):
            exec("terre" +str(i)+ "= pygame.image.load(image_EARTH"+str(i)+").convert_alpha()")
            exec("self.terre"+str(i)+" = pygame.transform.scale(terre"+str(i)+" , (40,40))")
        food = pygame.image.load(image_FOOD).convert_alpha()
        self.food = pygame.transform.scale(food , (40,40))

        self.grilleFond = [[randint(1,6) for i in range(TAILLE)] for j in range(TAILLE)]

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
                # self.fenetre.blit(self.sol, (930 + x * 21 - 21 * y,20 + y * 12 + x * 12))
                eval("self.fenetre.blit(self.terre" +str(self.grilleFond[x][y])+", (930 + " +str(x)+" * 18 - 18 * "+str(y)+", 8 + "+str(y)+"* 13.7 + "+str(x)+" * 13.7))")
                if not(grille[x][y].food ==0):
                    self.fenetre.blit(self.food, (int(self.width/2)-30 + x * 18 - 18 * y,-5 + y * 13.7 + x * 13.7))
        # self.fenetre.blit(self.grass, (935 + 0 * 21 - 21 * 0, 500 + 8 + 0 * 12 + 0 * 12))
        # Affichage des Bobs
        for bob in listebob:
            x, y = bob.i, bob.j
            perso = pygame.transform.scale(self.perso , (32,int(8*bob.energy**(1/3))))
            self.fenetre.blit(perso, (int(self.width/2)-26 + x * 18 - 18 * y,2 + y * 13.7 + x * 13.7))
        # Update
        pygame.display.flip()
        self.run = False