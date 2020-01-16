import matplotlib.pyplot as plt 
import matplotlib.style
import matplotlib.animation as animation

from view.debug import update_stats_graphs

matplotlib.style.use('dark_background')


class Graph :
    def __init__(self) :
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()
        self.dataX= []
        self.dataY= []
        self.line, = self.ax.plot(self.dataX,self.dataY)
        self.updated=False

    def set_labels(self,xLabel="x",yLabel="y",title=" "):
        self.ax.set_xlabel(xLabel)
        self.ax.set_ylabel(yLabel)
        self.ax.set_title(title)

    def update(self,data) :
        x,y=data
        self.dataX.append(x)
        self.dataY.append(y)
        self.updated=True

    def run(self,i) :
        if self.updated:
            self.ax.clear()
            self.line, = self.ax.plot(self.dataX,self.dataY)
            self.updated = False
        return self.line

    def launch_anim(self,data):
        #ani = animation.FuncAnimation(self.fig,self.run)
        #plt.show()
        self.update(data)
        self.line.set_xdata(self.dataX)
        self.line.set_ydata(self.dataY)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()



class Static_graph_data():

    def __init__(self) :
        self.data ={'ticks':[],
            'days':[],
            'pop': [],
            'food': [],
            'mass': [],
            'velocity': [],
            'perception': [],
            'memory': []
            }
        self.dataTrue = dict()
        self.parametres={'x':"ticks",'pop':True,'energy':False,'mass':False,'velocity':False,'memory':False,'perception':False,'food':False}
        self.rows = 1
        self.collumns = 1
        self.nbgraphs = 1

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
        print(self.nbgraphs,self.rows,self.collumns)     

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

        
    
    def plot(self,size=(20,20)):
        self.fig=plt.figure(figsize=size)
        x=self.data[self.parametres['x']]
        self.axs=[self.fig.add_subplot(self.rows,self.collumns,i) for i in range(1,self.nbgraphs+1)]
        sub = 0
        for c in self.dataTrue.keys():
            y = self.dataTrue[c]
            ax = self.axs[sub]
            print(c,sub,ax)
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

 





""""
class Static_Graph():
    def __init__(self,row=1,collumn=1):
        self.fig = plt.figure()
        self.row,self.collumn = row, collumn
        self.axs = [self.fig.add_subplot(row,collumn,i) for i in range(1,row*collumn+1)]

    def import_datas(self,dataX,dataY,subplot):
        self.axs[subplot-1].plot(dataX,dataY)

    def set_labels(self,subplot,xLabel="x",yLabel="y",title=" "):
        self.axs[i-1].set_xlabel(xLabel)
        self.axs[i-1].set_ylabel(yLabel)
        self.axs[i-1].set_title(title)

    def draw(self):
            self.fig.show()

            

        
        


"""
