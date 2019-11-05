from random import uniform
from model.case import *
from ressources.constantes import *

class Bob:

    def __init__(self, pos):
        self.i,self.j = pos      #Case où ce trouve le Bob
        self.energy = ENERGY_SPAWN
        self.velocity = 1
        self.masse = 1
        self.energy_move = self.velocity**2*self.masse

    def move(self, grille, di, dj):
        ni=self.i+di
        nj=self.j+dj
        if(0<=ni<TAILLE and 0<=nj<TAILLE ) :
            grille[self.i][self.j].place.remove(self)
            self.i=ni
            self.j=nj
            grille[self.i][self.j].place.append(self)
            return True
        return False


        

    def is_dead(self, listebob, grille):
        #Test si le bob est mort et le supprime si c'est le cas
        if self.energy <= 0:
            listebob.remove(self)
            grille[self.i][self.j].place.remove(self)
            return True
        return False

    def eat(self, grille, rate = 1):
        #Test si il y a de la bouffe la ou il est
        if grille[self.i][self.j].food != 0:

            #bouffe disponible
            food = grille[self.i][self.j].food * rate

            if food + self.energy <= ENERGY_MAX :
                self.energy += food
                grille[self.i][self.j].food -= food
            else:
                grille[self.i][self.j].food -= ENERGY_MAX-self.energy
                self.energy = 200

    def parthenogenesis(self, listebob, grille):
        #Naissance d'un nouveau Bob
        if self.energy == ENERGY_MAX:
            self.energy = ENERGY_MOTHER

            #Nouveau bob
            son = Bob([self.i,self.j])
            son.energy=ENERGY_SON
            #Ajout du fils dans la liste des Bobs et sur la grille
            listebob.append(son)
            grille[self.i][self.j].place.append(son)