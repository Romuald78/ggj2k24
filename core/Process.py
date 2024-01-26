# ====================================================================================================
# IMPORTS
# ====================================================================================================
import arcade.key

from .classes.constants import Constants
from .pages.page_0_intro import Page0Intro
from .pages.page_1_splash import Page1Splash
from .pages.page_2_select import Page2Select
from .utils.utils import Text


class Process:
    # ====================================================================================================
    # PARAMETERS
    # ====================================================================================================

    # ====================================================================================================
    # CONSTRUCTOR
    # ====================================================================================================
    def __init__(self, width, height, ratio, window):
        self.SCREEN_WIDTH = int(width * ratio)
        self.SCREEN_HEIGHT = int(height * ratio)
        self.window = window

    def selectPage(self, index, args=None):
        self.pageIndex = index
        self.currentPage = self.pages[self.pageIndex]
        self.currentPage.refresh(args)

    # ====================================================================================================
    # INIT
    # ====================================================================================================
    def setup(self):
        # Add all pages
        self.pages = []
        # Instanciate all pages
        self.pages.append(Page0Intro (self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.window, self))
        self.pages.append(Page1Splash(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.window, self))
        self.pages.append(Page2Select(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.window, self))

        # Set first page
        self.pageIndex = 0
        self.currentPage = self.pages[self.pageIndex]
        # Setup all the pages only once
        for p in self.pages:
            p.setup()
        # FPS
        self.display_fps = False
        self.fps_text = None
        self.frame_count = 0
        self.frame_time = 0.0

    # ====================================================================================================
    # UPDATE
    # ====================================================================================================
    def on_update(self, deltaTime):
        self.frame_time += deltaTime
        self.frame_count += 1
        if self.frame_count == 60:
            params = {
                "message": f"{int(60/self.frame_time)} FPS",
                "x": 10,
                "y": self.SCREEN_HEIGHT - 10,
                "color": (0, 0, 0, 255),
                "size": 10,
                "alignH": 'left',
                "alignV": 'top'
            }
            self.fps_text = Text.create_text(params)
            self.frame_count = 0
            self.frame_time  = 0

        # display FPS always on top left corner
        if self.display_fps:
            if self.fps_text is not None:
                vwprt = self.window.get_viewport()
                ratio = (vwprt[1] - vwprt[0])/1920
                self.fps_text.x = vwprt[0] + 10
                self.fps_text.y = vwprt[3] - 10
                self.fps_text.font_size = max(10, 10 * ratio)

        # process current page
        self.currentPage.on_update(deltaTime)

    # ====================================================================================================
    # RENDERING
    # ====================================================================================================
    def draw(self):
        # Draw page
        self.currentPage.draw()
        # Draw debug
        if Constants.DEBUG:
            try:
                self.currentPage.draw_debug()
            except :
                pass
        # Draw FPS
        if self.display_fps:
            if self.fps_text is not None:
                self.fps_text.draw()

    # ====================================================================================================
    # KEYBOARD EVENTS
    # key is taken from : arcade.key.xxx
    # ====================================================================================================
    def onKeyEvent(self, key, isPressed):
        # Display FPS
        if isPressed and key == arcade.key.F9:
            self.display_fps = not self.display_fps
            print(f"DISPLAY FPS = [{['OFF', 'ON'][int(self.display_fps)]}]")

        # Toggle Debug mode
        if isPressed and key == arcade.key.F10:
            Constants.DEBUG = not Constants.DEBUG
            print(f"MODE DEBUG = [{['OFF', 'ON'][int(Constants.DEBUG)]}]")

        # Send key event to current page
        try:
            self.currentPage.onKeyEvent(key, isPressed)
        except Exception as ex:
            print(f"[ERROR] process key event : {ex}")

    # ====================================================================================================
    # GAMEPAD BUTTON EVENTS
    # buttonName can be "A", "B", "X", "Y", "LB", "RB", "VIEW", "MENU", "LSTICK", "RSTICK"
    # ====================================================================================================
    def onButtonEvent(self, gamepadNum, buttonName, isPressed):
        try:
            self.currentPage.onButtonEvent(gamepadNum, buttonName, isPressed)
        except Exception as ex:
            print(f"[ERROR] process button event : {ex}")

    # ====================================================================================================
    # GAMEPAD AXIS EVENTS
    # axisName can be "X", "Y", "RX", "RY", "Z"
    # ====================================================================================================
    def onAxisEvent(self, gamepadNum, axisName, analogValue):
        try:
            self.currentPage.onAxisEvent(gamepadNum, axisName, analogValue)
        except Exception as ex:
            print(f"[ERROR] process axis event : {ex}")

    # ====================================================================================================
    # MOUSE MOTION EVENTS
    # ====================================================================================================
    def onMouseMotionEvent(self, x, y, dx, dy):
        try:
            self.currentPage.onMouseMotionEvent(x, y, dx, dy)
        except Exception as ex:
            print(f"[ERROR] process mouse motion event : {ex}")

    # ====================================================================================================
    # MOUSE BUTTON EVENTS
    # ====================================================================================================
    def onMouseButtonEvent(self, x, y, buttonNum, isPressed):
        try:
            print(buttonNum)
            self.currentPage.onMouseButtonEvent(x, y, buttonNum, isPressed)
        except Exception as ex:
            print(f"[ERROR] process mouse button event : {ex}")
