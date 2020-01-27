import matplotlib.pyplot as plt 
import matplotlib.style
import matplotlib.animation as animation

from view.debug import update_stats_graphs

matplotlib.style.use('dark_background')

class Graph():

    """Classe pour afficher les données de la simulation sous forme de grpahiques, statiques ou animés.
        utilisation : choisir si l'animation est activé à l'instanciation ( animated_graph= Graph(animtion=True)), désactivé par défaut
        une fois initialisé regler les parametres( stats à afficher) avec la methode Set_parameter
        mettre à jour les données avec la methode update()
        dessiner ou animer avec draw()
    """

    def __init__(self,animation="False"):
        self.animation=animation
        self.data ={'ticks':[],
            'days':[],
            'pop': [],
            'food': [],
            'mass': [],
            'velocity': [],
            'perception': [],
            'memory': [],
            'age':[]
            }
        self.dataTrue = {'pop':self.data['pop']}
        self.parametres={'x':"ticks",'pop':True,'energy':False,'mass':False,'velocity':False,'memory':False,'perception':False,'food':False,'age':False}
        self.rows = 1
        self.collumns = 1
        self.nbgraphs = 1
        if animation :
            self.init_annim()

    def init_annim(self,size=(20,20)):   
        plt.ion()
        self.fig = plt.figure(figsize=size)
        self.axes = [self.fig.add_subplot(self.rows,self.collumns,i) for i in range(1,self.nbgraphs+1)]
        self.lines = []
        x=self.data[self.parametres['x']]
        sub = 0
        for c in self.dataTrue.keys():
            y = self.dataTrue[c]
            ax = self.axes[sub]
            if type(y)== tuple :
               #pour les tuples en animation on affiche seulement la valeur moyenne 
               #TODO gerer valeurs max et min 
                line, = ax.plot(x,y[2])
            else :    
                line, = ax.plot(x,y)
            self.lines.append(line)
            sub+=1
        


    def update(self,grille,listbobs,tick):
        stats =update_stats_graphs(grille,listbobs,tick)
        for c in stats.keys():
            self.data[c].append(stats[c])
        

        #print(stats.__repr__())

    def set_parameter(self,rows=0,collumns=0,**kwargs,):
        self.nbgraphs = 0
        self.parametres['x']= kwargs.get('x','ticks')
        for c in self.parametres.keys():
            if c!='x' :
                self.parametres[c]=kwargs.get(c,False)
                if self.parametres[c]==True :
                    self.dataTrue[c] = self.data[c] 
        self.nbgraphs=len(self.dataTrue)
        if rows*collumns != self.nbgraphs :
            self.auto_grid_size()
        else:
            self.rows = rows
            self.collumns = collumns    
        if self.animation : 
            plt.close()
            self.init_annim()    

    def auto_grid_size(self):
        if self.nbgraphs >= 5 :
            self.rows,self.collumns = 3,2
            return
        if self.nbgraphs >=3 :
            self.rows,self.collumns = 2,2
            return
        if self.nbgraphs == 2 :
            self.rows,self.collumns = 2,1
            return
        if self.nbgraphs == 1 :
            self.rows,self.collumns = 1,1
            return

    def draw(self,size=(20,20)):
        if self.animation : self.anim()
        else : self.plot(size=size)
        
    def plot(self,size=(20,20)):
        assert self.animation == False
        self.fig=plt.figure(figsize=size)
        x=self.data[self.parametres['x']]
        self.axs=[self.fig.add_subplot(self.rows,self.collumns,i) for i in range(1,self.nbgraphs+1)]
        sub = 0
        for c in self.dataTrue.keys():
            y = self.dataTrue[c]
            ax = self.axs[sub]
            ax.set_xlabel(self.parametres['x'])
            ax.set_ylabel(c)
            if type(y)== tuple :
                ax.plot(x,y[1],label='max')
                ax.plot(x,y[2],label='moyenne')
                ax.plot(x,y[3],label='min')
                ax.legend(loc='upper left')
            else :    
                ax.plot(x,y)
            sub+=1
    
        self.fig.savefig("GraphStatsBobbar")
        self.fig.show()
        plt.show()

    
    def anim(self):
        assert self.animation == True
        x=self.data[self.parametres['x']]
        sub = 0
        
        for c in self.dataTrue.keys():
            y = self.data[c]
            ax = self.axes[sub]
            line = self.lines[sub]
            ax.set_xlabel(self.parametres['x'])
            ax.set_ylabel(c)
            line.set_xdata(x)
            if type(y[0])== tuple :
               #pour les tuples en animation on affiche seulement la valeur moyenne 
               #TODO gerer valeurs max et min 
                y=[t[1] for t in y]
                line.set_ydata(y)
            else :    
                line.set_ydata(y)
            ax.relim()
            ax.autoscale_view()
            sub+=1
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()



