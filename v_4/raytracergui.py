from tkinter    import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import *
import numpy as np
from lens import Lens
use("TkAgg")
class RayTracerGUI(Frame):
    # Initializes the gui, creates a blank matplotlib graph, blank entry fields and an update button.
    def __init__(self, root):
        Frame.__init__(self, root)
        """ This block of code takes care of packing a matlotlib graph to the screen """
        self.root = root
        # Declare a frame for the matplotlib graph to be stored in
        self.diagramFrame = Frame(master=self.root)
        self.diagramFrame.pack(side=BOTTOM)
        # Create matplotlib figure. This is the container for the graph
        self.graph = Figure(figsize=(10,7), dpi=100)
        # Add a subplot to the figure, this is the "graph"
        self.diagram  = self.graph.add_subplot(111)
        self.diagram.set_title("Focusing with a Single Lens")
        self.diagram.grid()
        # Instantiate the canvas on which our graph will be displayed

        self.canvas = FigureCanvasTkAgg(self.graph, self.diagramFrame)
        NavigationToolbar2TkAgg(self.canvas, self.diagramFrame).update()
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=TOP)

        leftFrame = Frame(master=self)
        """ Entry Fields """
        # We need a frame to store the entry boxes in
        entryFrame = Frame(master=leftFrame, borderwidth=2, padx=2, pady=2, relief=SUNKEN)
        entryFrameTitle = Label(master=entryFrame, text='Parameters')
        entryFrameTitle.pack(side=TOP)
        entryFrame.pack(side=LEFT)
        # We also need individual frames for each parameter
        fObjFrame       = Frame(master=entryFrame)
        objHeightFrame  = Frame(master=entryFrame)
        fEyeFrame       = Frame(master=entryFrame)
        eyeHeightFrame  = Frame(master=entryFrame)
        # Pack the individual entry frames
        fObjFrame.pack()
        objHeightFrame.pack()
        fEyeFrame.pack()
        eyeHeightFrame.pack()
        # Add labels for the entry boxes
        Label(fObjFrame, text="Objective Focal Length (cm)").pack(side=LEFT)
        Label(objHeightFrame, text="Objective Lens Height (cm)").pack(side=LEFT)
        Label(fEyeFrame, text="Eyepiece Focal Length (cm)").pack(side=LEFT)
        Label(eyeHeightFrame, text="Eyepiece Height (cm)").pack(side=LEFT)
        # Declare variables to be held in entry Boxes
        self.fObj       =   StringVar()
        self.objHeight  =   StringVar()
        self.fEye       =   StringVar()
        self.eyeHeight  =   StringVar()
        # Add entry boxes to each entry frame
        fObjEntry   = Entry(fObjFrame,          textvariable=self.fObj)
        objHeightEntry  = Entry(objHeightFrame, textvariable=self.objHeight)
        fEyeEntry   = Entry(fEyeFrame,          textvariable=self.fEye)
        eyeHeightEntry  = Entry(eyeHeightFrame, textvariable=self.eyeHeight)

        fObjEntry.pack(side=LEFT)
        objHeightEntry.pack(side=LEFT)
        fEyeEntry.pack(side=LEFT)
        eyeHeightEntry.pack(side=LEFT)

        Button(master=entryFrame, text="Update Ray Diagram", command=lambda: self.update()).pack(side=BOTTOM,padx=50)
        leftFrame.pack(side=LEFT)
    def create_lens(self, ):
        self.d  = float(self.lensHeight.get())      # Height of lens
        self.f  = float(self.focalLength.get())     # Focal length of the lens

    def create_rays(self):
        """ Plots rays connecting object->lens and lens->image on the current ray diagram """
        lDomain = np.linspace(-self.so, 0, 10)
        rDomain = np.linspace(0, self.si, 10)
        self.diagram.vlines(0, -self.d / 2, self.d/2, \
                       color='black', linewidth=2, \
                       label='Lens')                # Plot the lens
        self.diagram.vlines(self.si, 0, self.hi, \
                       color='green', label='Image')# Plot the image
        for i in range(3):
            yInt = (1-i)*self.d/2
            # Plot the rays
            self.diagram.plot(lDomain, np.array([((yInt-self.ho)/self.so)*_+yInt    for _ in lDomain]),  \
                         color='blue')
            self.diagram.plot(rDomain, np.array([((self.hi-yInt)/(self.si-0))*_+yInt for _ in rDomain]), \
                         color='green')

    def update(self):
        # Clear the current diagram just before displaying all the newly calculated items.
        self.diagram.cla()

        # Do calculations before clearing the diagram
        self.create_lens()      # Create a lens object. Stores lens height and focal length as class data
        self.objLens = Lens(0, self.fObj, self.objHeight)
        self.create_object()    # Create an object object (lol). Stores object position and height as class data
        self.create_image()     # Create an image object. Calculates and stores image position and height.

        # Plot the rays using the create_rays method
        self.create_rays()
        # Plot a line connecting the object to its image
        self.diagram.hlines(0, -self.so, self.si, linestyles='dashed')
        # Switch statements for plotting the arrow-tips correctly
        if self.ho > 0:
            self.diagram.plot(-self.so, self.ho, '^', color='blue')
        elif self.ho <0:
            self.diagram.plot(-self.so, self.ho, 'v', color='blue')
        if self.hi > 0:
            self.diagram.plot(self.si, self.hi, '^', color='green')
        elif self.hi < 0:
            self.diagram.plot(self.si, self.hi, 'v', color='green')

        # Set the title of the ray diagram, show a grid, and finally, display the ray diagram.
        self.diagram.set_title("Focusing with a Single Lens")
        self.diagram.grid()
        self.diagram.legend()
        self.canvas.show()
