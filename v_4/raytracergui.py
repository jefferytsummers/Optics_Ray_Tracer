from math import tan, pi


from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import *
use("TkAgg")
import numpy as np


from lens import Lens


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
        self.graph = Figure(figsize=(10, 7), dpi=100)
        # Add a subplot to the figure, this is the "graph"
        self.diagram = self.graph.add_subplot(111)
        self.diagram.set_title("Focusing with a Single Lens")
        self.diagram.grid()
        # Instantiate the canvas on which our graph will be displayed

        self.canvas = FigureCanvasTkAgg(self.graph, self.diagramFrame)
        NavigationToolbar2TkAgg(self.canvas, self.diagramFrame).update()
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP)

        leftFrame = Frame(master=self)
        """ Entry Fields """
        # We need a frame to store the entry boxes in
        entryFrame = Frame(master=leftFrame, borderwidth=2, padx=2, pady=2, relief=SUNKEN)
        entryFrameTitle = Label(master=entryFrame, text='Parameters')
        entryFrameTitle.pack(side=TOP)
        entryFrame.pack(side=LEFT)
        # We also need individual frames for each parameter
        fObjFrame = Frame(master=entryFrame)
        objHeightFrame = Frame(master=entryFrame)
        fEyeFrame = Frame(master=entryFrame)
        eyeHeightFrame = Frame(master=entryFrame)
        alphaFrame = Frame(master=entryFrame)
        # Pack the individual entry frames
        fObjFrame.pack()
        objHeightFrame.pack()
        fEyeFrame.pack()
        eyeHeightFrame.pack()
        alphaFrame.pack()
        # Add labels for the entry boxes
        Label(fObjFrame, text="Objective Focal Length (cm)").pack(side=LEFT)
        Label(objHeightFrame, text="Objective Lens Height (cm)").pack(side=LEFT)
        Label(fEyeFrame, text="Eyepiece Focal Length (cm)").pack(side=LEFT)
        Label(eyeHeightFrame, text="Eyepiece Height (cm)").pack(side=LEFT)
        Label(alphaFrame, text="Incident Angle (degrees)").pack(side=LEFT)
        # Declare variables to be held in entry Boxes
        self.fObj = StringVar()
        self.objHeight = StringVar()
        self.fEye = StringVar()
        self.eyeHeight = StringVar()
        self.alpha = StringVar()
        # Add entry boxes to each entry frame
        fObjEntry = Entry(fObjFrame, textvariable=self.fObj)
        objHeightEntry = Entry(objHeightFrame, textvariable=self.objHeight)
        fEyeEntry = Entry(fEyeFrame, textvariable=self.fEye)
        eyeHeightEntry = Entry(eyeHeightFrame, textvariable=self.eyeHeight)
        alphaEntry = Entry(alphaFrame, textvariable=self.alpha)
        # Pack the entry boxes
        fObjEntry.pack(side=LEFT)
        objHeightEntry.pack(side=LEFT)
        fEyeEntry.pack(side=LEFT)
        eyeHeightEntry.pack(side=LEFT)
        alphaEntry.pack(side=LEFT)
        # Create and pack the update button
        Button(master=entryFrame, text="Update Ray Diagram",
               command=lambda: self.update()).pack(side=BOTTOM, padx=50)
        leftFrame.pack(side=LEFT)

    def create_rays(self, objLens, eyeLens):
        """ Plots rays from a point source at infinity to the first lens,
        from the first lens to the second lens, and finally from the second
        lens to the exit pupil """
        sep = objLens.fL+eyeLens.fL  # separation distance between the lenses
        # First define the relevant domains
        dom = [np.linspace(-0.5*objLens.fL, 0, 10),
               np.linspace(0, sep, 10),
               np.linspace(sep, (sep+0.5*eyeLens.fL), 10)]

        # Define f1, f2 for easier calculations
        f1 = objLens.fL
        f2 = eyeLens.fL
        # Relief value; found as the image of the object lens wrt the eyepiece
        R = sep*f2/(sep-f2)
        # Store alpha1, we need 3 values for 3 rays
        alpha1 = [float(self.alpha.get())*pi/180.0]*3
        alpha2 = []
        alpha3 = []
        # Calculate the first ray
        ray1 = [[], [], []]
        ray2 = [[], [], []]
        ray3 = [[], [], []]
        for i in range(3):
            x1 = (1-i)*objLens.height/2
            ray1[i] = np.array([alpha1[i]*_+x1 for _ in dom[0]])

            alpha2.append(alpha1[i]-(x1/f1))
            x2 = x1
            ray2[i] = np.array([alpha2[i]*_+x2 for _ in dom[1]])

            alpha3.append(-f1/f2*alpha1[i])
            x3 = (f1+f2)*alpha1[i]+(2-f2/f1)*x1
            ray3[i] = np.array([alpha3[i]*_+x3 for _ in dom[2]])

        rays = [ray1, ray2, ray3]
        return dom, rays
        pass

    def update(self):
        # Do calculations before clearing the diagram
        objLens = Lens(float(self.fObj.get()), float(self.objHeight.get()))
        eyeLens = Lens(float(self.fEye.get()), float(self.eyeHeight.get()))
        # Clear the current diagram just before displaying all the newly calculated items.
        self.diagram.cla()
        # Plot the rays using the create_rays method
        dom, rays = self.create_rays(objLens, eyeLens)

        objLens.draw(0, self.diagram)
        eyeLens.draw(objLens.fL+eyeLens.fL, self.diagram)
        for i in range(3):
            self.diagram.plot(dom[0], rays[0][i], color="red")
            self.diagram.plot(dom[1], rays[1][i], color="blue")
            self.diagram.plot(dom[2], rays[2][i], color="green")
        # Set the title of the ray diagram, show a grid, and finally, display the ray diagram.
        self.diagram.set_title("Focusing with a Single Lens")
        self.diagram.grid()
        self.diagram.legend()
        self.canvas.draw()
