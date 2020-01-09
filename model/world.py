from random import randint

import ressources.config
from model import *


class World:
    def __init__(self):
        self.config = ressources.config.para
        self.grid = [[Case(x, y) for y in range(self.config.TAILLE)] for x in range(self.config.TAILLE)]
        self.foodpos = []

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
