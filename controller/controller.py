from model import *
from random import randint,choice
from ressources.config import *
from view.debug import *
from view import View
import pygame
from pygame.locals import *
from threading import Thread
import gc


class Controller:

    def __init__(self, mode='a', simul=1000):
        # Initialisation de la grille
        self.world = World()
        self.grille = self.world.grid
        # Initialisation des Bobs
        self.listebob = self.initbob()
        self.file = File()
        if mode == 'a':
            self.view = View()
            self.run(True,False)
        elif mode == 'd':
            self.run_debug()
        elif mode == 's':
            self.simul(simul)

    # Initialisation des Bobs
    def initbob(self):
        listebob = []
        for bob in range(NB_POP):
            # Position du Bob
            x, y = randint(0, TAILLE-1), randint(0, TAILLE-1)
            bob = Bob([x, y])
            self.grille[x][y].place.append(bob)
            listebob.append(bob)
        return listebob

    def update(self):
        new_bobs=[]
        for bob in self.listebob:
            # update du bob
            if not bob.is_dead() :
                new_bobs+=bob.update(self.grille)

            # Si le bob est mort on le retire
            if bob.is_dead() :
                self.grille[bob.x][bob.y].place.remove(bob)
                self.listebob.remove(bob)

        # on ajoute les nouveaux nés dans la liste de bobs qui sera actualisé au prochain tick
        self.listebob += new_bobs

    def run(self,affichage,stats):
        tick = 0
        day = 0
        continuer = True

        while continuer and self.listebob:
            wait = self.view.gui.gui_pause
            if not wait:
                # Comptage des ticks/Days
                if tick % TICK_DAY == 0:
                    # Suppression de la nourriture restante
                    self.world.removefood()
                    day += 1

                    # Spawn de la nouvelle food
                    self.world.spawnfood()
                tick += 1
                #drawStats(self.grille, self.listebob, tick)
                self.listebob.sort(key=lambda x: x.velocity, reverse=True)
                self.update()
                self.file.enfile(self.grille)
                if stats:
                    drawStats(self.grille, self.listebob, tick)

            if affichage:
                # Update de la fenêtre
                if not self.view.run:
                    if not wait:
                        self._thread = Thread(target=self.view.affichage, args=(self.file.defile(),self.file.tick))
                    else :
                        self._thread = Thread(target=self.view.affichage, args=(self.file.get_Current(),self.file.tick))
                    self._thread.start()
                # print(len(self.file.file),len(self.file.historique.pile),TICK_DAY*10)
                # Test de fin
                for event in pygame.event.get():  # On parcours la liste de tous les événements reçus

                    # Stop
                    if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT or self.view.gui.gui_quit:  # Si un de ces événements est de type QUIT
                        continuer = False  # On arrête la boucle

                    # Pause
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        self.view.gui.pause_button_pressed()

                    if event.type == VIDEORESIZE:
                        self.view.width,self.view.height = event.size

                    # Permet le déplacement dans la fenêtre
                    if event.type == KEYDOWN and (event.key == K_UP or event.key == K_z):
                        self.view.depy -= DEP_STEP
                    if event.type == KEYDOWN and (event.key == K_DOWN or event.key == K_s):
                        self.view.depy += DEP_STEP
                    if event.type == KEYDOWN and (event.key == K_LEFT or event.key == K_q):
                        self.view.depx -= DEP_STEP
                    if event.type == KEYDOWN and (event.key == K_RIGHT or event.key == K_d):
                        self.view.depx += DEP_STEP
                    if wait and event.type == KEYDOWN and event.key == K_KP4:
                        self.file.precTick()
                    if wait and event.type == KEYDOWN and event.key == K_KP6:
                        self.file.nextTick()
                    # Réagit si l'on bouge les sliders
                    self.view.menu_surface.unlock()
                    self.view.gui.menu.react(event)

                    if event.type == MOUSEBUTTONDOWN:
                        x,y = pygame.mouse.get_pos()
                        x-= self.view.dim_menu[0]
                        if self.view.soleil.blit.collidepoint((x,y)):
                            self.view.gui.pause_button_pressed()
                        for bob in self.view.bobliste:
                            if bob.blit.collidepoint((x,y)):
                                bob.bobController.select = True
                                bob.select = True

    def run_debug(self):
        tick = 0
        day = 0
        continuer = True
        while continuer and self.listebob:

            # Comptage des ticks/Days
            if tick % TICK_DAY == 0:
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
            if tick % TICK_DAY == 0:
                self.world.removefood()
                day += 1
                self.world.spawnfood()
            tick += 1
            self.update()
        drawStats(self.grille, self.listebob, tick)
