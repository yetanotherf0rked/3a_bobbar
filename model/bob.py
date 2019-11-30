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

    def update(self,grille) :
        """update le bob : combats, manger, déplacement... 
        Si le bob se reproduit update retourne une liste contenant le nouveau fils sinon une liste vide"""
        is_moving = False
        current_case = grille[self.x][self.y]

        # Fight ?
        self.fight(current_case)

        # Mange la nourriture restante si possible
        if current_case.food != 0:
             current_case.food = self.eat(current_case.food)
        
        
        
        #boucle tant que le bob peut  faire une action (speedbuffer > 1)
        self.speed_buffer += self.velocity
        while self.speed_buffer >= 1:
                self.speed_buffer -= 1
                #choix direction déplacement
                dx, dy = choice([(-1, 0), (1, 0), (0, -1), (0, 1)])  #self.move_preference(grille)  # 
                #déplacement
                is_moving = self.move(grille, dx, dy) 
                current_case = grille[self.x][self.y]
                #perte d'energie due au deplacement
                self.energy -= self.energy_move if is_moving else ENERGY_STAY

                #fight ?
                self.fight(current_case)

                # Bob mange si nouriture sur la  nouvelle case
                if current_case.food != 0:
                    current_case.food = self.eat(current_case.food)
                
        #reproduction si possible : 
        return self.parthenogenesis(current_case)
                   

    
    
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

    def parthenogenesis(self,case):
        """naissance d'un nouveau bob si assez d'energie 
        retourne une liste contenant le fils"""
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
            #Ajout du fils dans la case
            case.place.append(son)
            return [son]
         #si le bob n'enfante pas on retourne une liste vide
        return []
            

    def fight(self,case):
        """test si un combat est possible sur la case actuelle, dévore l'autre Bob dans ce cas """
        if len(case.place) > 1:  # Fight
            for other_bob in case.place:
                # if other_bob != bob:  # inutile car bob.masse/bob.masse > 2/3
                if other_bob.masse/self.masse < 2/3:
                    self.energy = min(ENERGY_MAX, self.energy + 0.5*other_bob.energy*(1-(other_bob.masse/self.masse)))
                    other_bob.energy = 0
                    other_bob.is_dead(listebob, grille)



    # apres ce commentaire : methode en cours d'implementation :

    def see(self,grille):
        """parcours les cases que voit le bob et retourne les eventuels dangers et eventuels cases de nouriture interresante"""
        radius = self.perception 
        danger = False
        danger_target = ()
        max_food = 0
        largest_masse = 0
        food_seen = []
        for dx, dy in [(i, j) for i in range(-radius, radius+1) for j in range(abs(i)-radius, radius+1-abs(i))]:  # génère toutes les couples (dx, dy) dans un cercle de norme radius en distance euclidienne et de centre (0, 0)
            if 0 <= self.x + dx < TAILLE and 0 <= self.y+dy < TAILLE:  # si la position qu'on regarde est bien dans la grille
                for other in grille[self.x+dx][self.y+dy].place:  # si il y a des bobs sur cette case
                    if self.masse/other.masse < 2/3:  # si il y a un bob menaçant, on est en danger + update de la valeur de largest_masse
                        danger = True
                        if other.masse > largest_masse:
                            danger_target = (self.x + dx, self.y + dy)
                            largest_masse = other.masse
                    if (not danger) and other.masse/self.masse < 2/3:  # si on est en danger, on ne s'interesse plus à la chasse
                        potential_energy = 0.5*other.energy*(1-(other.masse/self.masse))
                        if potential_energy > max_food:
                            food_seen.append((self.x + dx, self.y + dy),False)
                            max_food = potential_energy
                if not danger and grille[self.x+dx][self.y+dy].food > max_food:  # si on est en danger, on ne s'interesse plus à la food
                    food_seen.append((self.x + dx, self.y + dy),True)
                    max_food = grille[self.x+dx][self.y+dy].food
        return danger, danger_target , food_seen

       


    def move_preference(self, grille):
        mem = self.memory_points
        pref = choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        if self.perception < 1 :
            
                
            return pref
        danger_target, food_seen =self.see(grille)


    def save(self, case, mode=0):
        """ le bob stocke une case dans sa memoire
        mode = 0 pour stocker une case visitée 
        mode = 1 pour stocker une case vue interressante (food).
        """
        copy = Case(case.x,case.y)
        copy.food = case.food
        copy.place = case.place.copy()
        self.memory[mode].insert(0,copy)
        if len(self.memory[mode]) > 2*self.memory_points : # on vide les vieux souvenirs 
            self.memory[mode].pop(2*self.memory_points-1)



                    

        

    

    

