import json

from core.classes.QTELogic import qteBuilder
from core.classes.item import Item
from core.classes.QTEBarState import QTEBarState
from core.classes.constants import Constants
from core.classes.wall import Wall
from core.utils.utils import Gfx, Collisions
from core.classes.Stairs import Stairs


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
        self.__ratio = 1.0

        # get config
        fp = open(cfg_filepath)
        cfg = json.load(fp)
        fp.close()

        # Get ratio
        self.__ratio = max( self.W / cfg['width'],
                            self.H / cfg['height'] )

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
        # STAIRS
        self.stairs = []
        # ITEMS
        self.items  = {"front": [],
                       "back" : []}
        # QTE
        self.qte = []

        for floor in cfg['floors']:
            h  = floor['height'] * self.backhouse.height
            dy = floor['posy'] * self.backhouse.height
            for wall in floor['walls']:
                dx = wall['posx'] * self.backhouse.width
                x  = dx + self.__x0
                y  = dy + self.__y0
                w  = 0.015 * self.backhouse.width
                y += h / 2
                self.walls.append( Wall(x, y, w, h) )
            for stair in floor.get('stairs', []):
                dx = stair['posx'] * self.backhouse.width
                x  = dx + self.__x0
                y  = dy + self.__y0
                w  = stair.get("width",0.1) * self.backhouse.width
                y += h / 2
                self.stairs.append( Stairs(x, y - (h / 4), w, (h / 2),stair['id'],stair['dest']) )
            for item in floor['items']:
                dx = item['posx'] * self.backhouse.width
                x  = dx + self.__x0
                y  = dy + self.__y0
                itm = Item(item['name'], x0=x, y0=y, ratio=self.__ratio)
                self.items[item['posz']].append(itm)
                if item.get("qte", None) is not None:
                    qteBuilder(self.qte, x, y+h+10,itm,item['qte'])


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
    def ratio(self):
        return self.__ratio

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
            for s in self.stairs:
                s.debug_draw()

    def draw_items(self, layer):
        for itm in self.items[layer]:
            itm.draw()
