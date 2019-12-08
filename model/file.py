from ressources.constantes import *
from model.case import *

class File():

    def __init__(self):
        self.file = []

    def enfile(self,new):
        copie = [[Case(x, y) for y in range(TAILLE)] for x in range(TAILLE)]
        for x in range(TAILLE):
            for y in range(TAILLE):
                copie[x][y].food = new[x][y].food
                copie[x][y].place = [bob for bob in new[x][y].place]
        self.file.append(copie)

    def defile(self):
        self.last = self.file.pop(0)
        return self.last

    def current(self):
        return self.last