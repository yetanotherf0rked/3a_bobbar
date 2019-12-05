from model import *
from random import randint,choice
from ressources.config import *
from view.debug import *
from view import View
import pygame
from pygame.locals import *
from threading import Thread
from time import sleep
import os

class Controller:

    def __init__(self, affichage=True, stats=False):
        # Initialisation de la grille
        self.grille = [[Case(x, y) for y in range(TAILLE)] for x in range(TAILLE)]
        #Initialisation des Bobs
        self.listebob = self.initbob(self.grille)
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

    def update(self, grille, listebob):
        new_bobs=[]
        for bob in listebob:
            #update du bob
            new_bobs+=bob.update(grille,listebob)

            #Si le bob est mort on le retire
            bob.is_dead(listebob,grille[bob.x][bob.y])

        #on ajoute les nouveaux nés dans la liste de bobs qui sera actualisé au prochain tick
        listebob += new_bobs

    def run(self,affichage,stats):
        tick = 0
        day = 0
        continuer = True
        # wait = False

        while continuer:
            if not self.view.gui.gui_pause:

                # Comptage des ticks/Days
                if tick % TICK_DAY == 0:

                    # Suppression de la nourriture restante
                    self.removefood(self.grille)
                    day += 1

                    # Spawn de la nouvelle food
                    self.spawnfood(self.grille)

                tick += 1

                # Update
                self.listebob.sort(key=lambda x: x.velocity, reverse=True)
                self.update(self.grille, self.listebob)

                # Gestion des stats
                if stats:
                    drawStats(self.grille, self.listebob, tick)

            if affichage:
                # Update de la fenêtre
                while self.view.run:
                    # Limitation de vitesse de la boucle
                    sleep(0.001)
                self._thread = Thread(target=self.view.affichage, args=(self.grille, self.listebob, tick))
                self._thread.start()

                # Test de fin
                for event in pygame.event.get():  # On parcours la liste de tous les événements reçus

                    # Stop
                    if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT or self.view.gui.gui_quit:  # Si un de ces événements est de type QUIT
                        continuer = False  # On arrête la boucle

                    # Pause (solution temporaire)
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

                    # Réagit si l'on bouge les sliders ou si l'on appuie sur les boutons
                    self.view.gui.menu.react(event)


    # Fonction de débug des Sliders
    # def paramDebug(self):
    #     for name, value in parameters.actual.items():
    #         print(value,"\t", end='')
    #     print('')