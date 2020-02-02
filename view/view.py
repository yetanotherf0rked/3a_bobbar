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
        self.velocity_max = -1

    def initView(self):
        # Initialisation de pygame
        pygame.init()
        pygame.display.set_caption("BobBar")
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
        self.foodImage = pygame.image.load(self.config.image_FOOD).convert_alpha()
        tree = pygame.image.load(self.config.image_TREE).convert_alpha()
        self.tree = pygame.transform.scale(tree, (40, 40))
        grass = pygame.image.load(self.config.image_GRASS).convert_alpha()
        self.grass = pygame.transform.scale(grass, (20, 20))
        # # Chargement des Bob
        # self.perso = pygame.image.load(image_BOB).convert_alpha()

        self.beer_image = pygame.image.load(self.config.image_EMPTY_BEER).convert_alpha()

        # Création d'un soleil
        self.soleil = Star()

    def draw_Stats(self, bob, xmax):
        # Initialisation text
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

        # Initialisation of the view
        PosX_init, PosY_init, cote_x, cote_y, simu_x, xdec, ydec = self.init_view(tick)

        # Update et affichage Soleil
        self.soleil.updateListeX(cote_x)
        Pos = self.soleil.Pos(tick, cote_x, cote_y, PosX_init, PosY_init, self.depx, self.depy)
        self.soleil.blit = self.simu_surface.blit(self.soleil.image, Pos)

        # Affichage du sol en 3D
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
        current_food = 0
        for bob in self.listebob:
            bob.see(self.grid, show=True)

        # # Affichages des lignes extérieures du haut
        # pygame.draw.line(self.simu_surface, (255, 155, 65),
        #                  (PosX_init + cote_x + self.depx, PosY_init + self.depy), (
        #                      PosX_init + 2 * cote_x + self.depx,
        #                      PosY_init + cote_y + self.depy), 5)
        # pygame.draw.line(self.simu_surface, (255, 155, 65),
        #                  (PosX_init + cote_x + self.depx, PosY_init + self.depy),
        #                  (PosX_init + self.depx, PosY_init + cote_y + self.depy), 5)

        # Affichage des Cases en partant de la case du Haut.
        # Première boucle pour afficher la moitié du terrain
        for step in range(self.config.TAILLE):
            for col in range(step + 1):
                x, y = col, step - col
                case = self.grid[x][y]
                # Affichage de chaques cases
                self.draw_Cases(PosX_init, PosY_init, case, cote_x, xdec, ydec)
                # Affichages de chaques Food.
                current_food = self.draw_Food(PosX_init, PosY_init, case, cote_x, current_food, x, xdec, y, ydec)
                # Affichage des Bobs
                if case.place:
                    self.draw_Bob(PosX_init, PosY_init, case, cote_x, simu_x, xdec, ydec)
        i = 1
        # Seconde boucle pour afficher l'autre moitié du terrain
        for step in range(self.config.TAILLE, 2 * self.config.TAILLE - 1):
            for col in range(i, self.config.TAILLE):
                x, y = col, step - col
                case = self.grid[x][y]
                # Affichage de chaques cases
                self.draw_Cases(PosX_init, PosY_init, case, cote_x, xdec, ydec)
                # Affichages de chaques Food.
                current_food = self.draw_Food(PosX_init, PosY_init, case, cote_x, current_food, x, xdec, y, ydec)
                # Affichage des Bobs
                if case.place:
                    self.draw_Bob(PosX_init, PosY_init, case, cote_x, simu_x, xdec, ydec)
            i += 1

        # # Affichages des lignes extérieures du bas
        # pygame.draw.line(self.simu_surface, (255, 155, 65), (PosX_init + self.depx, PosY_init + cote_y + self.depy),
        #                  (PosX_init + cote_x + self.depx, PosY_init + 2 * cote_y + self.depy), 5)
        # pygame.draw.line(self.simu_surface, (255, 155, 65),
        #                  (PosX_init + 2 * cote_x + self.depx, PosY_init + cote_y + self.depy),
        #                  (PosX_init + cote_x + self.depx, PosY_init + 2 * cote_y + self.depy), 5)

        # Draw_Minimap
        if self.config.show_Minimap:
            self.draw_Minimap(xdec)

        # Draw ProgressBar
        if self.config.show_Food_ProgressBar:
            self.draw_ProgressBar(current_food)

        if(ydec != 0 or xdec != 0 or self.zoom != 0):
            self.gui.draw_reset_button(self.simu_surface)

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

    def init_view(self, tick):
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
        xdec = cote_x / self.config.TAILLE
        ydec = cote_y / self.config.TAILLE
        #Resize food
        size_X = int(0.75 * xdec)
        size_Y = int(1.5 * size_X)
        self.food = pygame.transform.scale(self.foodImage, (size_X, size_Y))
        return PosX_init, PosY_init, cote_x, cote_y, simu_x, xdec, ydec

    def draw_ProgressBar(self, current_food):
        #### PROGRESS BARS ####
        # Progress bar day #
        # Useless since there's Star()
        # pos_bar_day = (0, 20)
        # size_bar_day = (self.simu_surface.get_width() - 10, 5)
        # progress_day = (tick % TICK_DAY) / 100
        # self.gui.progress_bar(pos_bar_day, size_bar_day, progress_day, self.simu_surface, BEER, round=True,
        #                       radius=3)
        # Progress bar food
        progress_beer = pygame.transform.scale(self.beer_image, (150, 150))
        pos_bar_food = (27, 40)
        size_bar_food = (progress_beer.get_width() * 0.55, progress_beer.get_height() * 0.7)
        progress_food = current_food / self.config.NB_FOOD if self.config.NB_FOOD != 0 else 0
        #  Get color palette
        beer_palette = Gradient(BEER_PALETTE, progress_beer.get_width()).gradient(int(progress_food * 100))
        #  Draw the bar
        self.gui.progress_bar(pos_bar_food, size_bar_food, progress_food, progress_beer, beer_palette, vertical=True,
                              reverse=True, round=True, radius=5)
        # Re blit image to get in front of the bar
        progress_beer.blit(pygame.transform.scale(self.beer_image, (150, 150)), (0, 0))

        self.simu_surface.blit(progress_beer, (50, -170 + self.dim_simu[1]))

    def draw_Minimap(self, xdec):
        xdec /= (1 + 0.1 * self.zoom)
        for x in range(self.config.TAILLE):
            for y in range(self.config.TAILLE):
                self.grid[x][y].drawMap(self.simu_surface, xdec, 50)

    def draw_Bob(self, PosX_init, PosY_init, case, cote_x, simu_x, xdec, ydec):
        # Life progress bar
        pos_life_bar = (7, 0)
        # size_life_bar = (25, 5)
        size_life_bar = (1.1 * xdec, 0.3 * ydec)
        # Show velocity through color
        velocity_color = self.gui.color_palette.get_value()

        # Affichage des Bobs
        case.place.sort(key=lambda x: x.masse, reverse=True)
        n = min(5, len(case.place))
        liste = case.place[0:n]
        x, y = liste[0].x, liste[0].y
        Pos = Case(0, 0).bobCase(n, x, y, xdec, ydec)
        for i in range(n):
            bob = liste[i]
            size_X = int(1.5 * xdec - 7.5)
            size_Y = int(size_X*bob.masse**2 + size_X/2 *(1- bob.masse))

            #  Get max velocity for showing it
            if bob.velocity > self.velocity_max:
                self.velocity_max = bob.velocity

            if bob.bobController.select:
                self.draw_Stats(bob, simu_x)
                perso = pygame.transform.scale(bob.redImage, (size_X,size_Y))
            else:
                perso = pygame.transform.scale(bob.image, (size_X,size_Y))
            PosX, PosY = Pos[i]

            velocity_percentage = (bob.velocity / self.velocity_max)
            bob_velocity_color = (velocity_percentage * velocity_color[0],
                                  velocity_percentage * velocity_color[1],
                                  velocity_percentage * velocity_color[2])
            perso.fill(bob_velocity_color, special_flags=BLEND_RGB_ADD)

            self.gui.progress_bar(pos_life_bar, size_life_bar, bob.life, perso, GREEN, True, RED, round=True,
                                  radius=3)
            bob.blit = self.simu_surface.blit(perso, (
                PosX_init + cote_x - 0.5 * size_X + PosX + self.depx, PosY_init + 5 - size_Y + PosY + self.depy))

    def draw_Food(self, PosX_init, PosY_init, case, cote_x, current_food, x, xdec, y, ydec):
        n = min(5, ceil(case.food / self.config.ENERGY_FOOD))
        if n:
            Pos = Case(0, 0).bobCase(n, x, y, xdec, ydec)
            current_food += 1
            for i in range(n):
                PosX, PosY = Pos[i]
                # Affichage de la food
                size_X,size_Y = self.food.get_size()
                self.simu_surface.blit(self.food, (
                    PosX_init + cote_x - 0.5 *size_X + 10 + PosX + self.depx, PosY_init - size_Y + PosY + self.depy))
        return current_food

    def draw_Cases(self, PosX_init, PosY_init, case, cote_x, xdec, ydec):
        if case.floor == "Grass":
            case.draw(self.simu_surface, xdec, ydec, PosX_init, PosY_init, self.depx, self.depy, cote_x,
                      self.tree)
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
            case.draw(self.simu_surface, xdec, ydec, PosX_init, PosY_init, self.depx, self.depy, cote_x, None)
