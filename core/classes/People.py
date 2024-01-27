import arcade

from core.classes.constants import Constants
from core.utils.utils import Gfx


class Person:

    def __init__(self, ctrl, speed=10, x0=0, y0=0):
        self._ctrl = ctrl
        self._moveable = True
        self._speed = speed
        self._x = x0
        self._y = y0
        self._move_left  = False
        self._move_right = False
        self._lastdir_left = False

        self._idle_L = None
        self._idle_R = None

    def freeze(self):
        self._moveable = False

    def free(self):
        self._moveable = True

    def move_left(self, move):
        self._move_left = move
        if not move:
            self._lastdir_left = True

    def move_right(self, move):
        self._move_right = move
        if not move:
            self._lastdir_left = False

    def update(self, deltaTime):
        if self._move_left:
            self._x -= self._speed * deltaTime
        if self._move_right:
            self._x += self._speed * deltaTime

    def draw(self):
        if Constants.DEBUG:
            arcade.draw_rectangle_outline(
                self._x, self._y+100, 200, 200, (0, 0, 0), 5
            )
        if self._move_left == self._move_right:
            if self._lastdir_left:
                if self._idle_L is not None:
                    self._idle_L.draw()
            else:
                if self._idle_R is not None:
                    self._idle_R.draw()


class Human(Person):

    def __init__(self, ctrl, speed=10, x0=0, y0=0):
        super().__init__(ctrl, speed, x0, y0)
        params = {
            "filePath": "resources/characters/player.png",
            "size": (250, 250),
            "position": (x0, y0),
            "spriteBox": (7, 1, 170, 250),
            "startIndex": 0,
            "endIndex": 0,
        }
        self._idle_R = Gfx.create_animated(params)
        self._idle_R.center_y += self._idle_R.height / 2
        params['flipH'] = True
        self._idle_L = Gfx.create_animated(params)
        self._idle_L.center_y += self._idle_L.height / 2


class Cat(Person):

    def __init__(self, ctrl, speed=10, x0=0, y0=0):
        super().__init__(ctrl, speed, x0, y0)

    def draw(self):
        # Draw specific parts

        # draw common part (+debug)
        super().draw()
