import arcade


# Function to draw a progress bar
def drawAngerBar(width, height, percentage):
    """
    Draws a progress bar.

    Parameters:
    - x, y: The center coordinates of the progress bar.
    - width, height: The dimensions of the progress bar.
    - percentage: The current progress as a float between 0.0 and 1.0.
    - background_color: The color of the progress bar background.
    - progress_color: The color of the progress bar fill.
    """
    x = width/2
    y = height - 30
    width = 0.2*width
    height = 0.05*height

    # Draw the background of the progress bar
    arcade.draw_rectangle_filled(x, y, width, height, arcade.color.RED)

    # Calculate the width of the progress based on the percentage
    progress_width = width * percentage

    # Draw the progress on top of the background
    # The progress rectangle's right edge is aligned with the background's right edge
    progress_x = x - (width / 2) + (progress_width / 2)  # Adjust the x position based on progress
    arcade.draw_rectangle_filled(progress_x, y, progress_width, height, arcade.color.BLUE)