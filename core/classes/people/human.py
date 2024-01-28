import random

from core.classes.constants import Constants
from core.classes.people.People import Person
from core.utils.utils import Gfx


class Human(Person):

    def set_anim1(self):
        self.sweeping = False
        self.washing  = False

    def set_anim2(self):
        self.sweeping = True
        self.washing  = False

    def set_anim3(self):
        self.sweeping = False
        self.washing  = True

    def __init__(self, ctrl, x0=0, y0=0, ratio=1.0):
        super().__init__(ctrl, Constants.HUMAN_SPEED, x0, y0,type="human")

        self.sweeping = False
        self.washing  = False

        self.anger_level = 50 #start at 50% anger
        self.anger_time  = 0
        params = {
            "filePath": "resources/characters/vieux idle atlas.png",
            "position": (x0, y0),
            "spriteBox": (4, 1, 100, 150),
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
            "filePath": "resources/characters/atlas walk idle vieux.png",
            "position": (x0, y0),
            "spriteBox": (6, 1, 119, 171),
            "startIndex": 0,
            "endIndex": 5,
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
            "filePath": f"resources/characters/atlas vieux balai.png",
            "position": (x0, y0),
            "spriteBox": (4, 1, 154, 197),
            "startIndex": 0,
            "endIndex": 3,
            "frameDuration":0.2
        }
        self.gfxBalaiR = Gfx.create_animated(params)
        params['flipH'] = True
        self.gfxBalaiL = Gfx.create_animated(params)
        self.gfxBalaiR.scale = ratio * 0.85
        self.gfxBalaiL.scale = ratio * 0.85
        self.gfxBalaiR.center_y += self.gfxBalaiR.height / 2.2
        self.gfxBalaiL.center_y += self.gfxBalaiL.height / 2.2

        params = {
            "filePath": f"resources/characters/atlas vieux vaisselle.png",
            "position": (x0, y0),
            "spriteBox": (4, 1, 135, 150),
            "startIndex": 0,
            "endIndex": 3,
            "frameDuration":0.2
        }
        self.gfxDishL = Gfx.create_animated(params)
        params['flipH'] = True
        self.gfxDishR = Gfx.create_animated(params)
        self.gfxDishR.scale = ratio
        self.gfxDishL.scale = ratio
        self.gfxDishR.center_y += self.gfxDishR.height / 2
        self.gfxDishL.center_y += self.gfxDishL.height / 2


    def update(self, deltaTime):
        super().update(deltaTime)
        self.color = (255, 255, 255)
        if self.anger_time > 0:
            self.anger_time -= deltaTime
            gb = random.randint(78, 128)
            r  = random.randint(205, 255)
            self.color = (255, gb, gb)

        if self.anger_level >= Constants.MAX_ANGER:
            self.anger_time = Constants.ANGER_MAX_TIME
            self.anger_level = 0

        self.gfxBalaiL.update_animation(deltaTime)
        self.gfxBalaiR.update_animation(deltaTime)
        self.gfxBalaiL.center_x = self.x
        self.gfxBalaiR.center_x = self.x
        self.gfxBalaiL.center_y = self.y
        self.gfxBalaiR.center_y = self.y
        self.gfxDishL.update_animation(deltaTime)
        self.gfxDishR.update_animation(deltaTime)
        self.gfxDishL.center_x = self.x
        self.gfxDishR.center_x = self.x
        self.gfxDishL.center_y = self.y
        self.gfxDishR.center_y = self.y


    def draw(self):
        # Draw specific parts
        if self.sweeping:
            if self._lastdir_left:
                self.gfxBalaiL.draw()
            else:
                self.gfxBalaiR.draw()
        elif self.washing:
            if self._lastdir_left:
                self.gfxDishL.draw()
            else:
                self.gfxDishR.draw()

        else:
            # draw common part (+debug)
            super().draw()


    def is_angry(self):
        return self.anger_time > 0



    @property
    def anger(self):
        if self.anger_time > 0:
            return 100
        else:
            return min(self.anger_level, 100)

    @anger.setter
    def anger(self, newValue):
        self.anger_level = newValue

