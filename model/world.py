from model import *
from ressources.config import *
from random import randint


class World:
    def __init__(self):
        self.grid = [[Case(x, y) for y in range(TAILLE)] for x in range(TAILLE)]
        self.foodpos = []

    def spawnfood(self):
        for _ in range(parameters.get("Food Number")):
            x, y = randint(0, TAILLE - 1), randint(0, TAILLE - 1)
            self.grid[x][y].food += parameters.get("Food Energy")
            self.foodpos.append(self.grid[x][y])

    def removefood(self):
        #Suppression de la food par suppression des cases d'une liste
        for case in self.foodpos:
            case.food = 0
        self.foodpos = []