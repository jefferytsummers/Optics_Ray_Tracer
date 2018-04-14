""" Ray Tracing Program"""
#################################################################
# Author:       Jeffery Summers                                 #
# Filename:     RayTracer.py                                    #
# Description: Version 2 of the ray tracing program for PHYS    #
#              3520. This program
#################################################################

# Used for creating the GUI
from tkinter    import *


# Personally designed classes
# Used to create the ray diagram in the GUI, see raydiagram.py for documentation
from raydiagram import RayDiagram
# Used to create the GUI, see raygui.py for more documentation
from raygui import RayGUI

def main():
    # Declare main window, give it a title, specify dimensions
    root = Tk()
    root.title("Ray Tracer")
    root.geometry("1280x720+500+100")
    # Create and display the ray diagram
    graph = RayDiagram(root)
    graph.pack(side=RIGHT)
    # Display a GUI on the main window, to the left of the ray diagram
    rayGUI = RayGUI(root, graph)
    rayGUI.pack(side=LEFT)
    root.mainloop()
main()
