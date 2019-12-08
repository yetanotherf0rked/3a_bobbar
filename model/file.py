from ressources.constantes import *
from model.case import *

class File():

    def __init__(self):
        self.file = []

    def enfile(self,new):
        copie = [[case.copie() for case in liste] for liste in new]
        self.file.append(copie)

    def defile(self):
        self.last = self.file.pop(0)
        return self.last

    def current(self):
        return self.last