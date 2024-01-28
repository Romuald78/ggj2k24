from core.classes.People import Cat
from core.utils.utils import Gfx


class Pigeon:

    def __init__(self, x0=0, y0=0, ratio=1.0):
        params = {
            "filePath": "resources/characters/pigeon.png",
            "position": (x0, y0)
        }
        self.gfx = Gfx.create_fixed(params)
        params = {
            "filePath": "resources/characters/pigeon contour.png",
            "position": (x0, y0)
        }
        self.gfx2 = Gfx.create_fixed(params)
        self.gfx.scale = ratio
        self.gfx2.scale = ratio
        self.gfx.center_y += self.gfx.height  / 2
        self.gfx2.center_y += self.gfx.height / 2
        self.state = "away" # away / fly_in / idle / fly_out
                            #                      / dead
        self .highlighted = False

    def can_interact(self, player):
        return type(player) is Cat

    def highlight(self, value, clr=(255,255,255)):
        self.highlighted = value
        self.gfx2.color = clr

    def getPosition(self):
        return (self.gfx.center_x, self.gfx.center_y)

    @property
    def width(self):
        return self.gfx.width

    @property
    def height(self):
        return self.gfx.height

    @property
    def left(self):
        return self.gfx.center_x - self.gfx.width / 2

    @property
    def right(self):
        return self.gfx.center_x + self.gfx.width / 2

    @property
    def top(self):
        return self.gfx.center_y + self.gfx.height / 2

    @property
    def bottom(self):
        return self.gfx.center_y - self.gfx.height / 2

    def update(self, deltaTime):
        pass

    def draw(self):
        if self.highlighted:
            self.gfx2.draw()
        self.gfx.draw()

