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

    def move(self,is_moving,grille):
        direction = randint(0,3) #0 Nord 1 Sud 2 Est 3 Ouest
        if direction == 0 and self.i!=TAILLE-1:
            grille[self.i][self.j].place.remove(self)
            self.i+=1
            grille[self.i][self.j].place.append(self)
            is_moving = True
        elif direction == 1 and self.i != 0:
            grille[self.i][self.j].place.remove(self)
            self.i-=1
            grille[self.i][self.j].place.append(self)
            is_moving = True
        elif direction == 2 and self.j != TAILLE-1:
            grille[self.i][self.j].place.remove(self)
            self.j+=1
            grille[self.i][self.j].place.append(self)
            is_moving = True
        elif self.j != 0:
            grille[self.i][self.j].place.remove(self)
            self.j-=1
            grille[self.i][self.j].place.append(self)
            is_moving = True
        return is_moving


    def is_dead(self,listebob,grille):
        #Test si le bob est mort et le supprime si c'est le cas
        if self.energy <= 0:
            listebob.remove(self)
            grille[self.i][self.j].place.remove(self)
            return True
        return False

    def eat(self,grille,rate = 1):
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

    def parthenogenesis(self,listebob,grille):
        #Naissance d'un nouveau Bob
        if self.energy == ENERGY_MAX:
            self.energy = ENERGY_MOTHER

            #Nouveau bob
            son = Bob([self.i,self.j])

            #Ajout du fils dans la liste des Bobs et sur la grille
            listebob.append(son)
            grille[self.i][self.j].place.append(son)