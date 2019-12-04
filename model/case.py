from random import randint

class Case:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.food = 0
        self.place = []        #Contenue de la Case