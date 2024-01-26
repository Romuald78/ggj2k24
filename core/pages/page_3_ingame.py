import arcade

from core.classes.constants import Constants
from core.utils.utils import Gfx


class Page3InGame:

    def __init__(self, w, h, window: arcade.Window, process=None):
        super().__init__()
        self.window = window
        self.W = w
        self.H = h
        self.process = process

    def refresh(self, args=None):
        self.window.set_viewport(0, self.W, 0, self.H)
        # Select first player (use given controller number)
        if args is not None:
                print(args)

    def setup(self):
        self.refresh()

    def on_update(self, deltaTime):
        pass

    def draw(self):
        pass

    def onKeyEvent(self, key, isPressed):
        pass

    def onButtonEvent(self, gamepadNum, buttonName, isPressed):
        pass

    def onAxisEvent(self, gamepadNum, axisName, analogValue):
        pass

    def onMouseMotionEvent(self, x, y, dx, dy):
        pass

    def onMouseButtonEvent(self, x, y, buttonNum, isPressed):
        pass

