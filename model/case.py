from random import randint
import pygame

class Case:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.food = 0
        self.place = []   #Contenue de la Case
        self.type = "Normal"
        self.nbPerception = 0

    def draw(self,surface,xdec,ydec,Px_init,Py_init,depx,depy,cx):
        x,y = self.x,self.y
        if self.type == "Normal":
            couleur = (38,37,42)
        if self.type == "Perception":
            print(self.nbPerception)
            couleur = (max(0,173-20 * self.nbPerception), max(0,205-20*self.nbPerception), 226)
        pygame.draw.polygon(surface, couleur, [(cx+Px_init + depx + xdec * (x-y-1), Py_init + depy + ydec *  (x+y+1)) ,(cx+Px_init + depx + xdec * (x-y), Py_init + depy + ydec *  (x+y)),(cx+Px_init + depx + xdec * (x-y+1), Py_init + depy + ydec *  (x+y+1)) , (cx+Px_init + depx + xdec * (x-y), Py_init + depy + ydec *  (x+y+2)) ])
        pygame.draw.line(surface, (228,226,232),
                         (cx+Px_init + depx + xdec * (x-y-1), Py_init + depy + ydec *  (x+y+1)),
                         (cx+Px_init + depx + xdec * (x-y), Py_init + depy + ydec *  (x+y)))
        pygame.draw.line(surface, (228, 226, 232),
                         (cx + Px_init + depx + xdec * (x - y), Py_init + depy + ydec * (x + y)),
                         (cx+Px_init + depx + xdec * (x-y+1), Py_init + depy + ydec *  (x+y+1)))
        self.nbPerception = 0

    def copie(self):
        case = Case(self.x,self.y)
        case.food = self.food
        case.place = [bob.copie() for bob in self.place]
        case.type = self.type
        self.type = "Normal"
        return case

    def bobCase(self,n,x,y,xdec,ydec):
        if n == 1:
            return [(xdec * (x - y),ydec * (x + y + 1))]
        if n == 2:
            return [(xdec * (x - y - 1/4),ydec * (x + y + 1 - 1/4)),
                    (xdec * (x - y + 1/4),ydec * (x + y + 1 + 1/4))]
        if n == 3:
            return [(xdec * (x - y),ydec * (x + y + 1 - 1/4)),
                    (xdec * (x - y - 1/4),ydec * (x + y + 1 + 1/4)),
                    (xdec * (x - y + 1/4),ydec * (x + y + 1 + 1/4))]
        if n == 4:
            return [(xdec * (x - y - 1 / 4), ydec * (x + y + 1 - 1 / 4)),
                    (xdec * (x - y + 1 / 4), ydec * (x + y + 1 - 1 / 4)),
                    (xdec * (x - y - 1 / 4), ydec * (x + y + 1 + 1 / 4)),
                    (xdec * (x - y + 1 / 4), ydec * (x + y + 1 + 1 / 4))]
        if n == 5:
            return [(xdec * (x - y - 1 / 4), ydec * (x + y + 1 - 1 / 4)),
                    (xdec * (x - y + 1 / 4), ydec * (x + y + 1 - 1 / 4)),
                    (xdec * (x - y), ydec * (x + y + 1)),
                    (xdec * (x - y - 1 / 4), ydec * (x + y + 1 + 1 / 4)),
                    (xdec * (x - y + 1 / 4), ydec * (x + y + 1 + 1 / 4))]