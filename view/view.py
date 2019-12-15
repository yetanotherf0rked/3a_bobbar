import pygame
from random import randint
from pygame.locals import RESIZABLE
from ressources.constantes import *
from .gui import *
from view.gradient import Gradient

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

        # On distingue deux surfaces
        self.menu_surface = pygame.Surface(DIM_MENU)
        self.simu_surface = pygame.Surface(DIM_SIMU)

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
        self.gui.update()

        # Simu Update
        self.simu_surface.blit(self.fond , (0 , 0))

        current_food = 0

        # Affichage du sol
        for y in range(TAILLE):
            for x in range(TAILLE):
                self.simu_surface.blit(self.grilleFond[x][y], (int(self.width/2)-30 + self.depx + x * 18 - 18 * y,self.depy+ 8 + y* 13.7 + x * 13.7))
                if grille[x][y].food:
                    current_food += 1
                    self.simu_surface.blit(self.food, (int(self.width/2) + self.depx -30 + x * 18 - 18 * y,self.depy-5 + y * 13.7 + x * 13.7))
        # Affichage des Bobs
        for bob in listebob:
            x, y = bob.x, bob.y
            # bob_surf = pygame.Surface((32, int(32*bob.masse**2 -16*bob.masse+16) + 20))
            # bob_surf.set_alpha(0)
            perso = pygame.transform.scale(self.perso, (32,int(32*bob.masse**2 -16*bob.masse+16)))
            # bob_surf.blit(perso,(32,int(32*bob.masse**2 -16*bob.masse+16) + 20))

            # Life progress bar
            pos_life_bar = (0, 0)
            size_life_bar = (25, 5)
            progress_life_bar = (bob.energy % ENERGY_MAX)/100
            self.gui.progress_bar(pos_life_bar, size_life_bar, progress_life_bar, perso, GREEN, True, RED, round=True, radius=3)
            self.simu_surface.blit(perso, (int(self.width/2) + self.depx - 26 + x * 18 - 18 * y,self.depy + 2 + y * 13.7 + x * 13.7))


        #### PROGRESS BARS ####

        # Progress bar day
        pos_bar_day = (0, 20)
        size_bar_day = (self.simu_surface.get_width() - 10, 5)
        progress_day = (tick % TICK_DAY)/100
        self.gui.progress_bar(pos_bar_day, size_bar_day, progress_day, self.simu_surface, BEER, round=True, radius=3)

        # Progress bar food
        beer_image = pygame.image.load(image_EMPTY_BEER).convert_alpha()
        progress_beer = pygame.transform.scale(beer_image, (200, 200))
        pos_bar_food = (12, 5)
        size_bar_food = (progress_beer.get_width() - 67, progress_beer.get_height() - 12)
        progress_food = (current_food/NB_FOOD) % TICK_DAY
        #  Get color palette
        beer_palette = Gradient(BEER_PALETTE, progress_beer.get_width()).gradient(int(progress_food*100))

        #  Draw the bar
        self.gui.progress_bar(pos_bar_food, size_bar_food, progress_food, progress_beer, beer_palette, vertical=True, reverse=True, round=True, radius=5)
        self.simu_surface.blit(progress_beer, (35, 50))

        # Affichage des surfaces dans la fenêtre
        self.fenetre.blit(self.simu_surface, POS_SURFACE_SIMU)
        self.fenetre.blit(self.menu_surface, POS_SURFACE_MENU)

        # Update
        pygame.display.flip()
        self.run = False