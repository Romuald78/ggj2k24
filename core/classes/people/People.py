import arcade

from core.classes.constants import Constants


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

        self.color = (255,255,255)

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
        ref = None
        if self._move_left == self._move_right:
            if self._lastdir_left:
                if self._idle_L is not None:
                    ref = self._idle_L
            else:
                if self._idle_R is not None:
                    ref = self._idle_R
        # MOVE LEFT DISPLAY
        elif self._move_left:
            if self._move_L is not None:
                ref = self._move_L
        # MOVE RIGHT DISPLAY
        else:
            if self._move_R is not None:
                ref = self._move_R
        if ref is not None:
            ref.color = self.color
            ref.draw()


