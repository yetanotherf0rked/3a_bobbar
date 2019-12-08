from random import randint

class Case:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.food = 0
        self.place = []        #Contenue de la Case

    def copie(self):
        case = Case(self.x,self.y)
        case.food = self.food
        case.place = [bob.copie() for bob in self.place]
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