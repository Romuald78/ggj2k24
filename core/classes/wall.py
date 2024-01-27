import random

import arcade


class Wall:

    def __init__(self, x0, y0, w0, h0):
        self.x = x0
        self.y = y0
        self.w = w0
        self.h = h0

    def debug_draw(self):
        arcade.draw_rectangle_outline(
            self.x, self.y, self.w, self.h,
            (0, 0, 0, 128), 5 )
