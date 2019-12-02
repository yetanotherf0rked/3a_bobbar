import pygame
from ressources.constantes import *
from .gui import *

class View:

    def __init__(self):
        self.initView()
        self.run = False

    def initView(self):
        # Initialisation de pygame
        pygame.init()

        # Ouverture de la fenêtre Pygame
        self.fenetre = pygame.display.set_mode(DIM_WINDOW)

        # On distingue deux surfaces
        self.menuSurface = pygame.Surface(DIM_MENU)
        self.simuSurface = pygame.Surface(DIM_SIMU)

        # Initialisation de la GUI
        self.gui = Gui(self.menuSurface)

        # Chargement et collage du fond
        self.sol = pygame.image.load(image_SOL).convert_alpha()
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
        self.simuSurface.fill(BLACK)  # fond noir

        # Affichage du sol
        for y in range(TAILLE):
            for x in range(TAILLE):
                self.simuSurface.blit(self.sol, (930 + x * 21 - 21 * y, 20 + y * 12 + x * 12))
                if not (grille[x][y].food == 0):
                    self.simuSurface.blit(self.food, (935 + x * 21 - 21 * y,3 + y * 12 + x * 12))

        # Affichage des Bobs
        for bob in listebob:
            x, y = bob.i, bob.j
            self.simuSurface.blit(self.perso, (939 + x * 21 - 21 * y, 8 + y * 12 + x * 12))

        # Affichage des surfaces dans la fenêtre
        self.fenetre.blit(self.simuSurface, POS_SURFACE_SIMU)
        self.fenetre.blit(self.menuSurface, POS_SURFACE_MENU)

        # Update
        pygame.display.flip()
        self.run = False