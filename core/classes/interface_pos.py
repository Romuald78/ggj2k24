

def getNearestElement(lst, p):
    x1, y1 = p.x, p.y
    dist = 1000000000
    ref  = None
    for elt in lst:
        x0, y0 = elt.getPosition()
        dx = x1 - x0
        dy = y1 - y0
        dx *= dx
        dy *= dy
        d = dx + dy
        if d <= dist:
            dist = d
            ref = elt
    return ref


class InterfacePosition:

    def getPosition(self):
        raise NotImplementedError("Method not implemented yet !")

