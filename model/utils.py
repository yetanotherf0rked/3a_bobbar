from ressources.constantes import TAILLE

class Memory:

    def __init__(self,taillemax):
        self.taillemax = taillemax
        self.memory =[]

    def add(self,case) :
        for case_in_memory in self.memory:
            if case_in_memory == case:
                return None
        self.memory.insert(0,case)
        if len(self.memory)>self.taillemax:
            self.memory.pop(self.taillemax)

    def remember(self,nmbr=1):
        if nmbr>len(self.memory) : nmbr = len(self.memory)
        return [self.memory[i] for i in range(nmbr)]
    
    def forgot(self,case) :
        for i in range(len(self.memory)) :
            if self.memory[i].x == case.x and self.memory[i].y == case.y :
                self.memory.pop(i)
                break

    def is_empty(self):
        return len(self.memory)==0 


def distance(pos1,pos2):
    """ distance((x1,y1),(x2,y2))"""
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])  

def Danger_coeff(dangers,pos) :
    directions =(pos,(pos[0],pos[1]+1),(pos[0]+1,pos[1]),(pos[0],pos[1]-1),(pos[0]-1,pos[1])) #(pos,N,E,S,O)
    coef =[0,0,0,0,0]
    for d in dangers :
        for i in range(5) :
            dd = distance((d.x,d.y),directions[i])
            coef[i]+= 1 if dd==0 else 1/d


def is_obstacle(x,y):
    return x<0 or y<0 or x>=TAILLE or y>=TAILLE 
