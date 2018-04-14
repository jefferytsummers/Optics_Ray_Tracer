from math import tan, pi

from tkinter    import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import *
use("TkAgg")
class RayDiagram(Frame):
    """ 
    This class creates the actual ray diagram graph in a tkinter frame which is 
    packed into the application window.
    This class contains the following methods:
    1) __init__      - initializes the ray diagram to just draw the lens
    2) draw_rays     - draws rays on the ray diagram using the paraxial approximation
    3) clear_diagram - clears the diagram of any rays. This should be called before draw_rays()
    4) restart       - reinitializes the graph to only display the lens
    """
    def __init__(self, root):
        """ Initializes the ray diagram, creating a lens of height 0 at the origin """
        Frame.__init__(self, root)
        label = Label(self, text="Ray Diagram")
        label.pack(pady=10,padx=10)
        
        # Data created upon instantiation of a RayDiagram object
        self.root = root
        # Height of lens, will be displayed in the ray diagram.
        self.incidentAngle  = 0
        self.lensHeight     = 0
        self.focalLength    = 1
        # Create a matplotlib figure
        self.fig = Figure(figsize=(5,2.5), dpi=100)
        # Add a subplot to the figure, this is the "graph"
        self.ax  = self.fig.add_subplot(111)
        self.ax.set_title("Thin Lens - Object at Infinity")
        # Display the lens on the ray diagram
        self.ax.vlines([0], [-self.lensHeight], [self.lensHeight], color="blue")
        # Instantiate the canvas on which our graph will be displayed
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        NavigationToolbar2TkAgg(self.canvas, self).update()
        self.canvas.show()
        self.canvas.get_tk_widget()
        self.draw_rays(self.incidentAngle, self.lensHeight, self.focalLength)
    def draw_rays(self, incidentAngle, lensHeight, focalLength):
        """ Draws rays to the canvas which will then be displayed """
        # Declaring two 2-D lists which will store the information about the rays
        # This could be expanded to have as many rays as wanted
        incidentRays = [[], [], []]
        transmitRays = [[], [], []]
    
        for i in range(3):
            yIntercept = (1-i)*lensHeight/2.0
            transmitAngle   = incidentAngle*pi/180.0-(yIntercept/focalLength)
          
            incidentRays[i] = [ tan(incidentAngle*pi/180.0)*_+yIntercept  \
                               for _ in range(int(-1.5*focalLength),1)]
            transmitRays[i] = [tan(transmitAngle)*_+yIntercept  \
                               for _ in range(0,int(1.2*focalLength)+1)]
            self.ax.plot(range(int(-1.5*focalLength),1),   incidentRays[i], color='red')
            self.ax.plot(range(0,int(1.2*focalLength)+1),  transmitRays[i], color='k')

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=TOP)

    def clear_rays(self):
        """ Clears rays drawn to the canvas """
        self.pack_forget()
        
    def restart(self, incidentAngle, lensHeight, focalLength):
        """ Essientially reinitializes the default raydiagram, probably not the best methodology but it worked for me"""        
        Frame.__init__(self, self.root)
        label = Label(self, text="Ray Diagram")
        label.pack(pady=10,padx=10)
        self.lensHeight = lensHeight/2.0
        self.fig = Figure(figsize=(10,10), dpi=100)
        self.ax  = self.fig.add_subplot(111)
        self.ax.grid()
        self.ax.set_title("Thin Lens - Object at Infinity" + '\n' + r'$\alpha = %0.3f$' %incidentAngle)
        self.ax.set_xlabel("Optical Axis")
        self.ax.set_ylabel("Ray Elevation (cm)")
        self.ax.vlines([0], [-self.lensHeight], [self.lensHeight], color="blue", linewidth=5)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        NavigationToolbar2TkAgg(self.canvas, self).update()
        self.canvas.show()
        self.canvas.get_tk_widget()
        self.pack()
