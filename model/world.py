from random import randint,random
import ressources.config
from model import *
from model.Weather import Weather


class World:
    def __init__(self,init = True):
        self.config = ressources.config.para
        self.grid=[]
        self.listebob = []
        self.foodpos =[]
        self.weather = Weather()
        if init:
            self.initWorld()
            if self.config.active_biome:
                self.createBiome()


    def initWorld(self):
        self.grid = [[Case(x, y) for y in range(self.config.TAILLE)] for x in range(self.config.TAILLE)]
        self.listebob = self.initBob()

    def copie(self):
        newWorld = World(False)
        for liste in self.grid:
            ligne = []
            for case in liste:
                newCase = case.copie()
                newWorld.listebob += newCase.place
                if newCase.food!=0:
                    newWorld.foodpos.append(newCase)
                ligne.append(newCase)
            newWorld.grid.append(ligne)
        return newWorld

    def spawnfood(self):
        for _ in range(self.config.NB_FOOD):
            x, y = randint(0, self.config.TAILLE - 1), randint(0, self.config.TAILLE - 1)
            self.grid[x][y].food += self.config.ENERGY_FOOD
            self.foodpos.append(self.grid[x][y])

    def removefood(self):
        # Suppression de la food par suppression des cases d'une liste
        for case in self.foodpos:
            case.food = 0
        self.foodpos = []

    # Initialisation des Bobs
    def initBob(self):
        listebob = []
        for bob in range(self.config.NB_POP):
            # Position du Bob
            x, y = randint(0, self.config.TAILLE - 1), randint(0, self.config.TAILLE - 1)
            bob = Bob([x, y])
            self.grid[x][y].place.append(bob)
            listebob.append(bob)
        return listebob
    
    def update_listebob(self):
        new_bobs = []
        for bob in self.listebob:
            # update du bob
            if not bob.is_dead():
                new_bobs += bob.update(self.grid)

            # Si le bob est mort on le retire
            if bob.is_dead():
                self.grid[bob.x][bob.y].place.remove(bob)
                self.listebob.remove(bob)

        # on ajoute les nouveaux nés dans la liste de bobs qui sera actualisé au prochain tick
        self.listebob += new_bobs

    def update_consommation(self):
        for bob in self.listebob:
            bob.energy_move = self.config.move_consommation(bob.velocity, bob.masse)
            bob.energy_brain = self.config.brain_consommation(bob.perception, bob.memory_points)

    def createBiome(self):
        cases = []
        for _ in range(16):
            x,y = int(random() * self.config.TAILLE), int(random() * self.config.TAILLE)
            case = self.grid[x][y]
            case.floor = "Grass"
            if random() < 0.2:
                case.deco = True
            cases.append(case)
            x, y = int(random() * self.config.TAILLE), int(random() * self.config.TAILLE)
            case = self.grid[x][y]
            case.floor = "Sand"
            if random() < 0.2:
                case.deco = True
            cases.append(case)
            x, y = int(random() * self.config.TAILLE), int(random() * self.config.TAILLE)
            case = self.grid[x][y]
            case.floor = "Water"
            if random() < 0.2:
                case.deco = True
            cases.append(case)
            x, y = int(random() * self.config.TAILLE), int(random() * self.config.TAILLE)
            case = self.grid[x][y]
            case.floor = "Lava"
            if random() < 0.2:
                case.deco = True
            cases.append(case)
        self.grow_biome(cases)

    def grow_biome(self, cases):
        newcases = []
        for case in cases:
            if case.x <= self.config.TAILLE-2:
                nextCase = self.grid[case.x + 1][case.y]
                if not nextCase.floor:
                    nextCase.floor = case.floor
                    if random() < 0.2:
                        case.deco = True
                    newcases.append(nextCase)
            if case.y <= self.config.TAILLE-2:
                nextCase = self.grid[case.x][case.y + 1]
                if not nextCase.floor:
                    nextCase.floor = case.floor
                    if random() < 0.2:
                        case.deco = True
                    newcases.append(nextCase)
            if case.y >= 1:
                nextCase = self.grid[case.x][case.y - 1]
                if not nextCase.floor:
                    nextCase.floor = case.floor
                    if random() < 0.2:
                        case.deco = True
                    newcases.append(nextCase)
            if case.x >= 1:
                nextCase = self.grid[case.x - 1][case.y]
                if not nextCase.floor:
                    nextCase.floor = case.floor
                    if random() < 0.2:
                        case.deco = True
                    newcases.append(nextCase)

        if newcases:
            self.grow_biome(newcases)
