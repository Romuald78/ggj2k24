import arcade

from core.classes.constants import Constants
from core.utils.utils import Gfx


class Person:

    def __init__(self, ctrl, speed=1000, x0=0, y0=0, width=200, height=200,type="none"):
        self._ctrl = ctrl
        self._moveable = True
        self._speed = speed
        self._x = x0
        self._y = y0
        self._w = width
        self._h = height
        self._move_left  = False
        self._move_right = False
        self._lastdir_left = False

        self._idle_L = None
        self._idle_R = None
        self._move_L = None
        self._move_R = None
        self.type = type

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def left(self):
        return self._x - self._w / 2

    @property
    def right(self):
        return self._x + self._w / 2

    @property
    def top(self):
        return self._y + self._h / 2

    @property
    def bottom(self):
        return self._y - self._h / 2

    @property
    def ctrl(self):
        return self._ctrl

    @property
    def width(self):
        return self._idle_L.width

    def freeze(self):
        self._moveable = False

    def free(self):
        self._moveable = True

    def shift(self, dx, dy):
        self._x += dx
        self._y += dy

    def stop(self):
        self._move_left  = False
        self._move_right = False

    def move_left(self, move):
        self._move_left = move
        if move:
            self._lastdir_left = True

    def move_right(self, move):
        self._move_right = move
        if move:
            self._lastdir_left = False

    def update(self, deltaTime):
        self._idle_L.update_animation(deltaTime)
        self._idle_R.update_animation(deltaTime)
        self._move_L.update_animation(deltaTime)
        self._move_R.update_animation(deltaTime)

        if not self._moveable:
            return

        if self._move_left:
            self._x -= self._speed * deltaTime
        if self._move_right:
            self._x += self._speed * deltaTime

    # y est le pied du personnage (au dol)
    def tp(self, x, y):
        self._x = x
        self._y = y + self._h / 2

    def draw(self):
        # update gfx position according to model position
        self._idle_L.center_x, self._idle_L.center_y = self._x, self._y
        self._idle_R.center_x, self._idle_R.center_y = self._x, self._y
        self._move_L.center_x, self._move_L.center_y = self._x, self._y
        self._move_R.center_x, self._move_R.center_y = self._x, self._y

        if Constants.DEBUG:
            arcade.draw_rectangle_outline(
                (self.left + self.right) / 2,
                (self.top + self.bottom) / 2,
                self.width * (1 - Constants.ITEM_HITBOX_COEF),
                self.top-self.bottom, (0,0,255,128), 2

            )
        # STATIC DISPLAY
        if self._move_left == self._move_right:
            if self._lastdir_left:
                if self._idle_L is not None:
                    self._idle_L.draw()
            else:
                if self._idle_R is not None:
                    self._idle_R.draw()
        # MOVE LEFT DISPLAY
        elif self._move_left:
            if self._move_L is not None:
                self._move_L.draw()
        # MOVE RIGHT DISPLAY
        else:
            if self._move_R is not None:
                self._move_R.draw()


class Human(Person):

    def __init__(self, ctrl, x0=0, y0=0, ratio=1.0):
        super().__init__(ctrl, Constants.HUMAN_SPEED, x0, y0,type="human")
        params = {
            "filePath": "resources/characters/vieux idle atlas.png",
            "position": (x0, y0),
            "spriteBox": (4, 1, 100, 150),
            "startIndex": 0,
            "endIndex": 3,
            "frameDuration":0.2
        }
        self._idle_R = Gfx.create_animated(params)
        params['flipH'] = True
        self._idle_L = Gfx.create_animated(params)
        self._idle_L.scale = ratio
        self._idle_R.scale = ratio
        self.shift(0, self._idle_R.height / 2)

        # animations
        params = {
            "filePath": "resources/characters/atlas walk idle vieux.png",
            "position": (x0, y0),
            "spriteBox": (6, 1, 119, 171),
            "startIndex": 0,
            "endIndex": 5,
            "frameDuration":0.1
        }
        self._move_R = Gfx.create_animated(params)
        params['flipH'] = True
        self._move_L = Gfx.create_animated(params)
        self._move_L.scale = ratio
        self._move_R.scale = ratio

        # update _w _h
        self._w = self._idle_L.width
        self._h = self._idle_L.height


class Cat(Person):

    def __init__(self, ctrl, x0=0, y0=0, ratio=1.0):
        super().__init__(ctrl, Constants.CAT_SPEED, x0, y0,type="cat")
        params = {
            "filePath": "resources/characters/atlas chat idle.png",
            "position": (x0, y0),
            "spriteBox": (4, 1, 147, 90),
            "startIndex": 0,
            "endIndex": 3,
            "frameDuration":0.2
        }
        self._idle_R = Gfx.create_animated(params)
        params['flipH'] = True
        self._idle_L = Gfx.create_animated(params)
        self._idle_L.scale = ratio
        self._idle_R.scale = ratio
        self.shift(0, self._idle_R.height / 2)

        # animations
        params = {
            "filePath": "resources/characters/atlas chat walk idle.png",
            "position": (x0, y0),
            "spriteBox": (4, 1, 166, 94),
            "startIndex": 0,
            "endIndex": 3,
            "frameDuration":0.1
        }

        self._move_R = Gfx.create_animated(params)
        params['flipH'] = True
        self._move_L = Gfx.create_animated(params)
        self._move_L.scale = ratio
        self._move_R.scale = ratio

        # update _w _h
        self._w = self._idle_L.width
        self._h = self._idle_L.height

    def draw(self):
        # Draw specific parts

        # draw common part (+debug)
        super().draw()
