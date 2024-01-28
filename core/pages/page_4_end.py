import arcade

from core.classes.constants import Constants
from core.utils.utils import Gfx


class Page4End:

    def __go_to_splash(self):
        self.process.selectPage(1)

    def __init__(self, w, h, window: arcade.Window, process=None):
        super().__init__()
        self.window = window
        self.W = w
        self.H = h
        self.process = process
        # fields
        self.gfxs   = None
        self.addgfx = None

    def refresh(self, args=None):
        self.window.set_viewport(0, self.W, 0, self.H)
        params = {
            "filePath" : "resources/backgrounds/fond maison.png",
            "size" : (self.W, self.H),
            "filterColor": (255,255,255,128),
            "position" : (self.W/2, self.H/2)
        }
        gfx =Gfx.create_fixed(params)
        self.gfxs = [gfx, ]


        if args is not None:

            # string value
            if args == "human":
                # HUMAN VICTORY
                params = {
                    "filePath": "resources/backgrounds/victory human.png",
                    "size": (self.W*0.75, self.H*0.75),
                    "position": (self.W / 2, self.H / 2)
                }
                gfx = Gfx.create_fixed(params)
                self.gfxs.append(gfx)
                params = {
                    "filePath": "resources/characters/vieux idle atlas.png",
                    "position": (self.W/5, self.H/3),
                    "size": (self.W/3, self.H/3),
                    "spriteBox": (4, 1, 100, 150),
                    "startIndex": 0,
                    "endIndex": 3,
                    "frameDuration": 0.2
                }
                self.addgfx = Gfx.create_animated(params)

            else:
                # CAT VICTORY
                params = {
                    "filePath": "resources/backgrounds/victory kitty.png",
                    "size": (self.W*0.75, self.H*0.75),
                    "position": (self.W / 2, self.H / 2)
                }
                gfx = Gfx.create_fixed(params)
                self.gfxs.append(gfx)
                params = {
                    "filePath": "resources/characters/atlas chat idle orange.png",
                    "position": (self.W/5, self.H/3),
                    "size": (self.W/4, self.H/4),
                    "spriteBox": (4, 1, 147, 90),
                    "startIndex": 0,
                    "endIndex": 3,
                    "frameDuration": 0.2
                }
                self.addgfx = Gfx.create_animated(params)


    def setup(self):
        self.refresh()

    def on_update(self, deltaTime):
        self.addgfx.update_animation(deltaTime)

    def draw(self):
        for g in self.gfxs:
            g.draw()
        self.addgfx.draw()

    def onKeyEvent(self, key, isPressed):
        if (not isPressed) and key == arcade.key.SPACE:
            self.__go_to_splash()

    def onButtonEvent(self, gamepadNum, buttonName, isPressed):
        if not isPressed:
            self.__go_to_splash()

    def onAxisEvent(self, gamepadNum, axisName, analogValue):
        pass

    def onMouseMotionEvent(self, x, y, dx, dy):
        pass

    def onMouseButtonEvent(self, x, y, buttonNum, isPressed):
        pass
        # if isPressed:
        #     self.__go_to_select(Constants.MOUSE_CTRL)


