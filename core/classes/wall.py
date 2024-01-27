import random

import arcade


class Wall:

    def __init__(self, x0, y0, w0, h0):
        self._x = x0
        self._y = y0
        self._w = w0
        self._h = h0

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


    def debug_draw(self):
        arcade.draw_rectangle_outline(
            self._x, self._y, self._w, self._h,
            (0, 0, 0, 128), 5 )
