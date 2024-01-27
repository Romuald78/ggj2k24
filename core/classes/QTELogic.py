import time
import arcade

# Constants for the QTE bar display px
QTE_BAR_WIDTH = 200
QTE_BAR_HEIGHT = 10
QTE_CURSOR_WIDTH = 5

"""
class QTEBarState:
    def __init__(self, active, timeout,minProgress,maxProgress):
        self.startTimer = 0
        self.active = active
        self.timeout = timeout
        self.currentBarProgress = 0
        self.minProgress = minProgress
        self.maxProgress = maxProgress
        """

#first interaction start the QTE then the bar apears and the player has to press the button once it either fails or succeeds then QTE is over
def notifyQTEInteraction(qteSTates, player):
    for qte in qteSTates:
        #TODO here check player on QTE object interaction
        """
        if Collisions.AABBs((player.left, player.top),
                            (player.right, player.bottom),
                            (stair.left, stair.top),
                            (stair.right, stair.bottom)):
        """
        if qte.active == False:
            #update the state
            qte.active = True
            #TODO freeze the player
            qte.startTimer = time.time()
            print("QTE started")
        else: #qte is active
            #check if the player succeded
            if qte.currentBarProgress >= qte.minProgress and qte.currentBarProgress <= qte.maxProgress:
                print("QTE success")
                qte.active = False
            else:
                print("QTE failed - missed")
                qte.active = False

def qteDraw(qteSTates):
    for qte in qteSTates:
        if qte.active == True:
            # Increment or decrement the progress based on the direction
            if qte.currentBarProgress >= 1.0:
                qte.direction = -1  # Reverse direction when reaching the end
            elif qte.currentBarProgress <= 0.0:
                qte.direction = 1  # Reverse direction when reaching the start

            qte.currentBarProgress += 0.01 * qte.direction  # Adjust the step size as needed

            if(qte.startTimer + qte.timeout) < time.time():
                print("QTE failed - timeout")
                qte.active = False

            BAR_X = qte.x
            BAR_Y = qte.y

            # Calculate the left and right edges of the "win area"
            win_area_left = (qte.minProgress - 0.5) * QTE_BAR_WIDTH
            win_area_right = (qte.maxProgress - 0.5) * QTE_BAR_WIDTH
            win_area_width = win_area_right - win_area_left

            # Draw the QTE bar background at the specified position (BAR_X, BAR_Y)
            arcade.draw_rectangle_filled(BAR_X, BAR_Y, QTE_BAR_WIDTH, QTE_BAR_HEIGHT, arcade.color.GRAY)

            # Draw the QTE "win area" as a green rectangle
            arcade.draw_rectangle_filled(BAR_X + win_area_left + (win_area_width/2), BAR_Y, win_area_right - win_area_left, QTE_BAR_HEIGHT,
                                         arcade.color.GREEN)

            # Calculate the cursor position based on current progress
            cursor_x = BAR_X + (qte.currentBarProgress - 0.5) * QTE_BAR_WIDTH

            # Draw the QTE cursor at the specified position (cursor_x, BAR_Y)
            arcade.draw_rectangle_filled(cursor_x, BAR_Y, QTE_CURSOR_WIDTH, QTE_BAR_HEIGHT, arcade.color.RED)


