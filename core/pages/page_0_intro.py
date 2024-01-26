import arcade

from core.classes.constants import Constants
from core.utils.utils import Gfx


class Page0Intro:

    def __goto_splash_screen(self):
        self.process.selectPage(1)

    def __init__(self, w, h, window: arcade.Window, process=None):
        super().__init__()
        self.window = window
        self.W = w
        self.H = h
        self.process = process
        # fields
        self.gfx = None
        self.index = None
        self.timer = None

    def refresh(self, args=None):
        self.window.set_viewport(0, self.W, 0, self.H)
        params = {
            "filePath" : "resources/backgrounds/ggj2k24.png",
            "size" : (self.W, self.H),
            "position" : (self.W/2, self.H/2)
        }
        ggj = Gfx.create_fixed(params)
        params["filePath"] = "resources/backgrounds/rphstudio.png"
        rph = Gfx.create_fixed(params)
        params["filePath"] = "resources/backgrounds/arcade.png"
        arc = Gfx.create_fixed(params)
        self.gfx = [(ggj, Constants.TIME_GGJ),
                    (arc, Constants.TIME_ARC),
                    (rph, Constants.TIME_RPH)]
        self.timer = 0
        self.index = 0

    def setup(self):
        self.refresh()

    def on_update(self, deltaTime):
        if self.index < len(self.gfx):
            self.timer += deltaTime
            if self.timer >= self.gfx[self.index][1]:
                self.index += 1
                self.timer = 0
            self.gfx[self.index][0].alpha = 255 * (1.0 - abs(self.timer - self.gfx[self.index][1]/2)/(self.gfx[self.index][1]/2))
        else:
            self.__goto_splash_screen()

    def draw(self):
        if self.index < len(self.gfx):
            self.gfx[self.index][0].draw()

    def onKeyEvent(self, key, isPressed):
        if isPressed:
            self.__goto_splash_screen()

    def onButtonEvent(self, gamepadNum, buttonName, isPressed):
        if isPressed:
            self.__goto_splash_screen()

    def onAxisEvent(self, gamepadNum, axisName, analogValue):
        pass

    def onMouseMotionEvent(self, x, y, dx, dy):
        pass

    def onMouseButtonEvent(self, x, y, buttonNum, isPressed):
        if isPressed:
            self.__goto_splash_screen()

