import pygame
from ressources.constantes import *
from .gui import *

class View:

    def __init__(self):
        self.initView()
        self.run = False

    def initGui(self):
        """initGui : affecte l'interface gui à la surface surf1"""
        # On définit surf1 comme la surface de l'interface GUI
        for element in self.gui.menu.get_population():
            element.surface = self.menuSurface
        self.gui.update()
        # On utilise les éléments normalement
        # On affiche le logo
        self.logo = pygame.image.load(image_LOGO).convert_alpha()
        self.menuSurface.blit(self.logo, (0, 0))
        self.gui.box.set_topleft((0, 221))

    def initView(self):
        # Initialisation de pygame
        pygame.init()

        # Ouverture de la fenêtre Pygame
        self.fenetre = pygame.display.set_mode(DIM_WINDOW)

        # GUI-purpose : on distingue trois surfaces (logo, menu, simulation)
        # self.logoSurface = pygame.Surface(DIM_LOGO)
        self.menuSurface = pygame.Surface((220, 540*2))
        self.simuSurface = pygame.Surface(DIM_SIMU)

        # On remplit les trois surfaces avec un fond noir
        self.menuSurface.fill(BLACK)
        self.simuSurface.fill(BLACK)

        # On affiche le logo
        # self.logo = pygame.image.load(image_LOGO).convert_alpha()
        # self.menuSurface.blit(self.logo, (0, 0))


        # Initialisation de la GUI
        self.gui = Gui()
        self.initGui()

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
        self.simuSurface.fill(BLACK) #fond noir
        self.gui.update()

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
        # self.fenetre.blit(self.logoSurface, POS_SURFACE_LOGO)
        self.fenetre.blit(self.simuSurface, POS_SURFACE_SIMU)
        self.fenetre.blit(self.menuSurface, (0, 0))

        # Update
        pygame.display.flip()
        self.run = False