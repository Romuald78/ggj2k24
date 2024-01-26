import arcade

from core.classes.constants import Constants
from core.utils.utils import Gfx


class Page2Select:

    def __back_to_splash(self):
        self.process.selectPage(1)

    def __add_player(self, ctrl):
        if not ctrl in self.ctrls:
            self.ctrls[ctrl] = {} # TODO init player data

    def __remove_player(self, ctrl):
        if ctrl in self.ctrls:
            del self.ctrls[ctrl]
            if len(self.ctrls) == 0:
                self.__back_to_splash()

    def __change_player_left(self, ctrl):
        if ctrl in self.ctrls:
            self.ctrls[ctrl] = {} # TODO update player data

    def __change_player_right(self, ctrl):
        if ctrl in self.ctrls:
            self.ctrls[ctrl] = {} # TODO update player data

    def __init__(self, w, h, window: arcade.Window, process=None):
        super().__init__()
        self.window = window
        self.W = w
        self.H = h
        self.process = process
        # fields
        self.ctrls = None
        self.gfx = None

    def refresh(self, args=None):
        self.window.set_viewport(0, self.W, 0, self.H)
        self.ctrls = {}
        params = {
            "filePath" : "resources/backgrounds/select_back.png",
            "size" : (self.W, self.H),
            "position" : (self.W/2, self.H/2)
        }
        self.gfx =Gfx.create_fixed(params)
        # Select first player (use given controller number)
        if args is not None:
            self.__add_player(args['ctrl'])

    def setup(self):
        self.refresh()

    def on_update(self, deltaTime):
        # print("------------------------")
        # for ctrl in self.ctrls:
        #     print(ctrl)
        pass

    def draw(self):
        self.gfx.draw()

    def onKeyEvent(self, key, isPressed):
        if isPressed:
            if key == arcade.key.SPACE:
                self.__add_player(Constants.KEYBOARD_CTRL)
            elif key == arcade.key.DELETE or key == arcade.key.BACKSPACE:
                self.__remove_player(Constants.KEYBOARD_CTRL)
            elif key == arcade.key.LEFT or key == arcade.key.Q:
                self.__change_player_left(Constants.KEYBOARD_CTRL)
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.__change_player_right(Constants.KEYBOARD_CTRL)

    def onButtonEvent(self, gamepadNum, buttonName, isPressed):
        if isPressed:
            if buttonName == "A":
                self.__add_player(gamepadNum)
            elif buttonName == "B":
                self.__remove_player(gamepadNum)

    def onAxisEvent(self, gamepadNum, axisName, analogValue):
        if axisName == "X":
            if analogValue <= -0.5:
                self.__change_player_left(gamepadNum)
            elif analogValue >= 0.5
                self.__change_player_right(gamepadNum)

    def onMouseMotionEvent(self, x, y, dx, dy):
        pass

    def onMouseButtonEvent(self, x, y, buttonNum, isPressed):
        if isPressed:
            if buttonNum == 1:
                self.__add_player(Constants.MOUSE_CTRL)
            else:
                self.__remove_player(Constants.MOUSE_CTRL)
