from random import randint
from threading import Thread
from time import sleep

import pygame
from pygame.locals import *

from ressources.sliders import *
import ressources.config
from model import *
from view import View
from view.debug import *
from view.graphs import Graph


class Controller:

    def __init__(self, mode='a', simul=0, bar=None):
        # Initialisation de la grille
        self.config = ressources.config.para
        self.world = World()
        self.file = File()
        if self.config.show_graph:
            self.graph = Graph()
        # #  a : affichage
        # #  d : debug
        # #  s : simulation de n tour passsé à la suite pour stats
        if mode == 'a':
            self.simuBar = bar
            self.run(self.config.affichage, False, simul)
        elif mode == 'd':
            self.run_debug()
        elif mode == 's':
            self.simul(simul)

    def run(self, affichage, stats, simul=0):
        tick = 0
        day = 0
        continuer = True
        if simul == 1:
            self.simuBar.setValue(100)
        for _ in range((simul-1) * self.config.TICK_DAY):
            if tick % self.config.TICK_DAY == 0:
                # Suppression de la nourriture restante
                self.world.removefood()
                day += 1
                # Spawn de la nouvelle food
                self.world.spawnfood()
            tick += 1
            if self.config.show_graph:
                self.graph.update((tick / self.config.TICK_DAY, len(self.world.listebob)))
            # drawStats(self.world.grid, self.world.listebob, tick)
            self.world.listebob.sort(key=lambda x: x.velocity, reverse=True)
            self.world.update_listebob()
            self.simuBar.setValue(tick/((simul-1) * self.config.TICK_DAY) * 100)
            self.file.tick = tick
        if affichage:
            self.view = View()
        while continuer and self.world.listebob:
            wait = self.view.gui.gui_pause if affichage else False
            if not self.file.full():
                # Comptage des ticks/Days
                if tick % self.config.TICK_DAY == 0:
                    # Suppression de la nourriture restante
                    self.world.removefood()
                    day += 1
                    if affichage:
                        for s in self.view.gui.sliders:
                            eval(
                                "print(sliders_Config.get_info(s),str(self.config." + s + ").rjust(40-len(sliders_Config.get_info(s))))")
                        print()

                    # Spawn de la nouvelle food
                    self.world.spawnfood()
                tick += 1
                #drawStats(self.world.grid, self.world.listebob, tick)
                if self.config.show_graph:
                    self.graph.launch_anim((tick/self.config.TICK_DAY,len(self.world.listebob)))
                self.world.listebob.sort(key=lambda x: x.velocity, reverse=True)
                self.world.update_listebob()
                if affichage:
                    self.file.enfile(self.world)

                if stats:
                    drawStats(self.world.grid, self.world.listebob, tick)
            else:
                sleep(0.1)

            if affichage:
                # Update de la fenêtre
                if not self.view.run:
                    if not wait:
                        self._thread = Thread(target=self.view.affichage, args=(self.file.defile(), self.file.tick))
                    else:
                        self._thread = Thread(target=self.view.affichage,
                                              args=(self.file.get_Current(), self.file.tick))
                    self._thread.start()
                # Test de fin

                # Boucle sur les events
                for event in pygame.event.get():  # On parcours la liste de tous les événements reçus

                    # Stop
                    if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT or self.view.gui.gui_quit:  # Si un de ces événements est de type QUIT
                        continuer = False  # On arrête la boucle

                    # Pause
                    if affichage and event.type == KEYDOWN and event.key == K_SPACE:
                        self.view.gui.pause_button_pressed()

                    if event.type == VIDEORESIZE:
                        self.view.width, self.view.height = event.size

                    # Permet le déplacement dans la fenêtre
                    if event.type == KEYDOWN and (event.key == K_UP or event.key == K_z):
                        self.view.depy -= self.config.DEP_STEP * (1 + 0.1 * self.view.zoom)
                    if event.type == KEYDOWN and (event.key == K_DOWN or event.key == K_s):
                        self.view.depy += self.config.DEP_STEP * (1 + 0.1 * self.view.zoom)
                    if event.type == KEYDOWN and (event.key == K_LEFT or event.key == K_q):
                        self.view.depx -= self.config.DEP_STEP * (1 + 0.1 * self.view.zoom)
                    if event.type == KEYDOWN and (event.key == K_RIGHT or event.key == K_d):
                        self.view.depx += self.config.DEP_STEP * (1 + 0.1 * self.view.zoom)
                    # Permet d'avancer/reculer dans l'historique quand on est en pause
                    if wait and event.type == KEYDOWN and event.key == K_KP4:
                        self.file.precTick()
                    if wait and event.type == KEYDOWN and event.key == K_KP6:
                        self.file.nextTick()

                    # Réagit si l'on bouge les sliders
                    self.view.menu_surface.unlock()
                    self.view.gui.menu.react(event)

                    # Permet la sélection d'un bob
                    if event.type == MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        x -= self.view.dim_menu[0]
                        if self.view.soleil.blit.collidepoint((x, y)):
                            self.view.gui.pause_button_pressed()
                        for bob in self.view.listebob:
                            if bob.blit and bob.blit.collidepoint((x, y)):
                                bob.bobController.select = not bob.bobController.select

                    # Permet le zoom
                    if event.type == KEYDOWN and event.key == K_KP_PLUS:
                        self.view.zoom += 1
                    if event.type == KEYDOWN and event.key == K_KP_MINUS:
                        self.view.zoom -= 1

    def run_debug(self):
        tick = 0
        day = 0
        continuer = True
        while continuer and self.world.listebob:

            # Comptage des ticks/Days
            if tick % self.config.TICK_DAY == 0:
                # Suppression de la nourritue restante
                self.world.removefood()
                day += 1
                # Spawn de la nouvelle food
                self.world.spawnfood()
                print(day, len(self.world.listebob))
            tick += 1
            drawStats(self.world.grid, self.world.listebob, tick)
            self.world.listebob.sort(key=lambda x: x.velocity, reverse=True)
            self.update()
            sleep(0.01)
            os.system('cls' if os.name == 'nt' else 'clear')

    def simul(self, ticks):
        """simule un nombre de tick donné et affiche l'etat de la simulation."""
        tick = 0
        day = 0
        for _ in range(ticks):
            if tick % self.config.TICK_DAY == 0:
                self.world.removefood()
                day += 1
                self.world.spawnfood()
            tick += 1
            self.update()
        drawStats(self.world.grid, self.world.listebob, tick)