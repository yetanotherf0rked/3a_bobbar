from ressources.config import *

class Pile():

    def __init__(self):
        self.pile = []
        self.len = 0

    def empile(self,new):
        if self.len == 10*TICK_DAY:
            del self.pile[0]
            self.len-=1
        self.pile.append(new)
        self.len+=1

    def depile(self):
        if self.len == 0:
            return None
        else:
            self.len-=1
            return self.pile.pop(-1)