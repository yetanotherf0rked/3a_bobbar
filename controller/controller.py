from random import randint
from threading import Thread
from time import sleep

import pygame
from pygame.locals import *

from ressources.sliders import *
import ressources.config
from model import *
from view import View
from view.statutils import *
from view.graphs import Graph


class Controller:
    """
    Class of the controller.
    Intermediary between the model and the view
    """

    def __init__(self, simul=0, bar=None, settings = None):
        """
        Constructor of the controller

        :param simul: number of days to be simulated before launching the view
        :param bar: progress bar of the simulation
        :param settings: settings windows
        """

        self.settings = settings
        self.first = True

        # Initializes the grid
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
        """
        The main loop

        :param affichage: if equal to True, then display the simulation
        :param simul: number of days to be simulated
        """

        tick = 0
        day = 0
        continuer = True
        if simul == 1:
            self.simuBar.setValue(100)
        for _ in range((simul-1) * self.config.TICK_DAY):
            if tick % self.config.TICK_DAY == 0:
                # Suppressing the remain food
                self.world.removefood()
                day += 1
                # Spawn of the new food
                self.world.spawnfood()
            tick += 1

            # Graph update TODO regrouper dans une seule fonction de Graph
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

        if self.config.show_graph_simul :
            self.graph.animation=False
            self.graph.set_parameter(x='days',pop=True,age=True,velocity=True,perception=True,memory=True,mass=True)
            self.graph.plot()
        
        if affichage:
            if self.config.tick_by_tick:
                self.speed = 0.1
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
                # At each new day
                if tick % self.config.TICK_DAY == 0:
                    # Deletes the remaining food
                    self.world.removefood()
                    day += 1
                    # if affichage:
                        # for s in self.view.gui.sliders:
                        #     eval(
                        #         "print(sliders_Config.get_info(s),str(self.config.%s).rjust(40-len(sliders_Config.get_info(s))))" % s)
                        # print()

                    # Spawn of the new food
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
            if self.config.show_graph :
                    #self.graph.set_animation(False)
                    self.graph.update_parameter(False,self.config.g_parameters)
                    self.graph.plot()

                    self.config.show_graph=False
            if affichage:
                # Update of the windows
                if not self.view.run:
                    if not wait:
                        aff_world = self.file.defile()
                        self._thread = Thread(target=self.view.affichage, args=(aff_world, self.file.tick))
                        self.graph.update_data(aff_world.grid,aff_world.listebob,self.file.tick)
                        
                    else:
                        self._thread = Thread(target=self.view.affichage,
                                              args=(self.file.get_Current(), self.file.tick))
                    self._thread.start()
                # Ending test
                if self.config.restart:
                    continuer = False
                    self.viewSize = self.view.width, self.view.height

                #Test si on a changé la formule de consommation
                if self.config.change_consommation:
                    self.config.change_consommation = False
                    self.world.update_consommation()

                if self.config.settings:
                    self.settings.show()
                    self.config.settings = False
                    if not wait :
                        self.view.gui.pause_button_pressed()

                # Event loop
                for event in pygame.event.get():

                    # Stop
                    if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT or self.view.gui.gui_quit:
                        continuer = False
                        self.settings.close()
                        self.view.gui.gui_quit=False
                       

                    # Pause
                    if affichage and event.type == KEYDOWN and event.key == K_SPACE:
                        self.view.gui.pause_button_pressed()

                    # Resize
                    if event.type == VIDEORESIZE:
                        self.view.width, self.view.height = event.size
                        self.viewSize = event.size

                    # Window movement
                    if event.type == KEYDOWN and (event.key == K_UP or event.key == K_z):
                        self.view.depy += self.config.DEP_STEP * (1 + 0.1 * self.view.zoom)
                    if event.type == KEYDOWN and (event.key == K_DOWN or event.key == K_s):
                        self.view.depy -= self.config.DEP_STEP * (1 + 0.1 * self.view.zoom)
                    if event.type == KEYDOWN and (event.key == K_LEFT or event.key == K_q):
                        self.view.depx += self.config.DEP_STEP * (1 + 0.1 * self.view.zoom)
                    if event.type == KEYDOWN and (event.key == K_RIGHT or event.key == K_d):
                        self.view.depx -= self.config.DEP_STEP * (1 + 0.1 * self.view.zoom)

                    # Previous Tick/Next Tick
                    if wait and event.type == KEYDOWN and event.key == K_KP4:
                        self.file.precTick()
                    if wait and event.type == KEYDOWN and event.key == K_KP6:
                        self.file.nextTick()

                    # Changes the speed of the simulation
                    if event.type == KEYDOWN and event.key == K_KP8:
                        self.speed = max(0.001, self.speed-0.005)
                    if event.type == KEYDOWN and event.key == K_KP2:
                        self.speed += 0.005

                    # Reacts if we move a slider
                    self.view.menu_surface.unlock()
                    self.view.gui.menu.react(event)

                    # To select a bob
                    if event.type == MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        x -= self.view.dim_menu[0]
                        if self.view.soleil.blit.collidepoint((x, y)):
                            self.view.gui.pause_button_pressed()
                        for bob in self.view.listebob:
                            if bob.blit and bob.blit.collidepoint((x, y)):
                                bob.bobController.select = not bob.bobController.select

                        if(self.view.depx or self.view.depy or self.view.zoom):
                            #  Cannot make an if c1 and c2 because zoom_position does not exist
                            #  unless user moves or zoom the map
                            if self.view.gui.zoom_position.blit.collidepoint((x, y)):
                                self.view.gui.zoom_position.mouse_click()
                                self.view.depx = self.view.depy = self.view.zoom = 0

                    # Zoom
                    if event.type == KEYDOWN and event.key == K_KP_PLUS:
                        self.view.zoom += 1
                    if event.type == KEYDOWN and event.key == K_KP_MINUS:
                        self.view.zoom = max(0, self.view.zoom - 1)

            # Hide the settings window
            if self.first:
                self.settings.hide()
                self.settings.setEnabled(True)
                self.first = False

        # After simulation
        # if we want to restart new simulation
        if self.config.restart:
            self._thread.join()
            pygame.display.quit()
            self.settings.hide()
            self.config.restart = False
            self.world = World()
            self.file = File()
            self.run(self.config.affichage, self.simul)
        else:
            # If pygame is closed
            if self.config.affichage:
                self._thread.join()
                pygame.display.quit()

            # Displays the Graph
            self.graph.hide()
            self.graph.animation = False
            self.graph.set_parameter(x='days', pop=True, age=True, velocity=True, perception=True, memory=True,
                                     mass=True,
                                     rows=2, collumns=3)
            self.graph.plot()