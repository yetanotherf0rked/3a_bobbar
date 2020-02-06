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

    def __init__(self, simul=0, bar=None, settings = None):
        self.settings = settings
        self.first = True
        # Initialisation de la grille
        self.config = ressources.config.para
        self.world = World()
        self.file = File()
        self.viewSize = None
        self.graph = Graph(animation=False)
        self.simul = simul
        self.simuBar = bar
        self.speed = 0.001
        self.run(self.config.affichage, self.simul)

    def run(self, affichage, simul=0):
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

            #update du graph TODO regroupé dans une seule fonction de Graph 
            self.graph.update_data(self.world.grid,self.world.listebob,tick)
            if self.config.g_animation :
                self.graph.anim()
            if self.config.g_updated :
                self.config.g_updated =False
                self.graph.update_parameter(self.config.g_animation,self.config.g_parameters)
                
            
            
            self.world.listebob.sort(key=lambda x: x.velocity, reverse=True)
            self.world.update_listebob()
            self.simuBar.setValue(tick/((simul-1) * self.config.TICK_DAY) * 100)
            self.file.tick = tick
        
        if affichage:
            if self.config.tick_by_tick:
                self.speed = 1
            else:
                self.speed = 0.001
            self.view = View()
            if self.viewSize:
                self.view.width, self.view.height = self.viewSize
        else:
            self.settings.close()
            continuer = False
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
                                "print(sliders_Config.get_info(s),str(self.config.%s).rjust(40-len(sliders_Config.get_info(s))))" % s)
                        print()

                    # Spawn de la nouvelle food
                    self.world.spawnfood()
                tick += 1
                if self.config.g_updated :
                    self.config.g_updated =False
                    self.graph.update_parameter(self.config.g_animation,self.config.g_parameters)
                if self.config.g_animation and tick%self.config.g_update_rate==0:
                    self.graph.anim()
                if self.config.show_graph :
                    #self.graph.set_animation(False)
                    self.graph.update_parameter(False,self.config.g_parameters)
                    self.graph.plot()

                    self.config.show_graph=False

                self.world.listebob.sort(key=lambda x: x.velocity, reverse=True)
                self.world.update_listebob()
                if affichage:
                    self.file.enfile(self.world)
            sleep(self.speed)
            if affichage:
                # Update de la fenêtre
                if not self.view.run:
                    if not wait:
                        aff_world = self.file.defile()
                        self._thread = Thread(target=self.view.affichage, args=(aff_world, self.file.tick))
                        self.graph.update_data(aff_world.grid,aff_world.listebob,self.file.tick)
                        
                    else:
                        self._thread = Thread(target=self.view.affichage,
                                              args=(self.file.get_Current(), self.file.tick))
                    self._thread.start()
                # Test de fin
                if self.config.restart:
                    continuer = False
                    self.viewSize = self.view.width, self.view.height

                if self.config.settings:
                    self.settings.show()
                    self.config.settings = False
                    if not wait :
                        self.view.gui.pause_button_pressed()
                # Boucle sur les events
                for event in pygame.event.get():  # On parcours la liste de tous les événements reçus

                    # Stop
                    if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT or self.view.gui.gui_quit:  # Si un de ces événements est de type QUIT
                        continuer = False  # On arrête la boucle
                        self.settings.close()
                        self.view.gui.gui_quit=False
                       

                    # Pause
                    if affichage and event.type == KEYDOWN and event.key == K_SPACE:
                        self.view.gui.pause_button_pressed()

                    if event.type == VIDEORESIZE:
                        self.view.width, self.view.height = event.size
                        self.viewSize = event.size

                    # Permet le déplacement dans la fenêtre
                    if event.type == KEYDOWN and (event.key == K_UP or event.key == K_z):
                        self.view.depy += self.config.DEP_STEP * (1 + 0.1 * self.view.zoom)
                    if event.type == KEYDOWN and (event.key == K_DOWN or event.key == K_s):
                        self.view.depy -= self.config.DEP_STEP * (1 + 0.1 * self.view.zoom)
                    if event.type == KEYDOWN and (event.key == K_LEFT or event.key == K_q):
                        self.view.depx += self.config.DEP_STEP * (1 + 0.1 * self.view.zoom)
                    if event.type == KEYDOWN and (event.key == K_RIGHT or event.key == K_d):
                        self.view.depx -= self.config.DEP_STEP * (1 + 0.1 * self.view.zoom)
                    # Permet d'avancer/reculer dans l'historique quand on est en pause
                    if wait and event.type == KEYDOWN and event.key == K_KP4:
                        self.file.precTick()
                    if wait and event.type == KEYDOWN and event.key == K_KP6:
                        self.file.nextTick()
                    #Change speed of the simulation
                    if event.type == KEYDOWN and event.key == K_KP2:
                        self.speed = max(0.001, self.speed-0.005)
                        print(self.speed)
                    if event.type == KEYDOWN and event.key == K_KP8:
                        self.speed += 0.005
                        print(self.speed)

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
                        self.view.zoom = max(0, self.view.zoom - 1)
            #Permet de cacher la fenêtre de settings au départ.
            if self.first:
                self.settings.hide()
                self.settings.setEnabled(True)
                self.first = False

        # After simulation
        #if we want to restart new simulation
        if self.config.restart:
            self._thread.join()
            pygame.display.quit()
            self.settings.hide()
            self.config.restart = False
            self.world = World()
            self.file = File()
            self.run(self.config.affichage, self.simul)
        else:
            # If pygame is close
            if self.config.affichage:
                self._thread.join()
                pygame.display.quit()
            # Show the Graph
            self.graph.hide()
            self.graph.animation = False
            self.graph.set_parameter(x='days', pop=True, age=True, velocity=True, perception=True, memory=True,
                                     mass=True,
                                     rows=2, collumns=3)
            self.graph.plot()