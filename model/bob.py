from random import uniform, choice
from model.case import *
from ressources.constantes import *


class Bob:

    def __init__(self, pos):
        self.x, self.y = pos      #Case où ce trouve le Bob
        self.energy = ENERGY_SPAWN
        self.velocity = 1.0
        self.masse = 1.0
        self.perception = 0
        self.memory_points = 0
        self.energy_move = self.velocity**2*self.masse + self.perception/5 + self.memory_points/5
        self.speed_buffer = 0.0
        self.memory = ([],[])# memory[0] -> cases deja visités  memory [1]-> food vu mais pas prio.
    
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
            son.perception = max(0,self.perception+ choice([-MUT_PERCEPT,0,MUT_PERCEPT]))
            son.memory_points=max(0,self.memory_points + choice([-MUT_MEMORY,0,MUT_MEMORY]))
            son.energy_move = son.velocity**2*son.masse + son.perception/5 + son.memory_points/5
            #Ajout du fils dans la liste des Bobs et sur la grille
            listebob.insert(0,son)
            grille[self.x][self.y].place.append(son)

    def move_preference(self, grille):
        if self.perception < 1:
            return choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        radius = self.perception # on arrondi la perception à l'entier inférieur
        danger = False  # si il n'y a pas de danger on chasse, sinon on fuit
        max_food = 0
        largest_masse = 0
        target = (0, 0)
        for dx, dy in [(i, j) for i in range(-radius, radius+1) for j in range(abs(i)-radius, radius+1-abs(i))]:  # génère toutes les couples (dx, dy) dans un cercle de norme radius en distance euclidienne et de centre (0, 0)
            if 0 <= self.x + dx < TAILLE and 0 <= self.y+dy < TAILLE:  # si la position qu'on regarde est bien dans la grille
                for other in grille[self.x+dx][self.y+dy].place:  # si il y a des bobs sur cette case
                    if self.masse/other.masse < 2/3:  # si il y a un bob menaçant, on est en danger + update de la valeur de largest_masse
                        danger = True
                        if other.masse > largest_masse:
                            target = (self.x + dx, self.y + dy)
                            largest_masse = other.masse
                    if (not danger) and other.masse/self.masse < 2/3:  # si on est en danger, on ne s'interesse plus à la chasse
                        potential_energy = 0.5*other.energy*(1-(other.masse/self.masse))
                        if potential_energy > max_food:
                            target = (self.x + dx, self.y + dy)
                            max_food = potential_energy
                if not danger and grille[self.x+dx][self.y+dy].food > max_food:  # si on est en danger, on ne s'interesse plus à la food
                    target = (self.x + dx, self.y + dy)
                    max_food = grille[self.x+dx][self.y+dy].food

        if not max_food and not largest_masse:  # si aucune food et aucun bob menaçant n'a été trouvé
            return choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        if danger:
            return max([(-1, 0), (1, 0), (0, -1), (0, 1)], key=lambda x: abs(target[0] - x[0]) + abs(target[1] - x[1]))  # retourne le (dx, dy) pour maximiser la distance avec le danger
        return min([(-1, 0), (1, 0), (0, -1), (0, 1)], key=lambda x: abs(target[0] - x[0]) + abs(target[1] - x[1]))  # retourne le (dx, dy) pour minimiser la distance avec le gain

    def save(self, case, mode=0):
        """ le bob stocke une case dans sa memoire
        mode = 0 pour stocker une case visitée 
        mode = 1 pour stocker une case vue interressante.
        """
        copy = Case(case.x,case.y)
        copy.food = case.food
        copy.place = case.place.copy()
        self.memory[mode].insert(0,copy)
        if len(self.memory[mode]) > 10*self.memory_points : # on vide les vieux souvenirs 
            self.memory[mode].pop(10*self.memory_points)

    def remember(self, mode=0, number=1):
        """ renvoie la ou les number dernieres cases stockés en memoire
        mode = 0 pour les cases déjà visitées 
        mode = 1 pour les case vues interressantes.
        """
        return tuple(self.memory[mode][i] for i in range(number))

    

    

