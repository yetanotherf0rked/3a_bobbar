import ressources.config
from model.case import *
from model.pile import *


class File():

    def __init__(self):
        self.config = ressources.config.para
        self.file = []
        self.len = 0
        self.tick = 0
        self.historique = Pile()
        self.current = None

    def enfile(self, new):
        self.file.append(new.copie())
        self.len += 1

    def defile(self):
        if not self.current == None:
            self.historique.empile(self.current)
        self.current = self.file.pop(0)
        self.len -= 1
        self.tick += 1
        return self.current

    def get_Current(self):
        return self.current

    def precTick(self):
        if self.config.historique:
            self.file = [self.current] + self.file
            self.current = self.historique.depile()
            self.tick -= 1
            self.len += 1

    def nextTick(self):
        if self.config.historique and self.len != 0:
            self.defile()

    def full(self):
        if self.config.historique:
            taille_max = HISTORIQUE_MAX * TICK_DAY
        else:
            taille_max = 1
        return self.len == taille_max
