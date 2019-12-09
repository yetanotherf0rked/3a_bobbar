from model import *
from random import randint,choice
from ressources.constantes import *
from view.debug import *
from view import View
import pygame
from pygame.locals import *
from threading import Thread
from time import sleep


class Controller:

    def __init__(self, affichage=True, stats=False):
        # Initialisation de la grille
        self.grille = [[Case(x, y) for y in range(TAILLE)] for x in range(TAILLE)]
        #Initialisation des Bobs
        self.listebob = self.initbob(self.grille)
        self.file = File()
        if affichage:
            self.view = View()
        self.run(affichage,stats)

    #Initialisation des Bobs
    def initbob(self, grille):
        listebob = []
        for bob in range(NB_POP):
            #Position du Bob
            x, y = randint(0, TAILLE-1), randint(0, TAILLE-1)
            bob = Bob([x, y])
            grille[x][y].place.append(bob)
            listebob.append(bob)
        return listebob

    #Spawn de food
    def spawnfood(self, grille):
        for k in range(parameters.get("Food Number")):
            x, y = randint(0, TAILLE-1), randint(0, TAILLE-1)
            grille[x][y].food += parameters.get("Food Energy")

    def removefood(self, grille):
        for x in range(TAILLE):
            for y in range(TAILLE):
                grille[x][y].food = 0

    def update(self):
        new_bobs=[]
        for bob in self.listebob:
            #update du bob
            if not bob.is_dead() :
                new_bobs+=bob.update(self.grille)

            #Si le bob est mort on le retire
            if bob.is_dead() :
                self.listebob.remove(bob)
                self.grille[bob.x][bob.y].place.remove(bob)

        #on ajoute les nouveaux nés dans la liste de bobs qui sera actualisé au prochain tick
        self.listebob += new_bobs

    def run(self,affichage,stats):
        tick = 0
        day = 0
        continuer = True
        wait = False
        while continuer and self.listebob:
            if not wait:
                # Comptage des ticks/Days
                if tick % TICK_DAY == 0:
                    # Suppression de la nourritue restante
                    self.removefood(self.grille)
                    day += 1
                    # Spawn de la nouvelle food
                    self.spawnfood(self.grille)
                tick += 1
                # Affichage du tick, du day et de la population
                self.view.gui.update_state_box(day, tick, len(self.listebob))


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

                # Test de fin
                for event in pygame.event.get():  # On parcours la liste de tous les événements reçus

                    # Stop
                    if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT or self.view.gui.gui_quit:  # Si un de ces événements est de type QUIT
                        continuer = False  # On arrête la boucle

                    # Pause
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        wait = not wait

                    # Test si on a resize la fenêtre
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
                        print("Bonjour")
                    # Réagit si l'on bouge les sliders
                    self.view.gui.menu.react(event)

                    if event.type == MOUSEBUTTONDOWN:
                        x,y = pygame.mouse.get_pos()
                        x-= self.view.dim_menu[0]
                        if self.view.soleil.blit.collidepoint((x,y)):
                            wait = not wait
                        for bob in self.view.bobliste:
                            if bob.blit.collidepoint((x,y)):
                                bob.bobController.select = True