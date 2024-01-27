import arcade

from core.classes.constants import Constants
from core.utils.utils import Gfx


class Item:

    def __init__(self, name, x0=0, y0=0, ratio=1.0):
        f1 = f"{name}.png"
        f2 = f"{name} contour.png"
        # ITEM
        params = {
            "filePath": f"resources/items/{f1}",
            "position": (x0, y0)
        }
        self.__gfx = Gfx.create_fixed(params)
        # HIGH LIGHT
        params = {
            "filePath": f"resources/items/{f2}",
            "position": (x0, y0)
        }
        self.__gfx2 = Gfx.create_fixed(params)
        # scale and move
        self.__gfx.scale      = ratio
        self.__gfx2.scale     = ratio
        self.__gfx.center_y  += self.__gfx.height / 2
        self.__gfx2.center_y += self.__gfx2.height / 2
        # other fields
        self.__highlighted = True

    def highlight(self, mode):
        self.__highlighted = mode

    @property
    def x(self):
        return self.__gfx.center_x

    @property
    def y(self):
        return self.__gfx.center_y

    @property
    def left(self):
        return self.x - self.__gfx.width / 2

    @property
    def right(self):
        return self.x + self.__gfx.width / 2

    @property
    def top(self):
        return self.y - self.__gfx.height / 2

    @property
    def bottom(self):
        return self.y + self.__gfx.height / 2

    def draw(self):
        if Constants.DEBUG:
            arcade.draw_rectangle_outline(
                (self.left + self.right) / 2,
                (self.top + self.bottom) / 2,
                self.right - self.left,
                self.top-self.bottom, (0,0,0,128), 3
            )
        if self.__highlighted:
            self.__gfx2.draw()
        self.__gfx.draw()