from matplotlib.figure import Figure


class Lens():
    def __init__(self, fL, height):
        self.height = height
        self.fL = fL

    def draw(self, pos, diagram):
        diagram.vlines(pos, -(self.height/2), self.height/2)
