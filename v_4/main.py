from tkinter import *
from raytracergui import *


def main():
    root = Tk()
    root.title("Ray Tracing Program v3")
    root.geometry("1600x900+2100+100")
    rayGUI = RayTracerGUI(root)
    rayGUI.diagramFrame.pack(side=RIGHT)
    rayGUI.pack(side=LEFT)
    root.mainloop()


main()
