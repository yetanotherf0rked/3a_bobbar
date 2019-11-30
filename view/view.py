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
            element.surface = self.surf1
        self.gui.update()
        # On utilise les éléments normalement
        self.gui.box.set_topleft((0, 0))

    def initView(self):
        # Initialisation de pygame
        pygame.init()

        # Ouverture de la fenêtre Pygame
        self.fenetre = pygame.display.set_mode((960 * 2, 540 * 2))

        # GUI-purpose : on distingue deux surfaces (1 : paramètres et 2 : simulation)
        self.surf1 = pygame.Surface((500, 540 * 2))  # taille de ma surface
        self.surf2 = pygame.Surface((1620, 540 * 2))

        # On remplit les deux surfaces avec un fond noir
        self.surf1.fill((0, 0, 0))
        self.surf2.fill((0, 0, 0))

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
        self.surf2.fill((0, 0, 0)) #fond noir
        self.gui.update()

        # Affichage du sol
        for y in range(TAILLE):
            for x in range(TAILLE):
                self.surf2.blit(self.sol, (930 + x * 21 - 21 * y, 20 + y * 12 + x * 12))
                if not (grille[x][y].food == 0):
                    self.surf2.blit(self.food, (935 + x * 21 - 21 * y,3 + y * 12 + x * 12))

        # Affichage des Bobs
        for bob in listebob:
            x, y = bob.i, bob.j
            self.surf2.blit(self.perso, (939 + x * 21 - 21 * y, 8 + y * 12 + x * 12))

        # Affichage des surfaces dans la fenêtre
        self.fenetre.blit(self.surf2, (501, 0))
        self.fenetre.blit(self.surf1, (0, 0))

        # Update
        pygame.display.flip()
        self.run = False