import random
import time
import arcade

from core.classes.QTEBarState import QTEBarState
from core.utils.utils import Collisions

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

def addAngerOnHuman(people, anger):
    for person in people:
        if person.type == "human":
            person.anger_level += anger
            if person.anger_level >= 100:
                person.anger_level = 100
            elif person.anger_level < 0:
                person.anger_level = 0

# first interaction start the QTE then the bar apears and the player has to press the button once it either fails or succeeds then QTE is over
def notifyQTEInteraction(qteSTates, people, player,ia):
    for qte in qteSTates:
        if Collisions.AABBs((player.left, player.top),
                            (player.right, player.bottom),
                            (qte.item.left, qte.item.top),
                            (qte.item.right, qte.item.bottom)):
            if qte.type==player.type:
                if qte.active == False:
                    # update the state
                    qte.active = True
                    qte.currentPlayer = player
                    player.freeze()
                    qte.startTimer = time.time()
                    print("QTE started")
                # qte is active
                else:
                    # check if the player succeded
                    if qte.minProgress <= qte.currentBarProgress <= qte.maxProgress:
                        print("QTE success")
                        addAngerOnHuman(people, 10 if player.type == "human" else -1)
                        if(ia is not None):
                            ia.pushHumanSuccessMessage(player,qte)
                        player.free()
                        qte.active = False
                    else:
                        print("QTE failed - missed")
                        addAngerOnHuman(people, -10 if player.type == "human" else 1)
                        if(ia is not None):
                            ia.pushHumanFailMessage(player,qte)
                        player.free()
                        qte.active = False
                return True
    return False


def qteBuilder(qteStates, x, y,itm, qteType,type):
    # Define the size of the win area for each difficulty level
    win_area_sizes = {
        "bar-easy": 0.30,  # 30% of the bar
        "bar-medium": 0.20,  # 20% of the bar
        "bar-hard": 0.10  # 10% of the bar
    }

    # Ensure the qteType is valid
    if qteType in win_area_sizes:
        # Determine the size of the win area for the given difficulty
        win_area_size = win_area_sizes[qteType]

        # Randomly select the start point of the win area, ensuring there's enough room for the win area
        win_area_start = random.uniform(0, 1 - win_area_size)

        # Calculate the end point of the win area
        win_area_end = win_area_start + win_area_size

        # Append the new QTEBarState with the calculated win area
        qteStates.append(QTEBarState(x, y, itm, 4, win_area_start, win_area_end,type))
    else:
        print(f"Unknown qteType: {qteType}")


def qteDraw(qteSTates,ia):
    for qte in qteSTates:
        if qte.active == True:
            # Increment or decrement the progress based on the direction
            if qte.currentBarProgress >= 1.0:
                qte.direction = -1  # Reverse direction when reaching the end
            elif qte.currentBarProgress <= 0.0:
                qte.direction = 1  # Reverse direction when reaching the start

            qte.currentBarProgress += 0.01 * qte.direction  # Adjust the step size as needed

            if (qte.startTimer + qte.timeout) < time.time():
                print("QTE failed - timeout")
                if (ia is not None):
                    ia.pushHumanFailMessage(None, qte)
                qte.currentPlayer.free()
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
            arcade.draw_rectangle_filled(BAR_X + win_area_left + (win_area_width / 2), BAR_Y,
                                         win_area_right - win_area_left, QTE_BAR_HEIGHT,
                                         arcade.color.GREEN)

            # Calculate the cursor position based on current progress
            cursor_x = BAR_X + (qte.currentBarProgress - 0.5) * QTE_BAR_WIDTH

            # Draw the QTE cursor at the specified position (cursor_x, BAR_Y)
            arcade.draw_rectangle_filled(cursor_x, BAR_Y, QTE_CURSOR_WIDTH, QTE_BAR_HEIGHT, arcade.color.RED)
