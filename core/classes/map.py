import json

from core.classes.People import Human
from core.classes.Pigeon import Pigeon
from core.classes.IAState import IAState
from core.classes.QTELogic import qteBuilder
from core.classes.interface_pos import getNearestElement
from core.classes.item import Item
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
        # pigeon
        self.pigeon = None

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
        self.ia = None

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
                self.stairs.append( Stairs(x, y - (h / 4), w, (h / 2),stair['id'],stair['dest'] ,stair.get("type",None)))
            for item in floor['items']:
                dx = item['posx'] * self.backhouse.width
                x  = dx + self.__x0
                y  = dy + self.__y0
                itm = Item(item['name'],
                           x0=x, y0=y,
                           ratio=self.__ratio,
                           init_type=item['init_type'])
                self.items[item['posz']].append(itm)
                if item.get("qte", None) is not None:
                    qteBuilder(self.qte, x, y+h-(0.07*self.backhouse.height),itm,item['qte'],item['init_type'])
                if item.get("ia", None) is not None:
                    self.ia = IAState(item['ia'],x,y+h-(0.07*self.backhouse.height))


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

        # Add pigeon
        x = self.W * 0.846
        y = self.H * 0.320
        self.pigeon = Pigeon(x, y, self.ratio)

    @property
    def ratio(self):
        return self.__ratio

    @property
    def human_start_pix(self):
        return self.__human_start

    @property
    def cat_start_pix(self):
        return self.__cat_start

    def getNearestActivity(self, player):
        clr = (255, 240, 240, 255)
        if type(player) is Human:
            clr = (240, 255, 240, 255)
        all = []
        for layer in self.items:
            all += self.items[layer]

        all.append(self.pigeon)
        self.pigeon.highlight(False)

        all = list(filter(lambda x:x.can_interact(player), all))
        itm = getNearestElement(all, player)
        margin  = (itm.width * Constants.ITEM_HITBOX_COEF) / 2
        margin2 = (player.width   * Constants.ITEM_HITBOX_COEF) / 2
        if Collisions.AABBs( (player.left  + margin2 , player.top),
                             (player.right - margin2 , player.bottom),
                             (itm.left  + margin, itm.top),
                             (itm.right - margin, itm.bottom) ):
            itm.highlight(True, clr)
        return itm

    def clear_highlights(self):
        for layer in self.items:
            for item in self.items[layer]:
                item.highlight(False)

    def process_player(self, p, deltaTime):
        # pigeon activity
        self.pigeon.update(deltaTime)

        # Block player according to wall positions
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

        # Highlight items according to player type and position
        itm = self.getNearestActivity(p)

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
        if layer == "front":
            self.pigeon.draw()
