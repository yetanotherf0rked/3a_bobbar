from math import ceil

import pygame
from pygame.locals import *

import ressources.config
from model import *
from view.gradient import Gradient
from .gui import *


class View:

    def __init__(self):
        self.config = ressources.config.para
        self.initView()
        self.run = False
        # 2 Attributs permettant de se déplacer dans la fenêtre
        self.depx = 0
        self.depy = 0
        self.zoom = 0

    def initView(self):
        # Initialisation de pygame
        pygame.init()
        # Calcul de la self.config.TAILLE de l'écran
        info = pygame.display.Info()
        self.width, self.height = info.current_w, info.current_h

        self.dim_menu = (220, int(self.height) - 10)
        simu_x, simu_y = self.width - self.dim_menu[0], int(self.height) - 10
        self.dim_simu = (simu_x, simu_y)

        # Ouverture de la fenêtre Pygame
        self.fenetre = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        self.fenetre = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                self.width, self.height = event.size

        # On distingue deux surfaces
        self.menu_surface = pygame.Surface(self.dim_menu)
        self.simu_surface = pygame.Surface(self.dim_simu)

        # Initialisation de la GUI
        self.gui = Gui(self.menu_surface)

        # Chargement de la food
        food = pygame.image.load(self.config.image_FOOD).convert_alpha()
        self.food = pygame.transform.scale(food, (40, 40))
        tree = pygame.image.load(self.config.image_TREE).convert_alpha()
        self.tree = pygame.transform.scale(tree, (40, 40))
        grass = pygame.image.load(self.config.image_GRASS).convert_alpha()
        self.grass = pygame.transform.scale(grass, (20, 20))
        # # Chargement des Bob
        # self.perso = pygame.image.load(image_BOB).convert_alpha()

        # Création d'un soleil
        self.soleil = Star()

    def draw_Stats(self,bob,xmax):
        #Initialisation text
        font = pygame.font.Font('freesansbold.ttf', 16)
        stats = bob.stats()
        label = []
        for line in stats:
            label.append(font.render(line, True, (255, 255, 255)))
        n = len(label)
        for line in range(n):
            self.simu_surface.blit(label[line], (xmax - 200, 20 + (line * 16) + (15 * line)))

    # Fonction d'affichage
    def affichage(self, world, tick):
        self.grid = world.grid
        self.listebob = world.listebob
        self.run = True

        # Resize des surfaces:
        self.dim_menu = (240, int(self.height))
        simu_x, simu_y = int((self.width - self.dim_menu[0])), int(self.height)
        self.dim_simu = (simu_x, simu_y)
        pygame.transform.scale(self.menu_surface, self.dim_menu)
        pygame.transform.scale(self.simu_surface, self.dim_simu)

        # Simu Update
        cote_x = (simu_x / 2 - 50) * (1 + 0.1 * self.zoom)
        cote_y = cote_x / 2.5
        PosX_init = 50 - 0.1 * self.zoom * (simu_x / 2 - 50)
        PosY_init = simu_y - 2 * cote_y - 125 + 0.1 * self.zoom * (simu_x / 2 - 50) / 2.5

        # Affichage du fond
        rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.simu_surface, (30, 200 - tick % 100, 255), rect)

        # Update et affichage Soleil
        self.soleil.updateListeX(cote_x)
        Pos = self.soleil.Pos(tick, cote_x, cote_y, PosX_init, PosY_init, self.depx, self.depy)
        self.soleil.blit = self.simu_surface.blit(self.soleil.image, Pos)

        # Affichage du sol
        pygame.draw.polygon(self.simu_surface, (123, 68, 48),
                            [(PosX_init + self.depx, PosY_init + cote_y + self.depy),
                             (PosX_init + cote_x + self.depx, PosY_init + 2 * cote_y + self.depy),
                             (PosX_init + cote_x + self.depx, PosY_init + 2 * cote_y + 50 + self.depy),
                             (PosX_init + self.depx, PosY_init + cote_y + 50 + self.depy)])
        pygame.draw.polygon(self.simu_surface, (97, 54, 38),
                            [(2 * cote_x + PosX_init + self.depx, PosY_init + cote_y + self.depy),
                             (PosX_init + cote_x + self.depx, PosY_init + 2 * cote_y + self.depy),
                             (PosX_init + cote_x + self.depx, PosY_init + 2 * cote_y + 50 + self.depy),
                             (PosX_init + 2 * cote_x + self.depx, PosY_init + cote_y + 50 + self.depy)])

        """Obligé de séparaer cette boucle de l'affichage du sol car elle change les cases."""
        caseliste = set()
        current_food = 0
        for bob in self.listebob:
            bob.see(self.grid, show=True)
            caseliste.add(self.grid[bob.x][bob.y])

        # Affichage du sol
        for y in range(self.config.TAILLE):
            xdec, ydec = cote_x / self.config.TAILLE, cote_y / self.config.TAILLE
            # if y == 0:
                # Affichages des lignes extérieures du haut
                # pygame.draw.line(self.simu_surface, (255, 155, 65),
                #                  (PosX_init + cote_x - xdec * y + self.depx, PosY_init + ydec * y + self.depy), (
                #                  PosX_init + 2 * cote_x - xdec * y + self.depx,
                #                  PosY_init + cote_y + ydec * y + self.depy), 5)
                # pygame.draw.line(self.simu_surface, (255, 155, 65),
                #                  (PosX_init + cote_x + xdec * y + self.depx, PosY_init + ydec * y + self.depy),
                #                  (PosX_init + xdec * y + self.depx, PosY_init + cote_y + ydec * y + self.depy), 5)
            for x in range(self.config.TAILLE):
                case = self.grid[x][y]
                if case.floor == "Grass":
                    case.draw(self.simu_surface, xdec, ydec, PosX_init, PosY_init, self.depx, self.depy, cote_x,self.tree)
                elif case.floor == "Water":
                    case.draw(self.simu_surface, xdec, ydec, PosX_init, PosY_init, self.depx, self.depy, cote_x,
                              self.grass)
                elif case.floor == "Sand":
                    case.draw(self.simu_surface, xdec, ydec, PosX_init, PosY_init, self.depx, self.depy, cote_x,
                              self.tree)
                elif case.floor == "Lava":
                    case.draw(self.simu_surface, xdec, ydec, PosX_init, PosY_init, self.depx, self.depy, cote_x,
                              self.tree)
                else:
                    case.draw(self.simu_surface, xdec, ydec, PosX_init, PosY_init, self.depx, self.depy, cote_x,None)
                n = min(5, ceil(case.food / self.config.ENERGY_FOOD))
                if n:
                    Pos = Case(0, 0).bobCase(n, x, y, xdec, ydec)
                    current_food += 1
                    for i in range(n):
                        PosX, PosY = Pos[i]
                        # Affichage de la food
                        self.simu_surface.blit(self.food, (
                        PosX_init + cote_x - 20 + PosX + self.depx, PosY_init - 30 + PosY + self.depy))

        # Affichages des lignes extérieures du bas
        # pygame.draw.line(self.simu_surface, (255, 155, 65), (PosX_init + self.depx, PosY_init + cote_y + self.depy),
        #                  (PosX_init + cote_x + self.depx, PosY_init + 2 * cote_y + self.depy), 5)
        # pygame.draw.line(self.simu_surface, (255, 155, 65),
        #                  (PosX_init + 2 * cote_x + self.depx, PosY_init + cote_y + self.depy),
        #                  (PosX_init + cote_x + self.depx, PosY_init + 2 * cote_y + self.depy), 5)
        # Life progress bar
        pos_life_bar = (4, 0)
        size_life_bar = (25, 5)
        # Affichage des Bobs
        for case in caseliste:
            case.place.sort(key=lambda x: x.masse, reverse=True)
            n = min(5, len(case.place))
            liste = case.place[0:n]
            x, y = liste[0].x, liste[0].y
            Pos = Case(0, 0).bobCase(n, x, y, xdec, ydec)
            for i in range(n):
                bob = liste[i]
                size = int(32 * bob.masse ** 2 - 16 * bob.masse + 16)
                if bob.bobController.select:
                    self.draw_Stats(bob,simu_x)
                    perso = pygame.transform.scale(bob.redImage, (32, size))
                else:
                    perso = pygame.transform.scale(bob.image, (32, size))
                PosX, PosY = Pos[i]
                # print(bob.life) stays at 1 (?)
                self.gui.progress_bar(pos_life_bar, size_life_bar, bob.life, perso, GREEN, True, RED, round=True,
                                      radius=3)
                bob.blit = self.simu_surface.blit(perso, (
                PosX_init + cote_x - 16 + PosX + self.depx, PosY_init + 7 - size + PosY + self.depy))
        if self.config.show_Minimap:
            xdec /= (1 + 0.1 * self.zoom)
            for y in range(self.config.TAILLE):
                for x in range(self.config.TAILLE):
                    self.grid[x][y].drawMap(self.simu_surface, xdec, 50)

        #### PROGRESS BARS ####

        # Progress bar day #
        # Useless since there's Star()
        # pos_bar_day = (0, 20)
        # size_bar_day = (self.simu_surface.get_width() - 10, 5)
        # progress_day = (tick % TICK_DAY) / 100
        # self.gui.progress_bar(pos_bar_day, size_bar_day, progress_day, self.simu_surface, BEER, round=True,
        #                       radius=3)

        # Progress bar food
        beer_image = pygame.image.load(self.config.image_EMPTY_BEER).convert_alpha()
        progress_beer = pygame.transform.scale(beer_image, (150, 150))
        pos_bar_food = (12, 5)
        size_bar_food = (
        progress_beer.get_width() - 67, progress_beer.get_height() - 12)  # 67 and 12 are arbitrary to fit the image
        progress_food = current_food / self.config.NB_FOOD if self.config.NB_FOOD != 0 else 0

        #  Get color palette
        beer_palette = Gradient(BEER_PALETTE, progress_beer.get_width()).gradient(int(progress_food * 100))

        #  Draw the bar
        self.gui.progress_bar(pos_bar_food, size_bar_food, progress_food, progress_beer, beer_palette, vertical=True,
                              reverse=True, round=True, radius=5)
        self.simu_surface.blit(progress_beer, (50, -150 + self.dim_simu[1]))
        # Affichage des surfaces dans la fenêtre
        self.fenetre.blit(self.simu_surface, (self.dim_menu[0], 0))
        self.fenetre.blit(self.menu_surface, (0, 0))

        # GUI update
        self.gui.update(update_stats(self.grid, self.listebob, tick))

        # Update
        pygame.display.flip()
        self.run = False

        ######### Backup branch progressbar ########

        # for bob in listebob:
        #     x, y = bob.x, bob.y
        #     # bob_surf = pygame.Surface((32, int(32*bob.masse**2 -16*bob.masse+16) + 20))
        #     # bob_surf.set_alpha(0)
        #     perso = pygame.transform.scale(self.perso, (32,int(32*bob.masse**2 -16*bob.masse+16)))
        #     # bob_surf.blit(perso,(32,int(32*bob.masse**2 -16*bob.masse+16) + 20))
