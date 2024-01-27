import arcade


class Person:

    def __init__(self, ctrl, speed=10, x0=0, y0=0):
        self.__ctrl = ctrl
        self.__moveable = True
        self.__speed = speed
        self.__x = x0
        self.__y = y0
        self.__move_left  = False
        self.__move_right = False

    def freeze(self):
        self.__moveable = False

    def free(self):
        self.__moveable = True

    def move_left(self, move):
        self.__move_left = move

    def move_right(self, move):
        self.__move_right = move

    def update(self, deltaTime):
        if self.__move_left:
            self.__x -= self.__speed * deltaTime
        if self.__move_right:
            self.__x += self.__speed * deltaTime

    def draw(self):
        arcade.draw_rectangle_outline(
            self.__x, self.__y, 200, 200, (0, 0, 0), 5
        )


# class Human(Person):
#
#     def __init__(self, ctrl):
#         super().__init__(ctrl)
#
#
# class Cat(Person):
#
#     def __init__(self, ctrl):
#         super().__init__(ctrl)
#
