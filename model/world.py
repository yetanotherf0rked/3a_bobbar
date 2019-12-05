from model import *
from ressources.constantes import *
from random import randint


class World:
    def __init__(self):
        self.grid = [[Case(x, y) for y in range(TAILLE)] for x in range(TAILLE)]

    def spawnfood(self):
        for _ in range(NB_FOOD):
            x, y = randint(0, TAILLE - 1), randint(0, TAILLE - 1)
            self.grid[x][y].food += ENERGY_FOOD

    def removefood(self):
        for x in range(TAILLE):
            for y in range(TAILLE):
                self.grid[x][y].food = 0