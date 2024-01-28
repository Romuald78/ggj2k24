from random import random

import arcade
import json

from core.classes.IALogic import iaDrawStep
from core.classes.LooseTimer import LooseTimer
from core.classes.People import Person, Human, Cat
from core.classes.QTELogic import notifyQTEInteraction, qteDraw
from core.classes.StairsLogic import processStairsAction
from core.classes.constants import Constants
from core.classes.map import Map
from core.utils.utils import Gfx


class Page3InGame:

    def __find_player(self, ctrl):
        for p in self.people:
            if p.ctrl == ctrl:
                return p
        return None

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
                        p = Human(ctrl, x0=x, y0=y, ratio=self.map.ratio)
                    elif args[ctrl]['choice'] == "cat":
                        x = cat_start[0] + (random() - 0.5) * cat_start[2]
                        y = cat_start[1]
                        p = Cat(ctrl, x0=x, y0=y, ratio=self.map.ratio)
                    # add person to the people list
                    self.people.append(p)

        self.looseTimer = LooseTimer(60*2,self.W,self.H,self.map.ia)

    def setup(self):
        self.refresh()

    def on_update(self, deltaTime):
        if(self.looseTimer.isOver()):
            self.process("loose")
            return

        for p in self.people:
            p.update(deltaTime)
            # This method checks collisions with walls
            # if a collision occurs, the player is moved correctly.
            # [TODO] This method also checks if the player can interact with items
            # If true, the related item is highlighted
            self.map.process_player(p)
        self.map.ia.update(deltaTime)
        self.looseTimer.update(deltaTime)

    def draw(self):
        # Background
        self.map.draw_background()
        # Draw back items
        self.map.draw_items("back")
        # Draw players
        for p in self.people:
            p.draw()
        # Draw front items
        self.map.draw_items("front")

        # TODO
        qteDraw(self.map.qte,self.map.ia)
        self.map.ia.draw()
        self.looseTimer.draw()

    def onKeyEvent(self, key, isPressed):
        p = self.__find_player(Constants.KEYBOARD_CTRL)
        if p is not None:
            if key == arcade.key.LEFT or key == arcade.key.Q:
                p.move_left(isPressed)
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                p.move_right(isPressed)
            elif not isPressed and key == arcade.key.SPACE:
                #other interactive
                if not processStairsAction(self.map.stairs, p):
                    notifyQTEInteraction(self.map.qte, p,self.map.ia)


    def onButtonEvent(self, gamepadNum, buttonName, isPressed):
        p = self.__find_player(gamepadNum)
        if p is not None and isPressed:
            #other interactive
            processStairsAction(self.map.stairs, p)

    def onAxisEvent(self, gamepadNum, axisName, analogValue):
        if axisName == "X":
            p = self.__find_player(gamepadNum)
            if p is not None:
                if analogValue <= -0.5:
                    p.move_left (True)
                    p.move_right(False)
                elif analogValue >= 0.5:
                    p.move_left (False)
                    p.move_right(True)
                else:
                    p.move_left (False)
                    p.move_right(False)


    def onMouseMotionEvent(self, x, y, dx, dy):
        p = self.__find_player(Constants.MOUSE_CTRL)
        if p is not None:
            print(p)

    def onMouseButtonEvent(self, x, y, buttonNum, isPressed):
        if Constants.DEBUG and isPressed:
            xp = x / self.W
            yp = y / self.H
            print(f"x={x} ({xp}%) y={y} ({yp}%)")

