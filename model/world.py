from model import *
from ressources.config import *
from random import randint


class World:
    def __init__(self):
        self.grid = [[Case(x, y) for y in range(TAILLE)] for x in range(TAILLE)]

    def spawnfood(self):
        print("Food number =",parameters.get("Food Number"))
        for _ in range(parameters.get("Food Number")):
            x, y = randint(0, TAILLE - 1), randint(0, TAILLE - 1)
            self.grid[x][y].food += parameters.get("Food Energy")

    def removefood(self):
        for x in range(TAILLE):
            for y in range(TAILLE):
                self.grid[x][y].food = 0