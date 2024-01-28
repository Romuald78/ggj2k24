from core.classes.constants import Constants
from core.classes.people.People import Person
from core.utils.utils import Gfx


class Cat(Person):

    def set_anim1(self):
        self._eating = False
        self._purging = False

    def set_anim2(self):
        self._eating = True
        self._purging = False

    def set_anim3(self):
        self._eating  = False
        self._purging = True

    def __init__(self, ctrl, x0=0, y0=0, ratio=1.0, clr=''):
        super().__init__(ctrl, Constants.CAT_SPEED, x0, y0,type="cat")

        self._eating  = False
        self._purging = False
        self._started = False

        params = {
            "filePath": f"resources/characters/atlas chat idle{clr}.png",
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
            "filePath": f"resources/characters/atlas chat walk idle{clr}.png",
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

        # Specific anims (purge and eat)
        params = {
            "filePath": f"resources/characters/atlas cat eat{clr}.png",
            "position": (x0, y0),
            "spriteBox": (10, 1, 146, 100),
            "startIndex": 0,
            "endIndex": 8,
            "frameDuration":0.1
        }
        self._eatgfx_R = Gfx.create_animated(params)
        params['flipH'] = True
        self._eatgfx_L = Gfx.create_animated(params)
        self._eatgfx_L.scale = ratio
        self._eatgfx_R.scale = ratio
        self._eatgfx_L.center_y += self._eatgfx_L.height/2
        self._eatgfx_R.center_y += self._eatgfx_R.height/2

        params = {
            "filePath": f"resources/characters/atlas cat vomit{clr}.png",
            "position": (x0, y0),
            "spriteBox": (16, 1, 164, 200),
            "startIndex": 0,
            "endIndex": 15,
            "frameDuration":0.11
        }
        self._purgegfx_R = Gfx.create_animated(params)
        params['flipH'] = True
        self._purgegfx_L = Gfx.create_animated(params)
        self._purgegfx_L.scale = ratio
        self._purgegfx_R.scale = ratio
        self._purgegfx_L.center_y += self._purgegfx_L.height/2
        self._purgegfx_R.center_y += self._purgegfx_R.height/2


    def update(self, deltaTime):
        super().update(deltaTime)

        if self._purging:
            offset = self._idle_L.height * 0.18
            if self._lastdir_left:
                self._purgegfx_L.update_animation(deltaTime)
                self._purgegfx_L.center_x = self._x
                self._purgegfx_L.center_y = self._y + offset
                if self._purgegfx_L.cur_frame_idx >= len(self._purgegfx_L.frames) - 1:
                    self.set_anim1()
            else:
                self._purgegfx_R.update_animation(deltaTime)
                self._purgegfx_R.center_x = self._x
                self._purgegfx_R.center_y = self._y + offset
                if self._purgegfx_R.cur_frame_idx >= len(self._purgegfx_R.frames) - 1:
                    self.set_anim1()

        if self._eating:
            if self._lastdir_left:
                self._eatgfx_L.update_animation(deltaTime)
                self._eatgfx_L.center_x = self._x
                self._eatgfx_L.center_y = self._y
            else:
                self._eatgfx_R.update_animation(deltaTime)
                self._eatgfx_R.center_x = self._x
                self._eatgfx_R.center_y = self._y


    def draw(self):
        # Draw specific parts
        if self._eating:
            if self._lastdir_left:
                self._eatgfx_L.draw()
            else:
                self._eatgfx_R.draw()
        elif self._purging:
            if self._lastdir_left:
                self._purgegfx_L.draw()
            else:
                self._purgegfx_R.draw()

        else:
            # draw common part (+debug)
            super().draw()

