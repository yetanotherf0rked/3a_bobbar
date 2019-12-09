from ressources.constantes import *
from model.case import *

class File():

    def __init__(self):
        self.file = []
        self.len = 0
        self.tick = 0

    def enfile(self,new):
        copie = [[case.copie() for case in liste] for liste in new]
        self.file.append(copie)
        self.len+=1

    def defile(self):
        self.last = self.file.pop(0)
        self.len-=1
        self.tick+=1
        return self.last

    def current(self):
        return self.last