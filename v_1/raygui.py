# Used for entry boxes and buttons
from tkinter import *

# Personal class used to display the ray diagram
from raydiagram import RayDiagram

class RayGUI(Frame):
    """ Creates entry boxes in the primary application to the left """
    """ of the ray diagram. Important variables such as incdt   """
    """ angle, lens height, and focal length are stored in these.  """
    def __init__(self, root, raydiagram):
        """ Create a frame which holds three entry boxes """
        Frame.__init__(self, root)
        label = Label(self, text="Ray Diagram Text Entry")
        label.pack()
        
        # Store the raydiagram as an attribute of the RayGUI class
        self.raydiagram = raydiagram
        
        # Frame in which the GUI resides
        entryFrame = Frame(master=root)
        
        # Frames for each entry box
        self.incdtAngleFrame  = Frame(master=self)
        self.lensHeightFrame  = Frame(master=self)
        self.focalLengthFrame = Frame(master=self)
        
        # Pack the frames into the primary frame; entryFrame
        self.incdtAngleFrame.pack(pady=2,padx=5)
        self.lensHeightFrame.pack(pady=2,padx=5)
        self.focalLengthFrame.pack(pady=2,padx=5)
        
        # Declare Labels for the entry boxes
        Label(self.incdtAngleFrame,  text="Incident Angle" ).pack(side=LEFT, \
                                                             pady=2,padx=10)
        Label(self.lensHeightFrame,  text="Lens Height"    ).pack(side=LEFT, \
                                                             pady=2,padx=18)
        Label(self.focalLengthFrame, text="Focal Length"   ).pack(side=LEFT, \
                                                             pady=2,padx=15)
        # Declare instances of incdtAngle, lensHeight, and focalLength
        # which are to be stored as textvariables in the entry boxes
        incdtAngle  = StringVar()
        lensHeight  = StringVar()
        focalLength = StringVar()

        # Declare entry fields for the variables. The program will constantly
        # check the value of the entry boxes and update the rays in real time
        # using the RayDiagram class's draw_rays method.
        incdtAngleEntry     = Entry(self.incdtAngleFrame,  textvariable=incdtAngle)
        lensHeightEntry     = Entry(self.lensHeightFrame,  textvariable=lensHeight)
        focalLengthEntry    = Entry(self.focalLengthFrame, textvariable=focalLength)
        
        # Pack each entry box into their respective frames
        incdtAngleEntry.pack(side=LEFT)
        lensHeightEntry.pack(side=LEFT)
        focalLengthEntry.pack(side=LEFT)
        self.incidentAngle = incdtAngle.get()

        # Create a button which updates all important variables by checking the entry
        # boxes.
        updateButton = Button(
            master=self, text="Update Ray Diagram", \
            command=lambda: self.update_ray_diagram(incdtAngle, lensHeight, focalLength))
        updateButton.pack(side=LEFT,padx=50)
    def update_ray_diagram(self, incdtAngle, lensHeight, focalLength):
        # declare all variables as attributes of the rayGUI object
        self.incidentAngle  = float(incdtAngle.get())
        self.lensHeight     = float(lensHeight.get())
        self.focalLength    = float(focalLength.get())
        
        self.raydiagram.clear_rays()
        self.raydiagram.restart(self.incidentAngle, self.lensHeight, self.focalLength)
        self.raydiagram.draw_rays(self.incidentAngle, self.lensHeight, self.focalLength)
        
