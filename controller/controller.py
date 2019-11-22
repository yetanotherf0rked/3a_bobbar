from model import *
from random import randint,choice
from ressources.constantes import *
from view import *
from view.debug import *
import pygame
from pygame.locals import *
from threading import Thread
from time import sleep
import os


AFFICHAGE = False


class Controller:

    def __init__(self):
        # Initialisation de la grille
        self.grille = [[Case(x, y) for y in range(TAILLE)] for x in range(TAILLE)]
        #Initialisation des Bobs
        self.listebob = self.initbob(self.grille)
        if AFFICHAGE:
            self.view = View()
        self.run()
        



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
        for k in range(NB_FOOD):
            x, y = randint(0, TAILLE-1), randint(0, TAILLE-1)
            grille[x][y].food += ENERGY_FOOD

    def removefood(self, grille):
        for x in range(TAILLE):
            for y in range(TAILLE):
                grille[x][y].food = 0

    def update(self, grille, listebob):
        for bob in listebob:
            # Test si le Bob a bougé ou non
            is_moving = False
            # Test si le Bob est mort ou non
            is_dead = False
            # Mange la nourriture restante si possible
            if grille[bob.x][bob.y].food != 0:
                grille[bob.x][bob.y].food = bob.eat(grille[bob.x][bob.y].food)
            if len(grille[bob.x][bob.y].place) > 1:  # Fight
                for other_bob in grille[bob.x][bob.y].place:
                    # if other_bob != bob:  # inutile car bob.masse/bob.masse > 2/3
                    if other_bob.masse/bob.masse < 2/3:
                        bob.energy = min(ENERGY_MAX, bob.energy + 0.5*other_bob.energy*(1-(other_bob.masse/bob.masse)))
                        other_bob.energy = 0
                        other_bob.is_dead(listebob, grille)

            # Déplacement du Bob
            tmp = bob.speed_buffer + bob.velocity
            while tmp >= 1:
                tmp -= 1
                dx, dy = choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
                is_moving = bob.move(grille, dx, dy) or is_moving
                # Bob mange
                if grille[bob.x][bob.y].food != 0:
                    grille[bob.x][bob.y].food = bob.eat(grille[bob.x][bob.y].food)
            bob.speed_buffer = tmp

            # Naissance d'un enfant si possible
            bob.parthenogenesis(listebob, grille)

            # Retire de l'énergie
            bob.energy -= bob.energy_move if is_moving else ENERGY_STAY

            #Si le bob est mort on le retire
            bob.is_dead(listebob, grille)

    def run(self):
        tick = 0
        day = 0
        continuer = True
        while continuer:
            # Comptage des ticks/Days
            if tick % TICK_DAY == 0:
                # Suppression de la nourritue restante
                self.removefood(self.grille)
                day += 1
                # Spawn de la nouvelle food
                self.spawnfood(self.grille)
                #print(day, len(self.listebob))
            tick += 1
            self.listebob.sort(key=lambda x: x.velocity, reverse=True)
            self.update(self.grille, self.listebob)
            drawStats(self.grille, self.listebob, tick)
            sleep(0.01)
            os.system('cls' if os.name == 'nt' else 'clear')
            if AFFICHAGE: 
                # Update de la fenêtre
                while self.view.run:
                    # Limitation de vitesse de la boucle
                    sleep(0.001)
                self._thread = Thread(target=self.view.affichage, args=(self.grille, self.listebob))
                self._thread.start()

                # Update des Bobs
                self.update(self.grille, self.listebob)

                # Test de fin
                for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
                    if event.type == KEYDOWN and event.key == K_ESCAPE:  # Si un de ces événements est de type QUIT
                        continuer = False  # On arrête la boucle
        
        
    def simul(self, ticks): 
        """simule un nombre de tick donné et affiche l'etat de la simulation."""
        tick = 0
        day = 0
        for _ in range(ticks):
            if tick % TICK_DAY == 0:
                self.removefood(self.grille)
                day += 1
                self.spawnfood(self.grille)
            tick += 1
            self.update(self.grille, self.listebob)
        drawStats(self.grille, self.listebob, tick)