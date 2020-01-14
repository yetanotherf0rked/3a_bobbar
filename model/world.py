from random import randint

import ressources.config
from model import *


class World:
    def __init__(self):
        self.config = ressources.config.para
        self.grid = [[Case(x, y) for y in range(self.config.TAILLE)] for x in range(self.config.TAILLE)]
        self.foodpos = []
        self.listebob = self.initbob()

    def copie(self):
        newWorld = World()
        newWorld.grid = [[case.copie() for case in liste] for liste in self.grid]
        newWorld.listebob = [bob.copie() for bob in self.listebob]
        newWorld.foodpos = [case.copie() for case in self.foodpos]
        return newWorld

    def spawnfood(self):
        for _ in range(self.config.NB_FOOD):
            x, y = randint(0, self.config.TAILLE - 1), randint(0, self.config.TAILLE - 1)
            self.grid[x][y].food += self.config.ENERGY_FOOD
            self.foodpos.append(self.grid[x][y])

    def removefood(self):
        # Suppression de la food par suppression des cases d'une liste
        for case in self.foodpos:
            case.food = 0
        self.foodpos = []

    # Initialisation des Bobs
    def initbob(self):
        listebob = []
        for bob in range(self.config.NB_POP):
            # Position du Bob
            x, y = randint(0, self.config.TAILLE - 1), randint(0, self.config.TAILLE - 1)
            bob = Bob([x, y])
            self.grid[x][y].place.append(bob)
            listebob.append(bob)
        return listebob
    
    def update_listebob(self):
        new_bobs = []
        for bob in self.listebob:
            # update du bob
            if not bob.is_dead():
                new_bobs += bob.update(self.grid)

            # Si le bob est mort on le retire
            if bob.is_dead():
                self.grid[bob.x][bob.y].place.remove(bob)
                self.listebob.remove(bob)

        # on ajoute les nouveaux nés dans la liste de bobs qui sera actualisé au prochain tick
        self.listebob += new_bobs