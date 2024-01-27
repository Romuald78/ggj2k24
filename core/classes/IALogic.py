import arcade


def iaDrawStep(iaState):
    # Text to display
    text = "Hello, Arcade!"

    # Position for the text
    x = 100  # X coordinate
    y = 300  # Y coordinate

    # Display the text
    arcade.draw_text(text, x, y, arcade.color.BLACK, 14)