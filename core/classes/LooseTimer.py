import arcade

class LooseTimer:
    def __init__(self, time, screen_width, screen_height,ia, font_size=20, outline_width=2):
        self.time = time  # Total time in seconds
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_size = font_size
        self.outline_width = outline_width
        self.font_color = arcade.color.WHITE  # Main text color
        self.outline_color = arcade.color.BLACK  # Outline color
        self.text_objects = []  # List to hold the main and outline Text objects
        self.last_time = -1  # Variable to track the last updated time
        self.ia = ia
        self.ended = False

    def draw(self):
        # Draw each Text object in the list (outlines first, then main text)
        for text_object in self.text_objects:
            text_object.draw()

    def update(self, delta_time):
        # Subtract the delta_time from the total time
        self.time -= delta_time

        # Prevent the timer from going into negative values
        if self.time < 0:
            self.time = 0
            self.ended = True
            # [TODO] End game display an image in the middle (image is half the screen in size)

        # Update the displayed time only if it has changed (every second)
        current_time = int(self.time)
        if current_time != self.last_time:
            self.last_time = current_time
            self.create_text_objects()

    def create_text_objects(self):
        # Clear any existing Text objects
        self.text_objects.clear()

        # Format the time as MM:SS
        minutes = self.last_time // 60
        seconds = self.last_time % 60
        time_str = f"{minutes:02d}:{seconds:02d}"

        if(seconds == 0):
            self.ia.pushMessage("Speed up, you only have " + str(minutes) + " minutes left!")

        # Calculate position for the timer to be in the top right
        x_position = self.screen_width - 40  # 10 pixels from the right edge
        y_position = self.screen_height - self.font_size - 10  # 10 pixels from the top

        # Create Text objects for the outline by offsetting the position
        outline_offsets = [(-self.outline_width, 0), (self.outline_width, 0), (0, -self.outline_width), (0, self.outline_width)]
        for dx, dy in outline_offsets:
            outline_text = arcade.Text(time_str, x_position + dx, y_position + dy, self.outline_color, self.font_size, anchor_x="right", anchor_y="top")
            self.text_objects.append(outline_text)

        # Create the main Text object and add it to the list last, so it's drawn on top
        main_text = arcade.Text(time_str, x_position, y_position, self.font_color, self.font_size, anchor_x="right", anchor_y="top")
        self.text_objects.append(main_text)

    def isOver(self):
        return self.ended
