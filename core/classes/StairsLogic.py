from core.utils.utils import Collisions

"""
class Stairs:
    def __init__(self, x0, y0, w0, h0,id,dest_id):
        self.x = x0
        self.y = y0
        self.w = w0
        self.h = h0
        self.id = id
        self.dest_id = dest_id
"""


# compute the destinatio coords for a stair
def computeDestCoords(stair, stairs):
    if(stair.dest_x != -1):
        return
    # find the id of the stair the player is on and add a dest x y for the player TP
    dest = stair.dest_id
    for stairDest in stairs:
        if stairDest.id == dest:
            stair.dest_x = stairDest.x
            stair.dest_y = stairDest.bottom
            return
    #print("ERROR: could not find stair with id " + dest)

def processStairsHighlight(stairs, player):
    for stair in stairs:
        computeDestCoords(stair,stairs)
        if Collisions.AABBs((player.left, player.top),
                            (player.right, player.bottom),
                            (stair.left, stair.top),
                            (stair.right, stair.bottom)):
            stair.highlight = True # TODO
        else:
            stair.highlight = False

def processStairsAction(stairs, player):
    for stair in stairs:
        computeDestCoords(stair,stairs)
        if Collisions.AABBs((player.left, player.top),
                            (player.right, player.bottom),
                            (stair.left, stair.top),
                            (stair.right, stair.bottom)):
            if(stair.dest_x != -1):
                # TODO
                print("stairs " + stair.id + " to " + stair.dest_id)
                # move player to dest_id
                player.tp(stair.dest_x, stair.dest_y)
                return True
    return False

