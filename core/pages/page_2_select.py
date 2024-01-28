import arcade

from core.classes.constants import Constants
from core.utils.utils import Gfx


class Page2Select:

    def __cat_color(self):
        colors = []
        for ctrl in self.ctrls:
            colors.append(self.ctrls[ctrl]['cat_color'])
        if not ('' in colors):
            return ''
        elif not (' orange' in colors):
            return ' orange'
        elif not (' white' in colors):
            return ' white'

    def __how_many_human(self):
        count = 0
        for ctrl in self.ctrls:
            if self.ctrls[ctrl]['choice'] == "human":
                count += 1
        return count


    def __back_to_splash(self):
        self.process.selectPage(1)

    def __add_player(self, ctrl):
        if ctrl in self.ctrls:
            player = self.ctrls[ctrl]
            if player['choice'] != "":
                if not player['ready']:
                    self.ctrls[ctrl]['ready'] = True
                else:
                    # check all others ready
                    go = True
                    for ctrl in self.ctrls:
                        go = go and self.ctrls[ctrl]['ready']
                    if go and self.__how_many_human() >= 1 and len(self.ctrls) >= 2:
                        self.process.selectPage(3, self.ctrls)
        elif len(self.ctrls) < 3:
            id = 0
            if ctrl == Constants.KEYBOARD_CTRL:
                id = 2
            elif ctrl == Constants.MOUSE_CTRL:
                id = 1
            params = {
                "filePath"  : "resources/gui/controllers.png",
                "size"      : (self.W/8, self.H/8),
                "position"  : (self.W / 3, 0),
                "spriteBox" : (1, 3, 200, 100),
                "startIndex": id,
                "endIndex"  : id,
                "filterColor" : (255,255,255,128)
            }
            spr = Gfx.create_animated(params)
            params = {
                "filePath": "resources/characters/vieux idle atlas.png",
                "position": (self.W/3, 0),
                "size"    : (self.W/4, self.H/4),
                "spriteBox": (4, 1, 100, 150),
                "startIndex": 0,
                "endIndex": 3,
                "frameDuration": 0.2
            }
            hum = Gfx.create_animated(params)


            catclr = self.__cat_color()
            params = {
                "filePath": f"resources/characters/atlas chat idle{catclr}.png",
                "position": (self.W/3, 0),
                "size"    : (self.W/6, self.H/6),
                "spriteBox": (4, 1, 147, 90),
                "startIndex": 0,
                "endIndex": 3,
                "frameDuration": 0.2,
                "flipH" : True
            }
            cat = Gfx.create_animated(params)

            self.ctrls[ctrl] = {
                'gfx'   : (hum, cat, spr),
                'ready' : False,
                'choice': "",
                'rest_ctrl' : True,
                'cat_color': catclr
            }

    def __remove_player(self, ctrl):
        if ctrl in self.ctrls:
            if self.ctrls[ctrl]['ready']:
                self.ctrls[ctrl]['ready'] = False
            else:
                del self.ctrls[ctrl]
                if len(self.ctrls) == 0:
                    self.__back_to_splash()

    def __change_player_left(self, ctrl):
        if ctrl in self.ctrls:
            player = self.ctrls[ctrl]
            if not player['ready']:
                if player['choice'] == "" and self.__how_many_human() < 1:
                    player['choice'] = "human"
                elif player['choice'] == "cat":
                    player['choice'] = ""

    def __change_player_right(self, ctrl):
        if ctrl in self.ctrls:
            player = self.ctrls[ctrl]
            if not player['ready']:
                if player['choice'] == "":
                    player['choice'] = "cat"
                elif player['choice'] == "human":
                    player['choice'] = ""

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
            "filePath" : "resources/backgrounds/fond maison.png",
            "size" : (self.W, self.H),
            "filterColor": (255,255,255,128),
            "position" : (self.W/2, self.H/2)
        }
        self.gfx =Gfx.create_fixed(params)
        # Select first player (use given controller number)
        if args is not None:
            self.__add_player(args['ctrl'])

    def setup(self):
        self.refresh()

    def on_update(self, deltaTime):
        y = self.H * 0.7
        for ctrl in self.ctrls:
            x = self.W / 2.3
            player = self.ctrls[ctrl]
            # Choose x
            if player['choice'] == 'human':
                x -= self.W / 3.3
            elif player['choice'] == 'cat':
                x += self.W / 3.3
            # choose color
            clr = (255, 255, 255)
            if player['ready']:
                clr = (0, 255, 0)
            # Set properties
            for gfx in player['gfx']:
                gfx.center_x = x
                gfx.center_y = y
                gfx.update_animation(deltaTime)
            player['gfx'][2].color = clr
            player['gfx'][2].center_y -= 100
            y -= self.H/4

    def draw(self):
        self.gfx.draw()
        for ctrl in self.ctrls:
            player = self.ctrls[ctrl]
            if player['choice'] == "human":
                player['gfx'][0].draw()
            elif player['choice'] == "cat":
                player['gfx'][1].draw()
            player['gfx'][2].draw()

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
            if gamepadNum in self.ctrls :
                if self.ctrls[gamepadNum]['rest_ctrl']:
                    if analogValue <= -0.5:
                        self.__change_player_left(gamepadNum)
                        self.ctrls[gamepadNum]['rest_ctrl'] = False
                    elif analogValue >= 0.5:
                        self.__change_player_right(gamepadNum)
                        self.ctrls[gamepadNum]['rest_ctrl'] = False
                else:
                    if abs(analogValue) <= 0.2:
                        self.ctrls[gamepadNum]['rest_ctrl'] = True

    def onMouseMotionEvent(self, x, y, dx, dy):
        pass

    def onMouseButtonEvent(self, x, y, buttonNum, isPressed):
        pass
        # if isPressed:
        #     if buttonNum == 1:
        #         self.__add_player(Constants.MOUSE_CTRL)
        #     elif buttonNum == 4:
        #         self.__remove_player(Constants.MOUSE_CTRL)
        #     elif buttonNum == 8:
        #         self.__change_player_left(Constants.MOUSE_CTRL)
        #     elif buttonNum == 16:
        #         self.__change_player_right(Constants.MOUSE_CTRL)


