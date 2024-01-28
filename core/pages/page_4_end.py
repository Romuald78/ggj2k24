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
        self.gfx = None

    def refresh(self, args=None):
        self.window.set_viewport(0, self.W, 0, self.H)
        params = {
            "filePath" : "resources/backgrounds/fond maison.png",
            "size" : (self.W, self.H),
            "filterColor": (255,255,255,128),
            "position" : (self.W/2, self.H/2)
        }
        self.gfx =Gfx.create_fixed(params)
        self.gfxs = []


        if True: # args is not None:
            # string value
            if True : #args == "human":
                # HUMAN VICTORY

                # tv
                params = {
                    "filePath": "resources/items/atlas tele.png",
                    "position": (self.W/2, self.H/2),
                    "spriteBox": (5, 1, 234, 251),
                    "size" : (self.W/2.5, self.H/2.5),
                    "startIndex": 0,
                    "endIndex": 3,
                    "frameDuration": 0.1,
                    "flipH": True
                }
                tv = Gfx.create_animated(params)
                self.gfxs.append(tv)
                # human
                params = {
                    "filePath": "resources/characters/atlas telecommande.png",
                    "position": (4*self.W/7, self.H/2),
                    "spriteBox": (4, 1, 113, 300),
                    "size" : (self.W/2, self.H/2),
                    "startIndex": 0,
                    "endIndex": 3,
                    "frameDuration": 0.25,
                    "flipH": True
                }
                hum = Gfx.create_animated(params)
                self.gfxs.append(hum)
                # fauteuil
                params = {
                    "filePath": "resources/items/fauteuil.png",
                    "position": (self.W/3, self.H/3),
                    "spriteBox": (1, 1, 128, 123),
                    "size" : (self.W/3, self.H/3),
                    "startIndex": 0,
                    "endIndex": 0,
                    "frameDuration": 0.25,
                    "flipH": False
                }
                fau = Gfx.create_animated(params)
                self.gfxs.append(fau)

                params = {
                    "filePath": f"resources/characters/atlas cat vomit.png",
                    "position": (self.W/2, self.H/5),
                    "size": (self.W/4, self.H/4),
                    "spriteBox": (16, 1, 164, 200),
                    "startIndex": 5,
                    "endIndex": 5,
                    "frameDuration": 0.11
                }
                chat1 = Gfx.create_animated(params)
                self.gfxs.append(chat1)

                params = {
                    "filePath": f"resources/characters/atlas cat eat white.png",
                    "position": (self.W/1.5, self.H/6.5),
                    "size": (self.W/8, self.H/8),
                    "spriteBox": (10, 1, 145, 100),
                    "startIndex": 2,
                    "endIndex": 2,
                    "frameDuration": 0.11
                }
                chat2 = Gfx.create_animated(params)
                chat2.angle = 200
                self.gfxs.append(chat2)

                params = {
                    "filePath": f"resources/characters/atlas chat idle orange.png",
                    "position": (self.W/3.5, self.H/2),
                    "size": (self.W/8, self.H/8),
                    "spriteBox": (4, 1, 147, 90),
                    "startIndex": 1,
                    "endIndex": 1,
                    "frameDuration": 0.11
                }
                chat3 = Gfx.create_animated(params)
                self.gfxs.append(chat3)


            else:
                # CAT VICTORY
                pass



    def setup(self):
        self.refresh()

    def on_update(self, deltaTime):
        for g in self.gfxs:
            g.update_animation(deltaTime)

    def draw(self):
        self.gfx.draw()
        for g in self.gfxs:
            g.draw()

    def onKeyEvent(self, key, isPressed):
        if isPressed and key == arcade.key.SPACE:
            self.__go_to_splash()

    def onButtonEvent(self, gamepadNum, buttonName, isPressed):
        if isPressed:
            self.__go_to_splash()

    def onAxisEvent(self, gamepadNum, axisName, analogValue):
        pass

    def onMouseMotionEvent(self, x, y, dx, dy):
        pass

    def onMouseButtonEvent(self, x, y, buttonNum, isPressed):
        pass
        # if isPressed:
        #     self.__go_to_select(Constants.MOUSE_CTRL)


