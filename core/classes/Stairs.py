import arcade
class Stairs:

    def __init__(self, x0, y0, w0, h0,id,dest_id):
        self.x = x0
        self.y = y0
        self.w = w0
        self.h = h0
        self.id = id
        self.dest_x = -1
        self.dest_y = -1
        self.dest_id = dest_id
        print("stairs " + str(self.x) + " " + str(self.y) + " " + str(self.w) + " " + str(self.h) + " " + str(self.id) + " " + str(self.dest_id))

    @property
    def left(self):
        return self.x - self.w / 2

    @property
    def right(self):
        return self.x + self.w / 2

    @property
    def top(self):
        return self.y + self.h / 2

    @property
    def bottom(self):
        return self.y - self.h / 2

    def debug_draw(self):
        arcade.draw_rectangle_outline(
            self.x, self.y, self.w, self.h,
            (128, 0, 0, 128), 5 )