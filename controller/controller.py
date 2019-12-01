from model import *
from random import randint
from ressources.constantes import *
from view import *
import pygame
from pygame.locals import *
from threading import Thread
from time import sleep

class Controller:

    def __init__(self):
        #Initialisaion de la grille et des bobs
        self.initgame()
        self.view = View()
        self.run(0,0)


    def initgame(self):
        # Initialisation de la grille
        self.grille = [[Case(i, j) for j in range(TAILLE)] for i in range(TAILLE)]
        self.listebob = self.initbob(self.grille)

    #Initialisation des Bobs
    def initbob(self,grille):
        listebob = []
        for bob in range(NB_POP):
            #Position du Bob
            i,j = randint(0, TAILLE-1), randint(0, TAILLE-1)
            bob = Bob([i,j])
            grille[i][j].place.append(bob)
            listebob.append(bob)
        return listebob

    #Spawn de food
    def spawnfood(self,grille):
        for k in range(NB_FOOD):
            i,j = randint(0,TAILLE-1),randint(0,TAILLE-1)
            grille[i][j].food += ENERGY_FOOD

    def removefood(self,grille):
        for i in range(TAILLE):
            for j in range(TAILLE):
                grille[i][j].food = 0

    def update(self,grille,listebob):
        for bob in listebob:
            # Test si le Bob à bouger ou non
            is_moving = False

            # Mange la nourriture restante si possible
            bob.eat(grille)

            # Déplacement du Bob
            is_moving = bob.move(is_moving,grille)

            # Bob mange
            bob.eat(grille)

            # Naissance d'un enfant si possible
            bob.parthenogenesis(listebob,grille)

            # Retire de l'énergie
            bob.energy -= bob.energy_move if is_moving else ENERGY_STAY

            #Si le bob est mort on le retire
            bob.is_dead(listebob,grille)

    def run(self,tick,day):
        continuer = True
        wait = False
        while continuer:
            # Comptage des ticks/Days
            if tick % TICK_DAY == 0:
                # Suppression de la nourritue restante
                self.removefood(self.grille)
                day += 1
                # Spawn de la nouvelle food
                self.spawnfood(self.grille)
                print(day, len(self.listebob))
            tick += 1

            # Update de la fenêtre
            while self.view.run:
                # Limitation de vitesse de la boucle
                sleep(0.5)
            self._thread = Thread(target=self.view.affichage, args=(self.grille, self.listebob))
            self._thread.start()

            # Update des Bobs
            if not wait:
                self.update(self.grille, self.listebob)

            # Test de fin
            for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
                if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:  # Si un de ces événements est de type QUIT
                    continuer = False  # On arrête la boucle
                if event.type == KEYDOWN and event.key == K_SPACE:
                    wait = not wait
                if event.type == VIDEORESIZE:
                    self.view.width,self.view.height = event.size