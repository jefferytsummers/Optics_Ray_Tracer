from matplotlib.figure import Figure

class Lens():
    def __init__(self, zLoc, fL, height):
        self.pos    = zLoc
        self.height = height
        self.fL     = fL
    def draw_Lens(self, diagram):
        diagram.vlines(self.pos, -(self.height/2), self.height/2)
        
