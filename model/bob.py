from random import uniform, choice
from model.case import *
from ressources.config import *
from model.utils import *
import pygame


class Bob:
    def __init__(self, pos):
        self.x, self.y = pos      #Case où se trouve le Bob
        self.energy = parameters.get("Spawn Energy")
        self.velocity = 1.0
        self.masse = 1.0
        self.perception = 0
        self.memory_points = 0
        self.energy_move = self.velocity**2*self.masse
        self.energy_brain = self.perception/5 + self.memory_points/5
        self.speed_buffer = 0.0
        self.mem_food = Memory(self.memory_points)
        self.place_historic = Memory(2*self.memory_points)
        self.blit = None
        self.select = False
        self.bobController = self
        self.parents = set()
        self.childs = set()
        self.age = 0

        # Life for progress bar
        self.life = (self.energy % ENERGY_MAX)/100

    def copie(self):
        bob = Bob((self.x,self.y))
        bob.energy = self.energy
        bob.velocity = self.velocity
        bob.masse = self.masse
        bob.perception = self.perception
        bob.memory_points = self.memory_points
        bob.energy_move = self.energy_move
        bob.speed_buffer = self.speed_buffer
        bob.mem_food = self.mem_food
        bob.place_historic = self.place_historic
        bob.image = pygame.image.load(image_BOB).convert_alpha()
        bob.redImage = pygame.image.load(image_REDBOB).convert_alpha()
        bob.blit = self.blit
        bob.bobController = self.bobController
        bob.select = self.select
        bob.life = self.life
        return bob

    def update(self, grille):
        """update le bob : combats, manger, déplacement... 
        Si le bob se reproduit update retourne une liste contenant le nouveau fils sinon une liste vide"""

        self.age += 1

        is_moving = False
        current_case = grille[self.x][self.y]

        sons = [] #liste contenant les enventuels enfants du bob à ce tour

        # Fight ?
        self.fight(current_case)

        # Mange la nourriture restante si possible
        if current_case.food != 0:
             current_case.food = self.eat(current_case.food)

        #boucle tant que le bob peut  faire une action (speedbuffer > 1)
        self.speed_buffer += self.velocity
        while self.speed_buffer >= 1:
                self.speed_buffer -= 1

                # Mange la nourriture restante si possible
                if current_case.food != 0:
                    current_case.food = self.eat(current_case.food)

                #choix direction déplacement
                dx, dy = self.move_preference(grille) #choice([(-1, 0), (1, 0), (0, -1), (0, 1)]

                #déplacement
                is_moving = self.move(grille, dx, dy)
                self.place_historic.add(current_case)  # ajoute la case qu'il vient de quitter a son historique des cases visités
                current_case = grille[self.x][self.y]
                self.place_historic.forgot(current_case)  # si on arrive le bob arrive à une case dont il se souvenait il la supprime de sa memoire.

                # perte d'energie due au deplacement
                self.energy -= self.energy_move if is_moving else ENERGY_STAY

                # fight ?
                self.fight(current_case)

                # Bob mange si nouriture sur la  nouvelle case
                if current_case.food != 0:
                    current_case.food = self.eat(current_case.food)
                
                #Reproduction ou parthenogenese si possible
                sons+= self.reproduction(current_case)
                sons+= self.parthenogenesis(current_case)

        self.energy-=self.energy_brain

        # Update life in function of energy
        self.life = self.energy / ENERGY_MAX

        if self.life < 0:
            self.life = 0
        elif self.life > 1:
            self.life = 1

        #reproduction si possible :
        return sons

    def move(self, grille, dx, dy):
        nx=self.x+dx
        ny=self.y+dy
        if(0<=nx<TAILLE and 0<=ny<TAILLE): # test limites du monde
            grille[self.x][self.y].place.remove(self)
            self.x=nx
            self.y=ny
            grille[self.x][self.y].place.append(self)
            return True
        return False

    def is_dead(self):
        # Test si le bob est mort et le supprime si c'est le cas
        return self.energy<=0

    def eat(self, food, rate=1):
        eaten_food = rate*food
        if eaten_food + self.energy <= ENERGY_MAX:
            self.energy += eaten_food
            food-=eaten_food
        else:
            food -= ENERGY_MAX-self.energy
            self.energy = 200
        return food

    def parthenogenesis(self, case):
        """naissance d'un nouveau bob si assez d'energie
        retourne une liste contenant le fils"""
        if self.energy == ENERGY_MAX:
            self.energy = parameters.get("Mother Energy")

            # Nouveau bob
            son = Bob([self.x, self.y])
            son.energy = ENERGY_SON
            # Fonction max pour eviter qu'un bob est une vitesse < 1
            son.velocity = max(0, self.velocity + uniform(-MUT_VELOCITY, MUT_VELOCITY))
            son.masse = max(0, self.masse + uniform(-MUT_MASSE, MUT_MASSE))
            son.perception = max(0, self.perception+ choice([-MUT_PERCEPT, 0, MUT_PERCEPT]))
            son.memory_points=max(0, self.memory_points + choice([-MUT_MEMORY, 0 ,MUT_MEMORY]))
            son.energy_move = son.velocity**2*son.masse
            son.energy_brain = son.perception/5 + son.memory_points/5
            # Ajout du fils dans la case
            case.place.append(son)
            self.childs.add(son)
            son.parents.add(self)
            return [son]
         # si le bob n'enfante pas on retourne une liste vide
        return []


    def fight(self, case):
        """test si un combat est possible sur la case actuelle, dévore l'autre Bob dans ce cas """
        if len(case.place) > 1:  # Fight
            for other_bob in case.place:
                # if other_bob != bob:  # inutile car bob.masse/bob.masse > 2/3
                if other_bob.masse/self.masse < 2/3 and (FAMILY_AGGRESSION or (not FAMILY_AGGRESSION and not self.areInSameFamily(other_bob))):
                    self.energy = min(ENERGY_MAX, self.energy + 0.5*other_bob.energy*(1-(other_bob.masse/self.masse)))
                    other_bob.energy = 0

    # apres ce commentaire : methodes en cours d'implementation :

    def reproduction(self, case):
        """ """
        sons=[]
        if self.energy > ENERGY_MIN_REPRO and len(case.place) > 1:
            for other_bob in case.place :
                if other_bob != self and other_bob.energy>ENERGY_MIN_REPRO and self.energy>ENERGY_MIN_REPRO and abs(self.age-other_bob.age) < DIFF_AGE_FOR_REPRODUCTION and (FAMILY_REPRODUCTION or (not FAMILY_REPRODUCTION and not self.areInSameFamily(other_bob))):
                    other_bob.energy -= ENERGY_REPRO
                    self.energy -= ENERGY_REPRO
                    son = Bob([self.x, self.y])
                    son.energy = ENERGY_SON_REPRO

                    son.velocity = max(0, (self.velocity + other_bob.velocity)/2 + uniform(-MUT_VELOCITY, MUT_VELOCITY))
                    son.masse = max(1.0, (self.masse + other_bob.masse)/2 + uniform(-MUT_MASSE, MUT_MASSE))
                    son.perception = max(0, round((self.perception + other_bob.perception )/2) + choice([-MUT_PERCEPT, 0, MUT_PERCEPT]))
                    son.memory_points=max(0, round((self.memory_points + other_bob.memory_points)/2) + choice([-MUT_MEMORY, 0 ,MUT_MEMORY]))
                    son.energy_move = son.velocity**2*son.masse
                    son.energy_brain = son.perception/5 + son.memory_points/5

                    case.place.append(son)

                    self.childs.add(son)
                    other_bob.childs.add(son)

                    son.parents.add(self)
                    son.parents.add(other_bob)

                    sons.append(son)
        return sons

    def see(self, grille, show = False):
        """parcours les cases que voit le bob et retourne des listes des eventuels cases dangereuses,de nouriture et/ou de proies
        show permet de tester si on est dans la view ou non"""

        radius = self.perception
        danger = False
        dangers = []
        preys = []
        foods = []

        for dx, dy in [(i, j) for i in range(-radius, radius+1) for j in range(abs(i)-radius, radius+1-abs(i))]:  # génère toutes les couples (dx, dy) dans un cercle de norme radius en distance euclidienne et de centre (0, 0)
            if 0 <= self.x + dx < TAILLE and 0 <= self.y+dy < TAILLE:  # si la position qu'on regarde est bien dans la grille
                case = grille[self.x+dx][self.y+dy]
                if show and (self.select or WATCH_PERCEPTION):
                    case.type = "Perception"
                    case.nbPerception += 1
                    continue
                for other in case.place:  # si il y a des bobs sur cette case
                    if self.masse/other.masse < 2/3:  # si il y a un bob menaçant, on est en danger
                        danger = True
                        dangers.append(other)

                    if (not danger) and other.masse/self.masse < 2/3:  # si on est pas en danger, on cherche les proies possibles
                        preys.append(other)

                if case.food > 0:  # si il y a de la nourriture on la voit
                    foods.append(case)

        return dangers, foods, preys



    def move_preference(self, grille):
        """récupere les informations sur les cases vues par le bob et choisit une direction en fonction """

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # voit les cases qu'il perçoit
        dangers, foods, prey = self.see(grille)
        
        for food in foods:
            self.mem_food.add(food)

        # si il y a un danger on fuit
        if dangers:
            for e in directions:  # detection d'obstacle/bords de carte
                if is_obstacle(e[0],e[1]):
                    directions.remove(e)

            dangers.sort(key=lambda b: distance((b.x, b.y), (self.x, self.y)), reverse=True)
            dax = dangers[0].x
            day = dangers[0].y

            for dx, dy in directions:
                dmax = distance((dax, day),(self.x, self.y)) 
                if distance((dax, day),(self.x+dx, self.y+dy)) > dmax:
                    directions.remove((dx, dy))
                    dmax = distance((dax, day),(self.x+dx, self.y+dy))

            if not directions:
                directions.append((0, 0))

            return choice(directions)

        # si il y a de la nourriture en vue on y va
        foods = [case for case in set(foods) if case != grille[self.x][self.y]]
        if foods:
            for food in foods:
                self.mem_food.add(food)

            if len(foods) > 1: foods.sort(key=lambda case: case.food if case != grille[self.x][self.y] else -1, reverse=True)
            target = (foods[0].x, foods[0].y)  # case avec la meilleure food
            current = (self.x, self.y)  # case actuelle
            vector = (target[0] - current[0], target[1] - current[1])  # direction vectorielle vers target
            # choix des deux meilleures directions (si il y en a deux)
            directions = []
            if vector[0] != 0: directions.append((vector[0]//abs(vector[0]), 0))
            if vector[1] != 0: directions.append((0, vector[1]//abs(vector[1])))
            return choice(directions)

        if not self.mem_food.is_empty:
            possibilities = self.mem_food.remember(self.memory_points)
            food_case = possibilities.max(key=lambda x: x.food)
            target = (food_case[0].x, food_case[0].y)  # case avec la meilleure food
            current = (self.x, self.y)  # case actuelle
            vector = (target[0] - current[0], target[1] - current[1])  # direction vectorielle vers target
            # choix des deux meilleures directions (si il y en a deux)
            directions = []
            if vector[0] != 0: directions.append((vector[0] // abs(vector[0]), 0))
            if vector[1] != 0: directions.append((0, vector[1] // abs(vector[1])))
            return choice(directions)

        #print("RANDOM")
        return choice(directions)



    def areInSameFamily(self, other_bob):
        if self == other_bob:
            return True

        # si ils ont le(s) même(s) parent(s) (frère/soeur)
        if self.parents == other_bob.parents:
            return True

        # on regarde les parents
        if other_bob.age > self.age:
            open_list = self.parents.copy()
            while open_list:
                current = open_list.pop()
                if current == other_bob:
                    return True
                if current.age < other_bob.age:  # si on regarde un bob plus vieux, on ne continue pas sur les parents de current
                    open_list.update(current.parents)

        # on regarde les enfants
        if other_bob.age < self.age:
            open_list = self.childs.copy()
            while open_list:
                current = open_list.pop()
                if current == other_bob:
                    return True
                if current.age > other_bob.age:  # si on regarde un bob plus jeune, on ne continue pas sur les enfants de current
                    open_list.update(current.childs)

        return False

