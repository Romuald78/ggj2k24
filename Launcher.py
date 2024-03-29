# ====================================================================================================
# IMPORTS
# ====================================================================================================
import sys

import arcade
import pyglet

from core.Process import Process
import os

pyglet.options["xinput_controllers"] = False

# ====================================================================================================
# CONSTANTS
# ====================================================================================================
TITLE = "Global Game Jam 2024"

# https://api.arcade.academy/en/latest/tutorials/bundling_with_pyinstaller/index.html
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)


# ====================================================================================================
# GAME CLASS
# ====================================================================================================
class MyGame(arcade.Window):
    BUTTON_NAMES = ["A",
                    "B",
                    "X",
                    "Y",
                    "LB",
                    "RB",
                    "VIEW",
                    "MENU",
                    "LSTICK",
                    "RSTICK",
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    ]

    # ----------------------------------
    # PRIVATE METHODS FOR INPUT MANAGEMENT
    # ----------------------------------
    def __onButtonPressed(self, _gamepad, button):
        idx = self.gamepadsLegacy[_gamepad]
        if type(button) == "string":
            self.onButtonPressed(idx, button)
        else:
            self.onButtonPressed(idx, MyGame.BUTTON_NAMES[button])

    def __onButtonReleased(self, _gamepad, button):
        idx = self.gamepadsLegacy[_gamepad]
        if type(button) == "string":
            self.onButtonReleased(idx, button)
        else:
            self.onButtonReleased(idx, MyGame.BUTTON_NAMES[button])

    def __onCrossMove(self, _gamepad, x, y):
        idx = self.gamepadsLegacy[_gamepad]
        self.onCrossMove(idx, x, -y)

    def __onAxisMove(self, _gamepad, axis, value):
        idx = self.gamepadsLegacy[_gamepad]
        self.onAxisMove(idx, axis, value)

    # ----------------------------------
    # PRIVATE METHODS FOR SCREEN COORDS
    # ----------------------------------
    def __convert_xy(self, x, y):
        winW, winH = self.get_size()
        x0, x1, y0, y1 = self.get_viewport()
        x = x0 + x * (x1 - x0) / winW
        y = y0 + y * (y1 - y0) / winH
        return x, y

    def __toggle_full_screen(self):
        # toggle screen mode (process ratio must be compliant with screen resolution
        self.set_fullscreen(not self.fullscreen)
        if self.fullscreen:
            winW, winH = self.get_size()
            ratioX = self.process.SCREEN_WIDTH / winW
            ratioY = self.process.SCREEN_HEIGHT / winH
            ratio = max(ratioX, ratioY)
            finalW = int(round(ratio * winW, 0))
            finalH = int(round(ratio * winH, 0))
            x0 = -int((finalW - self.process.SCREEN_WIDTH) / 2)
            y0 = -int((finalH - self.process.SCREEN_HEIGHT) / 2)
            self.set_viewport(x0, finalW + x0, y0, finalH + y0)
        else:
            self.set_viewport(0, self.process.SCREEN_WIDTH, 0, self.process.SCREEN_HEIGHT)

    def on_stick_motion(self,controller, name, x_value, y_value):
        if name == "leftstick":
            self.process.onAxisEvent(controller.name, "X", x_value)
            self.process.onAxisEvent(controller.name, "Y", -y_value)

        if name == "rightstick":
            self.process.onAxisEvent(controller.name, "RX", x_value)
            self.process.onAxisEvent(controller.name, "RY", -y_value)

    def on_button_press(self,controller, button_name):
        self.process.onButtonEvent(controller.name,button_name,True)

    def on_button_release(self, controller, button_name):
        self.process.onButtonEvent(controller.name,button_name,False)

    # ----------------------------------
    # CONSTRUCTOR
    # ----------------------------------
    def __init__(self, width, height, ratio, title):
        # init application window
        super().__init__(int(width*ratio), int(height*ratio), title)
        # init process object
        self.process = Process(width, height, ratio, self)
        # set application window background color
        arcade.set_background_color(arcade.color.BLACK)
        if pyglet.compat_platform in ('cygwin', 'win32'):
            # Store gamepad list
            self.gamepads = pyglet.input.get_controllers()
            print(self.gamepads)
            # check every connected gamepad
            if self.gamepads:
                for g in self.gamepads:
                    # link all gamepad callbacks to the current class methods
                    g.open()
                    g.on_button_release = self.on_button_release
                    g.on_button_press = self.on_button_press
                    g.on_stick_motion = self.on_stick_motion
                    # transform list into a dictionary to get its index faster
            else:
                print("There are no Gamepad connected !")
                self.gamepads = None
        else:
            # Store gamepad list
            self.gamepads = arcade.get_joysticks()
            # check every connected gamepad
            if self.gamepads:
                for g in self.gamepads:
                    # link all gamepad callbacks to the current class methods
                    g.open()
                    g.on_joybutton_press = self.__onButtonPressed
                    g.on_joybutton_release = self.__onButtonReleased
                    g.on_joyhat_motion = self.__onCrossMove
                    g.on_joyaxis_motion = self.__onAxisMove
                    # transform list into a dictionary to get its index faster
                self.gamepadsLegacy = {self.gamepads[idx]: idx for idx in range(len(self.gamepads))}
            else:
                print("There are no Gamepad connected !")
                self.gamepads = None
        # full screen config
        self.appW = None
        self.appH = None

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #                                SETUP your game here
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def setup(self):
        self.process.setup()

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #                               DRAW your game elements here
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_draw(self):
        # - - - - - - - - - - - - - - - - - - - - - - - - -#
        arcade.start_render()
        self.process.draw()
        # - - - - - - - - - - - - - - - - - - - - - - - - -#

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #                                  UPDATE your game model here
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_update(self, delta_time):
        try:
            self.process.on_update(delta_time)
        except Exception as ex:
            print(f"[ERROR] update : {ex}")


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # KEY PRESSED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_key_press(self, key, modifiers):
        try:
            # Close application if ESCAPE key is hit
            if key == arcade.key.ESCAPE:
                self.close()
            # Toggle full screen mode with F11
            elif key == arcade.key.F11:
                self.__toggle_full_screen()
            else:
                self.process.onKeyEvent(key, True)
        except Exception as ex:
            print(f"[ERROR] key press : {ex}")

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # KEY RELEASED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_key_release(self, key, modifiers):
        try:
            self.process.onKeyEvent(key, False)
        except Exception as ex:
            print(f"[ERROR] key release : {ex}")

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # GAMEPAD BUTTON PRESSED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def onButtonPressed(self, gamepadNum, buttonNum):
        try:
            self.process.onButtonEvent(gamepadNum, buttonNum, True)
        except Exception as ex:
            print(f"[ERROR] button press : {ex}")

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # GAMEPAD BUTTON RELEASED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def onButtonReleased(self, gamepadNum, buttonNum):
        try:
            self.process.onButtonEvent(gamepadNum, buttonNum, False)
        except Exception as ex:
            print(f"[ERROR] button release : {ex}")

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # GAMEPAD CROSSPAD events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def onCrossMove(self, gamepadNum, xValue, yValue):
        try:
            self.process.onAxisEvent(gamepadNum, "x", xValue)
            self.process.onAxisEvent(gamepadNum, "y", yValue)
        except Exception as ex:
            print(f"[ERROR] cross move : {ex}")

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # GAMEPAD AXIS events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def onAxisMove(self, gamepadNum, axisName, analogValue):
        try:
            if axisName == "z":
                analogValue = -analogValue
            self.process.onAxisEvent(gamepadNum, axisName.upper(), analogValue)
        except Exception as ex:
            print(f"[ERROR] axis move : {ex}")

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # MOUSE MOTION events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_mouse_motion(self, x, y, dx, dy):
        try:
            x, y = self.__convert_xy(x, y)
            self.process.onMouseMotionEvent(x, y, dx, dy)
        except Exception as ex:
            print(f"[ERROR] mouse motion : {ex}")

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # MOUSE BUTTON PRESSED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_mouse_press(self, x, y, button, modifiers):
        try:
            x, y = self.__convert_xy(x, y)
            self.process.onMouseButtonEvent(x, y, button, True)
        except Exception as ex:
            print(f"[ERROR] mouse press : {ex}")

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # MOUSE BUTTON RELEASED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_mouse_release(self, x, y, button, modifiers):
        try:
            x, y = self.__convert_xy(x, y)
            self.process.onMouseButtonEvent(x, y, button, False)
        except Exception as ex:
            print(f"[ERROR] mouse release : {ex}")


# ====================================================================================================
# MAIN PROCESS
# ====================================================================================================
def main():
    # add current file path
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')
    os.chdir(file_path)

    coef = 1.0
    full = True
    if "-window" in sys.argv:
        coef = 0.5
        full = False
    game = MyGame(int(1920 * coef), int(1080 * coef), 1.0, TITLE)
    game.set_fullscreen(full)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
