import pygame
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

        # Chargement et collage du fond
        self.sol = pygame.image.load(image_SOL).convert_alpha()
        food = pygame.image.load(image_FOOD).convert_alpha()
        self.food = pygame.transform.scale(food , (40,40))

        # Chargement et collage des Bob
        self.perso = pygame.image.load(image_BOB).convert_alpha()

    # Fonction d'affichage
    def affichage(self,grille,listebob):
        self.run = True
        # Affichage du fond
        self.fenetre.fill((0, 0, 0))
        # Affichage du sol
        for y in range(TAILLE):
            for x in range(TAILLE):
                self.fenetre.blit(self.sol, (930 + x * 21 - 21 * y,20 + y * 12 + x * 12))
                if not(grille[x][y].food ==0):
                    self.fenetre.blit(self.food, (935 + x * 21 - 21 * y,3 + y * 12 + x * 12))
        # Affichage des Bobs
        for bob in listebob:
            x, y = bob.i, bob.j
            self.fenetre.blit(self.perso, (939 + x * 21 - 21 * y,8 + y * 12 + x * 12))
        # Update
        pygame.display.flip()
        self.run = False