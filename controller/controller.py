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
        self.grille = self.world.grid
        # Initialisation des Bobs
        self.listebob = self.initbob()
        self.file = File()
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

    # Initialisation des Bobs
    def initbob(self):
        listebob = []
        for bob in range(self.config.NB_POP):
            # Position du Bob
            x, y = randint(0, self.config.TAILLE - 1), randint(0, self.config.TAILLE - 1)
            bob = Bob([x, y])
            self.grille[x][y].place.append(bob)
            listebob.append(bob)
        return listebob

    def update(self):
        new_bobs = []
        for bob in self.listebob:
            # update du bob
            if not bob.is_dead():
                new_bobs += bob.update(self.grille)

            # Si le bob est mort on le retire
            if bob.is_dead():
                self.grille[bob.x][bob.y].place.remove(bob)
                self.listebob.remove(bob)

        # on ajoute les nouveaux nés dans la liste de bobs qui sera actualisé au prochain tick
        self.listebob += new_bobs

    def updateBar(self, tick, max):
        self.simuBar.setValue(tick / max * 100)

    def run(self, affichage, stats, simul=0):
        tick = 0
        day = 0
        continuer = True
        for _ in range(simul * self.config.TICK_DAY):
            if tick % self.config.TICK_DAY == 0:
                # Suppression de la nourriture restante
                self.world.removefood()
                day += 1

                # Spawn de la nouvelle food
                self.world.spawnfood()
            tick += 1
            # drawStats(self.grille, self.listebob, tick)
            self.listebob.sort(key=lambda x: x.velocity, reverse=True)
            self.update()
            self.updateBar(tick, simul * self.config.TICK_DAY)
        if affichage:
            self.view = View()
        while continuer and self.listebob:
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
                #drawStats(self.grille, self.listebob, tick)
                self.graph.launch_anim((tick/self.config.TICK_DAY,len(self.listebob)))
                self.listebob.sort(key=lambda x: x.velocity, reverse=True)
                self.update()
                if affichage:
                    self.file.enfile(self.grille)

                if stats:
                    drawStats(self.grille, self.listebob, tick)
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
                # print(len(self.file.file),len(self.file.historique.pile),self.config.TICK_DAY)
                # Test de fin

                # Boucle sur les events
                for event in pygame.event.get():  # On parcours la liste de tous les événements reçus

                    # Stop
                    if (
                            event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT or self.view.gui.gui_quit:  # Si un de ces événements est de type QUIT
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
                        for bob in self.view.bobliste:
                            if bob.blit.collidepoint((x, y)):
                                bob.bobController.select = True
                                bob.select = True

                    # Permet le zoom
                    if event.type == KEYDOWN and event.key == K_KP_PLUS:
                        self.view.zoom += 1
                    if event.type == KEYDOWN and event.key == K_KP_MINUS:
                        self.view.zoom -= 1

    def run_debug(self):
        tick = 0
        day = 0
        continuer = True
        while continuer and self.listebob:

            # Comptage des ticks/Days
            if tick % self.config.TICK_DAY == 0:
                # Suppression de la nourritue restante
                self.world.removefood()
                day += 1
                # Spawn de la nouvelle food
                self.world.spawnfood()
                print(day, len(self.listebob))
            tick += 1
            drawStats(self.grille, self.listebob, tick)
            self.listebob.sort(key=lambda x: x.velocity, reverse=True)
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
        drawStats(self.grille, self.listebob, tick)