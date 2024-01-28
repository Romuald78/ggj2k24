import random

from core.classes.constants import Constants
from core.classes.people.People import Person
from core.utils.utils import Gfx


class Human(Person):

    def __init__(self, ctrl, x0=0, y0=0, ratio=1.0):
        super().__init__(ctrl, Constants.HUMAN_SPEED, x0, y0,type="human")
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

    def update(self, deltaTime):
        super().update(deltaTime)
        self.color = (255, 255, 255)
        if self.anger_time > 0:
            self.anger_time -= deltaTime
            gb = random.randint(78, 128)
            r  = random.randint(205, 255)
            self.color = (255, gb, gb)

        if self.anger_level >= 100:
            self.anger_time = Constants.ANGER_MAX_TIME
            self.anger_level = 0

    def is_angry(self):
        return self.anger_time > 0

    @property
    def anger(self):
        if self.anger_time > 0:
            return 100
        else:
            return min(self.anger_level, 100)