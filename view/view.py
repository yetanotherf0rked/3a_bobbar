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
        self.menu_surface = pygame.Surface(DIM_MENU)
        self.simu_surface = pygame.Surface(DIM_SIMU)

        # Initialisation de la GUI
        self.gui = Gui(self.menu_surface)

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
        self.simu_surface.fill(BLACK)  # fond noir

        # Affichage du sol
        for y in range(TAILLE):
            for x in range(TAILLE):
                self.simu_surface.blit(self.sol, (930 + x * 21 - 21 * y, 20 + y * 12 + x * 12))
                if not (grille[x][y].food == 0):
                    self.simu_surface.blit(self.food, (935 + x * 21 - 21 * y,3 + y * 12 + x * 12))

        # Affichage des Bobs
        for bob in listebob:
            x, y = bob.i, bob.j
            self.simu_surface.blit(self.perso, (939 + x * 21 - 21 * y, 8 + y * 12 + x * 12))

        # Affichage des surfaces dans la fenêtre
        self.fenetre.blit(self.simu_surface, POS_SURFACE_SIMU)
        self.fenetre.blit(self.menu_surface, POS_SURFACE_MENU)

        # Update
        pygame.display.flip()
        self.run = False