from random import random

import arcade
import json

from core.classes.People import Person, Human, Cat
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
                for ctrl in args:
                    # create person according to player choice
                    if args[ctrl]['choice'] == "human":
                        x = human_start[0] + (random() - 0.5) * human_start[2]
                        y = human_start[1]
                        p = Human(ctrl, x0=x, y0=y)
                    elif args[ctrl]['choice'] == "cat":
                        x = cat_start[0] + (random() - 0.5) * cat_start[2]
                        y = cat_start[1]
                        p = Cat(ctrl, x0=x, y0=y)
                    # add person to the people list
                    self.people.append(p)

    def setup(self):
        self.refresh()

    def on_update(self, deltaTime):
        for p in self.people:
            p.update(deltaTime)

    def draw(self):
        # Background
        self.map.draw_back()
        # Draw back items
        # TODO
        # Draw players
        for p in self.people:
            p.draw()
        # Draw front items
        # TODO

    def onKeyEvent(self, key, isPressed):
        pass

    def onButtonEvent(self, gamepadNum, buttonName, isPressed):
        pass

    def onAxisEvent(self, gamepadNum, axisName, analogValue):
        pass

    def onMouseMotionEvent(self, x, y, dx, dy):
        pass

    def onMouseButtonEvent(self, x, y, buttonNum, isPressed):
        if Constants.DEBUG:
            xp = x / self.W
            yp = y / self.H
            print(xp, yp)

