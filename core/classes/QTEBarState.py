
#represent one QTE
class QTEBarState:
    def __init__(self, x, y,item, timeoutSecond, minProgress, maxProgress,type):
        self.x = x
        self.y = y
        self.item = item
        self.startTimer = -1
        self.active = False
        self.timeout = timeoutSecond
        self.currentBarProgress = 0.5
        self.minProgress = minProgress
        self.direction = 1
        self.maxProgress = maxProgress
        self.currentPlayer = None
        self.type = type

