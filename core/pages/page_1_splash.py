import arcade

from core.classes.constants import Constants
from core.classes.people.cat import Cat
from core.utils.utils import Gfx


class Page1Splash:

    def __go_to_select(self, ctrl):
        self.process.selectPage(2, {'ctrl': ctrl})

    def __init__(self, w, h, window: arcade.Window, process=None):
        super().__init__()
        self.window = window
        self.W = w
        self.H = h
        self.process = process
        # fields
        self.gfx = None

    def refresh(self, args=None):
        self.window.set_viewport(0, self.W, 0, self.H)
        params = {
            "filePath" : "resources/backgrounds/fond maison.png",
            "size" : (self.W, self.H),
            "filterColor": (255,255,255,128),
            "position" : (self.W/2, self.H/2)
        }
        self.gfx =Gfx.create_fixed(params)
        params = {
            "filePath": "resources/backgrounds/kitty khaos logo.png",
            "size": (self.W/1.5, self.H/1.5),
            "position": (self.W / 2, self.H * 3 )
        }
        self.title = Gfx.create_fixed(params)
        self.cat   = Cat(0, x0=self.W*2, y0=self.H/15, ratio=2.0, clr=' white')


    def setup(self):
        self.refresh()

    def on_update(self, deltaTime):
        k = 0.95
        self.title.center_y = self.title.center_y * k + (1-k) * self.H/2
        if self.cat.x >= self.W * 1.5:
            self.cat.move_left(True)
            self.cat.move_right(False)
        if self.cat.x <= - self.W * 0.5:
            self.cat.move_left(False)
            self.cat.move_right(True)
        self.cat.update(deltaTime)

    def draw(self):
        self.gfx.draw()
        self.title.draw()
        self.cat.draw()

    def onKeyEvent(self, key, isPressed):
        if isPressed:
            self.__go_to_select(Constants.KEYBOARD_CTRL)

    def onButtonEvent(self, gamepadNum, buttonName, isPressed):
        if isPressed:
            self.__go_to_select(gamepadNum)

    def onAxisEvent(self, gamepadNum, axisName, analogValue):
        pass

    def onMouseMotionEvent(self, x, y, dx, dy):
        pass

    def onMouseButtonEvent(self, x, y, buttonNum, isPressed):
        pass
        # if isPressed:
        #     self.__go_to_select(Constants.MOUSE_CTRL)


