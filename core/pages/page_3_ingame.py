from random import random

import arcade
import json

from core.classes.People import Person
from core.classes.constants import Constants
from core.classes.map import Map
from core.utils.utils import Gfx


class Page3InGame:

    def __init__(self, w, h, window: arcade.Window, process=None):
        super().__init__()
        self.window = window
        self.W = w
        self.H = h
        self.process = process
        self.map = None
        self.people = None

    def refresh(self, args=None):
        self.window.set_viewport(0, self.W, 0, self.H)
        # Level path
        level = "resources/json/level01.json"
        # Load map from config file
        self.map = Map(level, self.W, self.H)

        # get start positions from map
        human_start = self.map.human_start_pix
        cat_start = self.map.cat_start_pix

        # Load players (use given controller number)
        self.people = []
        # loop through all players
        if args is not None:
                for arg in args:
                    print(arg)
                    # TODO choose human or cat according to player info
                    x = human_start[0] + (random() - 0.5) * human_start[2]
                    y = human_start[1]
                    p = Person(arg, x0=x, y0=y)
                    self.people.append(p)





    def setup(self):
        self.refresh()

    def on_update(self, deltaTime):
        for p in self.people:
            p.update(deltaTime)

    def draw(self):
        self.map.draw()
        for p in self.people:
            p.draw()

    def onKeyEvent(self, key, isPressed):
        pass

    def onButtonEvent(self, gamepadNum, buttonName, isPressed):
        pass

    def onAxisEvent(self, gamepadNum, axisName, analogValue):
        pass

    def onMouseMotionEvent(self, x, y, dx, dy):
        pass

    def onMouseButtonEvent(self, x, y, buttonNum, isPressed):
        xp = x / self.W
        yp = y / self.H
        if Constants.DEBUG:
            print( xp, yp )

