import matplotlib.pyplot as plt 
import matplotlib.style
import matplotlib.animation as animation

matplotlib.style.use('dark_background')
plt.ion()

class Graph :
    def __init__(self) :
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()
        self.dataX= []
        self.dataY= []
        self.line, = self.ax.plot(self.dataX,self.dataY)
        self.updated=False

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



