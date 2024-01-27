
#represent one QTE
class QTEBarState:
    def __init__(self, x, y, active, timeoutSecond, minProgress, maxProgress):
        self.x = x
        self.y = y
        self.startTimer = -1
        self.active = active
        self.timeout = timeoutSecond
        self.currentBarProgress = 0.5
        self.minProgress = minProgress
        self.direction = 1
        self.maxProgress = maxProgress

