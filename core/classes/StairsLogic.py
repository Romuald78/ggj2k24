from core.utils.utils import Collisions


def processStairs(stairs, p):
    for stair in stairs:
        if Collisions.AABBs((p.left, p.top),
                            (p.right, p.bottom),
                            (stair.left, stair.top),
                            (stair.right, stair.bottom)):
            # TODO
            print("stairs "+stair.id+" to "+stair.dest_id)