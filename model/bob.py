from random import uniform, random

import ressources.config
from model.case import *
from model.utils import *


class Bob:
    """
    Class Bob.
    Contains the attributes and the methods of a bob
    """
    def __init__(self, pos):
        """
        Constructor of a bob
        :param pos: (x,y) tuple of the position of a bob
        """

        self.config = ressources.config.para
        self.x, self.y = pos  # Cell position of a bob
        self.energy = self.config.ENERGY_SPAWN
        self.velocity = 1.0
        self.masse = 1.0
        self.perception = 0
        self.perception_pos = [(0,0)]
        self.memory_points = 0
        self.energy_move = self.velocity ** 2 * self.masse
        self.energy_brain = self.perception / 5 + self.memory_points / 5
        self.speed_buffer = 0.0
        self.mem_food = Memory(self.memory_points)
        self.place_historic = Memory(2 * self.memory_points)
        self.blit = None
        self.select = False
        self.bobController = self
        self.parents = set()
        self.childs = set()
        self.age = 0
        # Life for progress bar
        self.life = (self.energy % self.config.ENERGY_MAX) / 100
        self.meteoeffect = 1

    def update_meteoeffect(self):
        """
        Updates a bob energy in case of harsh weather
        """
        if self.meteoeffect == 1:
            self.energy=self.energy-200*(1/(16*self.config.TICK_DAY))


    def copie(self):
        """
        Makes a copy of a bob
        :return: the copy of a bob
        """
        bob = Bob((self.x, self.y))
        bob.energy = self.energy
        bob.velocity = self.velocity
        bob.masse = self.masse
        bob.perception = self.perception
        bob.perception_pos = self.perception_pos
        bob.memory_points = self.memory_points
        bob.energy_move = self.energy_move
        bob.energy_brain = self.energy_brain
        bob.speed_buffer = self.speed_buffer
        bob.mem_food = self.mem_food
        bob.place_historic = self.place_historic
        bob.blit = self.blit
        bob.select = self.select
        bob.bobController = self.bobController
        bob.parents = self.parents
        bob.childs = self.childs
        bob.age = self.age
        bob.life = self.life
        bob.meteoeffect = self.meteoeffect
        return bob

    def stats(self):
        """
        For debuging purposes
        :return: list of strings with the statistics
        """

        text=[]
        text.append("Energy : %s" % round(self.energy,2))
        text.append("Velocity : %s" % round(self.velocity,2))
        text.append("Mass : %s" % round(self.masse, 2))
        text.append("Perception : %s" % round(self.perception, 2))
        text.append("Memory : %s" % round(self.memory_points,2))
        text.append("Age : %s" % round(self.age//self.config.TICK_DAY, 2))
        return text

    def update(self, grille):
        """
        :param grille: a grid of bobs
        :return: If the bob reproduces itself then returns a list with the new son, else returns an empty list
        """

        self.age += 1

        is_moving = False
        current_case = grille[self.x][self.y]

        sons = []  # list of the prospective sons of the bob

        # Fights
        self.fight(current_case)

        # Eats
        if current_case.food != 0:
            current_case.food = self.eat(current_case.food)

        # If the bob can still do another action
        self.speed_buffer += self.velocity
        while self.speed_buffer >= 1:
            self.speed_buffer -= 1

            # Eats the remaining food
            if current_case.food != 0:
                current_case.food = self.eat(current_case.food)

            # Chooses the direction
            dx, dy = self.move_preference(grille)  # choice([(-1, 0), (1, 0), (0, -1), (0, 1)]

            # Moves
            is_moving = self.move(grille, dx, dy)
            self.place_historic.add(
                current_case)  # ajoute la case qu'il vient de quitter a son historique des cases visités
            current_case = grille[self.x][self.y]
            self.place_historic.forgot(
                current_case)  # si on arrive le bob arrive à une case dont il se souvenait il la supprime de sa memoire.

            # Loses energy as he's moving
            self.energy -= self.energy_move if is_moving else self.config.ENERGY_STAY

            # fight ?
            self.fight(current_case)

            # Eats if there is food in the Cell he moved in
            if current_case.food != 0:
                current_case.food = self.eat(current_case.food)

            # Reproduction or parthenogenesis
            if self.config.REPRO : sons += self.reproduction(current_case)
            if self.config.PARTH : sons += self.parthenogenesis(current_case)

        self.energy -= self.energy_brain

        # Update life in function of energy
        self.life = self.energy / self.config.ENERGY_MAX

        if self.life < 0:
            self.life = 0
        elif self.life > 1:
            self.life = 1

        # reproduction if possible :
        return sons

    def move(self, grille, dx, dy):
        """
        Movement of a bob on the grid

        :param grille: (world.grid) 2-dimension list containing Case objects
        :param dx: x movement
        :param dy: y movement
        :return: a boolean that says if the bob has moved or not (so we remove energy)
        """

        nx = self.x+dx
        ny = self.y+dy
        if(0<=nx<self.config.TAILLE and 0<=ny<self.config.TAILLE):  # test limites du monde
            grille[self.x][self.y].place.remove(self)
            self.x = nx
            self.y = ny
            grille[self.x][self.y].place.append(self)
            return True
        return False

    def is_dead(self):
        """
        Tests if a bob is dead in a grid
        :return: a boolean that says if a bob is dead or not
        """
        return self.energy <= 0

    def eat(self, food):
        """
        Action of eating

        :param food: the quantity of food in the Cell
        :return: the new quantity of food in a Cell
        """
        eaten_food = food
        if eaten_food + self.energy <= self.config.ENERGY_MAX:
            self.energy += eaten_food
            food -= eaten_food
        else:
            food -= self.config.ENERGY_MAX - self.energy
            self.energy = self.config.ENERGY_MAX
        return food

    def parthenogenesis(self, case):
        """
        Birth of a new bob by parthenogenesis if the mother reaches ENERGY_MAX

        :param case: the Cell where the new bob will eventually spawn
        :return: a list with the new bob if he's born, else an empty list
        """
        if self.energy == self.config.ENERGY_MAX:
            self.energy = self.config.ENERGY_MOTHER

            # New bob
            son = Bob([self.x, self.y])
            son.energy = self.config.ENERGY_SON

            # Max function to avoid that a bob gets a velocity < 1
            son.velocity = max(0, self.velocity + uniform(-self.config.MUT_VELOCITY, self.config.MUT_VELOCITY))
            son.masse = max(1, self.masse + uniform(-self.config.MUT_MASSE, self.config.MUT_MASSE))
            son.perception = max(0, self.perception + choice([-self.config.MUT_PERCEPT, 0, self.config.MUT_PERCEPT]))
            son.perception_pos = [(i, j) for i in range(-son.perception, son.perception + 1) for j in range(abs(i) - son.perception, son.perception + 1 - abs(i))]
            son.memory_points = max(0,
                                    self.memory_points + choice([-self.config.MUT_MEMORY, 0, self.config.MUT_MEMORY]))
            son.energy_move = self.config.move_consommation(son.velocity, son.masse)
            son.energy_brain = self.config.brain_consommation(son.perception, son.memory_points)

            # Appends the son in the Cell
            case.place.append(son)
            self.childs.add(son)
            son.parents.add(self)
            return [son]

        # If no parthenogenesis, returns an empty list
        return []

    def fight(self, case):
        """
        Test if fights are available in the current Cell, eats the other bobs if a fight is available
        :param case: Cell where the fight will eventually happen
        """
        if len(case.place) > 1:  # Fight
            for other_bob in case.place:
                # if other_bob != bob:  # useless because bob.masse/bob.masse > 2/3
                if other_bob.masse / self.masse < 2 / 3 and (self.config.family_Agression or (
                        not self.config.family_Agression and not self.areInSameFamily(other_bob))):
                    self.energy = min(self.config.ENERGY_MAX,
                                      self.energy + 0.5 * other_bob.energy * (1 - (other_bob.masse / self.masse)))
                    other_bob.energy = 0

    def reproduction(self, case):
        """
        Sexual reproduction between one bob and another in a cell
        :param case: the concerned cell
        :return: list of born bobs
        """

        sons = []
        if self.energy > self.config.ENERGY_MIN_REPRO and len(case.place) > 1:
            for other_bob in case.place:
                if other_bob != self and other_bob.energy > self.config.ENERGY_MIN_REPRO and self.energy > self.config.ENERGY_MIN_REPRO and abs(
                        self.age - other_bob.age) < self.config.DIFF_AGE_FOR_REPRODUCTION and (
                        self.config.family_Reproduction or (
                        not self.config.family_Reproduction and not self.areInSameFamily(other_bob))):
                    other_bob.energy -= self.config.ENERGY_REPRO
                    self.energy -= self.config.ENERGY_REPRO
                    son = Bob([self.x, self.y])
                    son.energy = self.config.ENERGY_SON_REPRO

                    son.velocity = max(0, (self.velocity + other_bob.velocity) / 2 + uniform(-self.config.MUT_VELOCITY,
                                                                                             self.config.MUT_VELOCITY))
                    son.masse = max(1.0, (self.masse + other_bob.masse) / 2 + uniform(-self.config.MUT_MASSE,
                                                                                      self.config.MUT_MASSE))
                    son.perception = max(0, round((self.perception + other_bob.perception) / 2) + choice(
                        [-self.config.MUT_PERCEPT, 0, self.config.MUT_PERCEPT]))
                    son.perception_pos = [(i, j) for i in range(-son.perception, son.perception + 1) for j in range(abs(i) - son.perception, son.perception + 1 - abs(i))]
                    son.memory_points = max(0, round((self.memory_points + other_bob.memory_points) / 2) + choice(
                        [-self.config.MUT_MEMORY, 0, self.config.MUT_MEMORY]))
                    son.energy_move = self.config.move_consommation(son.velocity, son.masse)
                    son.energy_brain = self.config.brain_consommation(son.perception, son.memory_points)

                    case.place.append(son)

                    self.childs.add(son)
                    other_bob.childs.add(son)

                    son.parents.add(self)
                    son.parents.add(other_bob)

                    sons.append(son)
        return sons

    def see(self, grille,show=False):
        """
        Iterates on the cells that a bob can see and returns lists of eventual dangerous cell, cells with food or
         cells with preys

        Parametres:
            grille (world.grid): une liste bidimensionnelle contenant des objets Case

        Returns:
            dangers [Bob]: Une liste de Bob plus gros de 2/3 selon la masse par rapport à self.masse
            foods [Case]: Une liste de Case avec de la nourriture
            preys [Bob]: Une liste de Bob plus petit de 2/3 selon la masse par rapport à self.masse

        :param grille: a 2-dimension list with a Case object
        :param show:
        :return: dangers [Bob] : list of bobs which have a mass 2/3 bigger compared to self.masse
                 foods [Case]: list of cells with food in it
                 preys [Bob] : list of bobs which have a mass 2/3 less bigger compared to self.masse
        """
        danger = False
        dangers = []
        preys = []
        foods = []
        for dx, dy in self.perception_pos:
            # génère toutes les couples (dx, dy) dans un cercle de norme radius en distance euclidienne et de centre (0, 0)
            if 0 <= self.x + dx < self.config.TAILLE and 0 <= self.y + dy < self.config.TAILLE:  # si la position qu'on regarde est bien dans la grille
                case = grille[self.x + dx][self.y + dy]
                if show :
                    case.type = "Perception"
                    case.nbPerception += 1
                    continue
                for other in case.place:  # si il y a des bobs sur cette case
                    if self.masse / other.masse < 2 / 3:  # si il y a un bob menaçant, on est en danger
                        danger = True
                        dangers.append(other)

                    if (
                    not danger) and other.masse / self.masse < 2 / 3:  # si on est pas en danger, on cherche les proies possibles
                        preys.append(other)

                if case.food > 0:  # si il y a de la nourriture on la voit
                    foods.append(case)

        return dangers, foods, preys

    def move_preference(self, grille):
        """récupere les informations sur les cases vues par le bob et choisit une direction en fonction

        Parametres:
            grille (world.grid): Une liste bidimensionnelle contenant des objets Case

        Returns:
            direction (int, int): Un tuple représentant la direction vers laquelle va se diriger le bob
        """

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # voit les cases qu'il perçoit
        dangers, foods, prey = self.see(grille)

        for food in foods:
            self.mem_food.add(food)

        # si il y a un danger on fuit
        if dangers:
            for e in directions:  # detection d'obstacle/bords de carte
                if is_obstacle(e[0], e[1]):
                    directions.remove(e)

            dangers.sort(key=lambda b: distance((b.x, b.y), (self.x, self.y)), reverse=True)
            dax = dangers[0].x
            day = dangers[0].y

            for dx, dy in directions:
                dmax = distance((dax, day), (self.x, self.y))
                if distance((dax, day), (self.x + dx, self.y + dy)) > dmax:
                    directions.remove((dx, dy))
                    dmax = distance((dax, day), (self.x + dx, self.y + dy))

            if not directions:
                directions.append((0, 0))

            return choice(directions)

        # si il y a de la nourriture en vue on y va
        foods = [case for case in set(foods) if case != grille[self.x][self.y]]
        if foods:
            for food in foods:
                self.mem_food.add(food)

            if len(foods) > 1: foods.sort(key=lambda case: case.food if case != grille[self.x][self.y] else -1,
                                          reverse=True)
            target = (foods[0].x, foods[0].y)  # case avec la meilleure food
            current = (self.x, self.y)  # case actuelle
            vector = (target[0] - current[0], target[1] - current[1])  # direction vectorielle vers target
            # choix des deux meilleures directions (si il y en a deux)
            directions = []
            if vector[0] != 0: directions.append((vector[0] // abs(vector[0]), 0))
            if vector[1] != 0: directions.append((0, vector[1] // abs(vector[1])))
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

        visited_cases = self.place_historic.remember(self.memory_points)
        for case in visited_cases :
            for dx,dy in directions:
                if (case.x,case.y) == (self.x + dx,self.y+dy):
                    directions.remove((dx,dy))
        if directions :
            directions =[(-1, 0), (1, 0), (0, -1), (0, 1)]

        
        return choice(directions)

    def areInSameFamily(self, other_bob):
        """Méthode qui détermine si deux bobs sont de la même famille

        Parametres:
            other_bob (Bob): Le bob que l'on va comparer avec self

        Returns:
            Boolean
        """
        if self == other_bob:
            return True

        family = set()
        family.add(self)

        for _ in range(self.config.DISTANCE_TO_BE_IN_SAME_FAMILY):  # recherche en largeur dans l'arbre généalogique
            tmp = set()
            for bob in family:
                tmp.update(bob.parents.union({bro for parent in bob.parents for bro in parent.childs if bro != self}))
                tmp.update(bob.childs)
            family = tmp.copy()
            if other_bob in family:
                return True
        return False

def choice(liste):
    return liste[int(random()*len(liste))]
