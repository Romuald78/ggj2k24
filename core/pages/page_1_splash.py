import arcade

from core.classes.constants import Constants
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
            "filePath" : "resources/backgrounds/splash_back.png",
            "size" : (self.W, self.H),
            "position" : (self.W/2, self.H/2)
        }
        self.gfx =Gfx.create_fixed(params)

    def setup(self):
        self.refresh()

    def on_update(self, deltaTime):
        pass

    def draw(self):
        self.gfx.draw()

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
        if isPressed:
            self.__go_to_select(Constants.MOUSE_CTRL)


