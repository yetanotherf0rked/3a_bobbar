import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt 
import matplotlib.style
import matplotlib.animation as animation
import matplotlib
matplotlib.use('TkAgg')

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
        self.animation=animation #mode (animation True/False)

        #self.data dictionnaires ou seront stockées les données à afficher ou non
        self.data ={'ticks':[],
            'days':[],
            'pop': [],
            'food': [],
            'mass': ([],[],[]),
            'velocity': ([],[],[]),
            'perception': ([],[],[]),
            'memory': ([],[],[]),
            'age':([],[],[]),
            }
        
        #liste conenant les nom des données a afficher 
        self.dataTrue = ['pop']

        #parametres d'afichage (tyoe d'absysse) Affichage ou non de chaque type de donées 
        self.parametres={'x':"ticks",'pop':True,'energy':False,'mass':False,'velocity':False,'memory':False,'perception':False,'food':False,'age':False}
        #nombre de colonnes, de lignes et de graphs
        self.rows = 1
        self.collumns = 1
        self.nbgraphs = 1 
        if animation :
            self.init_annim()

    def init_annim(self):   
        self.animation=True
        plt.ion() #mode interactif
        self.auto_grid_size()
        self.fig = plt.figure()
        self.axes = [self.fig.add_subplot(self.rows,self.collumns,i) for i in range(1,self.nbgraphs+1)]
        self.lines = []
        x=self.data[self.parametres['x']]
        sub = 0
        for c in self.dataTrue:
            y = self.data[c]
            ax = self.axes[sub]
            if type(y)== tuple :
                l1, =ax.plot(x,y[0],label='moyenne')
                l2, =ax.plot(x,y[1],label='max',color='green')
                l3, = ax.plot(x,y[2],label='min')
                line=(l1,l2,l3)
            else :    
                line, = ax.plot(x,y)
            self.lines.append(line)
            sub+=1
        


    def update_data(self,grille,listbobs,tick):
        stats =update_stats_graphs(grille,listbobs,tick)

        for c in stats.keys():
            if(type(stats[c]) == tuple):
               
                self.data[c][0].append(stats[c][0])
                self.data[c][1].append(stats[c][1])
                self.data[c][2].append(stats[c][2])
            else :
                self.data[c].append(stats[c])

       

    def set_parameter(self,rows=0,collumns=0,**kwargs,):
        self.nbgraphs = 0
        self.dataTrue =[]
        self.parametres['x']= kwargs.get('x','ticks')
        for c in self.parametres.keys():
            if c!='x' :
                self.parametres[c]=kwargs.get(c,False)
                if self.parametres[c]==True :
                    self.dataTrue.append(c)
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
        if self.nbgraphs >= 7 :
            self.rows,self.collumns = 3,3
            return
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

    def import_parameter(self,param):
        self.parametres =  param
        self.dataTrue.clear()
        self.nbgraphs=0
        for c in self.parametres.keys():
            if self.parametres[c]==True :
                self.dataTrue.append(c)
                self.nbgraphs+=1
        self.auto_grid_size()  

        
    def plot(self,):
        #assert self.animation == False
        self.fig=plt.figure()
        x=self.data[self.parametres['x']]
        self.axs=[self.fig.add_subplot(self.rows,self.collumns,i) for i in range(1,self.nbgraphs+1)]
        sub = 0
        for c in self.dataTrue:
            y = self.data[c]
            ax = self.axs[sub]
            ax.set_xlabel(self.parametres['x'])
            ax.set_ylabel(c)
            if type(y)== tuple :
                ax.plot(x,y[0],label='moyenne')
                ax.scatter(x,y[1],label='max',marker='+',color='green')
                ax.scatter(x,y[2],label='min',marker='+')
                ax.legend(loc='upper left')
            else :    
                ax.plot(x,y)
            sub+=1
        self.fig.show()
        plt.show()

  

    def switch_mode(self):
        plt.close()
        if self.animation :
            plt.ioff()
            self.animation=False
        else :
            self.init_annim()

    def hide(self):
        plt.close()
        plt.ioff()

    def set_animation(self,animation):
        self.hide()
        if animation :
            self.init_annim()
        
    
    def anim(self):
        assert self.animation == True
        x=self.data[self.parametres['x']]
        sub = 0
        
        for c in self.dataTrue:
            y = self.data[c]
            ax = self.axes[sub]
            line = self.lines[sub]
            ax.set_xlabel(self.parametres['x'])
            ax.set_ylabel(c)
            if type(y)== tuple :
               line[0].set_data(x,y[0])
               line[1].set_data(x,y[1])
               line[2].set_data(x,y[2])
            else :
                line.set_xdata(x)   
                line.set_ydata(y)
            ax.relim()
            ax.autoscale_view()
            sub+=1
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def update_parameter(self,animation,parameter):
        self.hide()
        self.import_parameter(parameter)
        if animation :
            self.init_annim()






