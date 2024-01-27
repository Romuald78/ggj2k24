import json
from random import random

from core.classes.constants import Constants
from core.classes.wall import Wall
from core.utils.utils import Gfx, Collisions


class Map:

    def __init__(self, cfg_filepath, W, H):
        # store screen size
        self.W = W
        self.H = H
        # ref point
        self.__x0 = 0
        self.__y0 = 0
        # Start positions
        self.__human_start = {}
        self.__cat_start = {}

        # get config
        fp = open(cfg_filepath)
        cfg = json.load(fp)
        fp.close()

        # BACKGROUND
        params = {
            "filePath": cfg['background_gfx'],
            "size": (self.W, self.H),
            "position": (self.W / 2, self.H / 2)
        }
        self.backhouse = Gfx.create_fixed(params)

        # Ref point
        self.__x0 = (self.W - self.backhouse.width) / 2
        self.__y0 = (self.H - self.backhouse.height) / 2

        # WALLS (blocking)
        self.walls = []
        for floor in cfg['floors']:
            h  = floor['height'] * self.backhouse.height
            dy = floor['posy'] * self.backhouse.height
            for wall in floor['walls']:
                dx = wall['posx'] * self.backhouse.width
                x  = dx + self.__x0
                y  = dy + self.__y0
                w  = 0.009375 * self.backhouse.width
                y += h / 2
                self.walls.append( Wall(x, y, w, h) )

        # START POSITIONS
        hx = cfg['human_start']['posx']
        cx = cfg['cat_start']['posx']
        hr = cfg['human_start']['xrange']
        cr = cfg['cat_start']['xrange']
        hf = cfg['human_start']['floor']
        cf = cfg['cat_start']['floor']
        # pixel positions
        hx *= self.backhouse.width
        cx *= self.backhouse.width
        hx += self.__x0
        cx += self.__x0
        hr *= self.backhouse.width
        cr *= self.backhouse.width
        hy = cfg['floors'][hf]['posy'] * self.backhouse.height + self.__y0
        cy = cfg['floors'][cf]['posy'] * self.backhouse.height + self.__y0
        self.__human_start = (hx, hy, hr)
        self.__cat_start = (cx, cy, cr)

    @property
    def human_start_pix(self):
        return self.__human_start

    @property
    def cat_start_pix(self):
        return self.__cat_start

    def process_player(self, p):
        for wall in self.walls:
            if Collisions.AABBs( (p.left    , p.top),
                                 (p.right   , p.bottom),
                                 (wall.left , wall.top),
                                 (wall.right, wall.bottom) ):
                # put player outside wall
                if p.x < wall.x:
                    unionx =  wall.left - p.right
                else:
                    unionx = wall.right - p.left
                p.shift(unionx, 0)

    def draw_background(self):
        self.backhouse.draw()
        if Constants.DEBUG:
            for w in self.walls:
                w.debug_draw()


