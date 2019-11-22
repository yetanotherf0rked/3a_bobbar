from random import uniform
from model.case import *
from ressources.constantes import *

class Bob:

    def __init__(self, pos):
        self.x, self.y = pos      #Case où ce trouve le Bob
        self.energy = ENERGY_SPAWN
        self.velocity = 1.0
        self.masse = 1.0
        self.energy_move = self.velocity**2*self.masse
        self.speed_buffer = 0.0

    def move(self, grille, dx, dy):
        nx=self.x+dx
        ny=self.y+dy
        if(0<=nx<TAILLE and 0<=ny<TAILLE): #test limites du monde
            grille[self.x][self.y].place.remove(self)
            self.x=nx
            self.y=ny
            grille[self.x][self.y].place.append(self)
            return True
        return False

    def is_dead(self, listebob, grille):
        #Test si le bob est mort et le supprime si c'est le cas
        if self.energy <= 0:
            listebob.remove(self)
            grille[self.x][self.y].place.remove(self)
            return True
        return False

    def eat(self, food, rate=1):
        eaten_food = rate*food
        if eaten_food + self.energy <= ENERGY_MAX :
            self.energy += eaten_food
            food-=eaten_food
        else:
            food -= ENERGY_MAX-self.energy
            self.energy = 200
        return food

    def parthenogenesis(self, listebob, grille):
        #Naissance d'un nouveau Bob
        if self.energy == ENERGY_MAX:
            self.energy = ENERGY_MOTHER

            #Nouveau bob
            son = Bob([self.x, self.y])
            son.energy = ENERGY_SON
            # Fonction max pour eviter qu'un bob est une vitesse < 1
            son.velocity = max(1.0, self.velocity + uniform(-MUT_VELOCITY, MUT_VELOCITY))
            son.masse = max(1.0, self.masse + uniform(-MUT_MASSE, MUT_MASSE))
            son.energy_move = son.velocity**2*son.masse
            #Ajout du fils dans la liste des Bobs et sur la grille
            listebob.insert(0,son)
            grille[self.x][self.y].place.append(son)