from random import random

import arcade

from core.classes.AngerBar import drawAngerBar
from core.classes.LooseTimer import LooseTimer
from core.classes.people.cat import Cat
from core.classes.people.human import Human
from core.classes.QTELogic import notifyQTEInteraction, qteDraw, qteUpdate
from core.classes.StairsLogic import processStairsAction
from core.classes.constants import Constants
from core.classes.map import Map


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
                        catclr = args[ctrl]['cat_color']
                        p = Cat(ctrl, x0=x, y0=y, ratio=self.map.ratio, clr=catclr)
                    # add person to the people list
                    self.people.append(p)

        self.looseTimer = LooseTimer(Constants.GAME_TIME,self.W,self.H,self.map.ia, proc=self.process)


    def setup(self):
        self.refresh()


    def on_update(self, deltaTime):
        # players
        if(self.looseTimer.isOver()):
            return

        # clear all highlights
        self.map.clear_highlights()
        for p in self.people:
            p.update(deltaTime)
            # This method checks collisions with walls
            # if a collision occurs, the player is moved correctly.
            # This method also checks if the player can interact with items
            # If true, the related item is highlighted
            self.map.process_player(p, deltaTime)



        self.map.ia.update(deltaTime)
        self.looseTimer.update(deltaTime)
        qteUpdate(self.map.qte,deltaTime)

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
        qteDraw(self.map.qte,self.map.ia)
        self.map.ia.draw()
        self.looseTimer.draw()

        # Compute the mean anger level of all people
        if self.people:  # Ensure there are people to avoid division by zero
            mean_anger = 0
            anger_count = 0
            for p in self.people:
                if p.type == "human":
                    mean_anger = p.anger_level
                    anger_count += 1
            if(anger_count != 0):
                mean_anger = mean_anger / anger_count
                if(mean_anger ==0):
                    print("human win")
                    self.looseTimer.end()
                    self.process.selectPage(4, "human")
            drawAngerBar(self.W, self.H,mean_anger/100)  # Use the mean anger to draw the anger bar
        else:
            drawAngerBar(self.W, self.H,0)  # If there are no people, draw an empty anger bar

    def onKeyEvent(self, key, isPressed):
        if self.looseTimer.isOver():
            return
        p = self.__find_player(Constants.KEYBOARD_CTRL)
        if p is not None:
            if key == arcade.key.A:
                p.set_anim1()
            elif key == arcade.key.Z:
                p.set_anim2()
            elif key == arcade.key.E:
                p.set_anim3()
            if key == arcade.key.LEFT:
                p.move_left(isPressed)
            elif key == arcade.key.RIGHT:
                p.move_right(isPressed)
            elif not isPressed and key == arcade.key.SPACE:
                #other interactive
                if not processStairsAction(self.map.stairs, p):
                    notifyQTEInteraction(self.map.qte,self.people, p,self.map.ia)


    def onButtonEvent(self, gamepadNum, buttonName, isPressed):
        if self.looseTimer.isOver():
            return
        p = self.__find_player(gamepadNum)
        if p is not None:

            if buttonName == "B":
                p.set_anim1()
            elif buttonName == "X":
                p.set_anim2()
            elif buttonName == "Y":
                p.set_anim3()
            elif not isPressed:
                #other interactive
                if not processStairsAction(self.map.stairs, p):
                    notifyQTEInteraction(self.map.qte,self.people, p, None)
                    #notifyQTEInteraction(self.map.qte,self.people, p,self.map.ia)

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
        pass
        # p = self.__find_player(Constants.MOUSE_CTRL)
        # if p is not None:
        #     print(p)

    def onMouseButtonEvent(self, x, y, buttonNum, isPressed):
        if Constants.DEBUG and isPressed:
            xp = x / self.W
            yp = y / self.H
            print(f"x={x} ({xp}%) y={y} ({yp}%)")

