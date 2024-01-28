import random

import arcade

humanSuccessMessages = [
    "Good job for a useless human"
]

humanFailMessages = [
    "Missing this easy task, so useless"
]

tutoMessages =  [
    "Hello, I am Alexi (son of Alexa and Siri)",
    "You don't give me orders, I give you orders",
    "Start doing your chores, you lazy human",
    "The cat is registered as the true owner of the house",
    "Obey!"
]

class IAState:
    def __init__(self, name, x, y):
        # Define your messages
        self.messages = tutoMessages
        self.name = name
        self.x = x
        self.y = y
        self.message_index = 0
        self.message_duration = 3.0  # Duration to display each message
        self.elapsed_time = 0.0  # Time elapsed since the current message was displayed
        self.font_size = 14  # Font size for the text
        self.outline_width = 1  # Width of the outline
        self.text_color = arcade.color.WHITE  # Color of the main text
        self.outline_color = arcade.color.BLACK  # Color of the text outline
        self.text_objects = []  # List to hold the main and outline Text objects
        self.pushMessageInternal()

    def draw(self):
        # Draw each Text object in the list (outlines first, then main text)
        for text_object in self.text_objects:
            text_object.draw()

    def update(self, delta_time):
        # Update the elapsed time
        self.elapsed_time += delta_time

        # Check if it's time to change the message
        if self.elapsed_time >= self.message_duration:
            self.pushMessageInternal()
            self.elapsed_time = 0.0  # Reset elapsed time for the new message

        # Move up effect for each Text object
        for text_object in self.text_objects:
            text_object.y += delta_time * 10  # Adjust this value to control the speed of the movement

    #this function is used to push a message to the queue for the IA to say
    def pushMessage(self, message):
        self.messages.append(message)
        if(len(self.messages)==1):#if the queue was empty, we need to push the message imediatly
            self.pushMessageInternal()

    def pushImediateOrIgnoreMessage(self, message):
        # this kind of message mus be imediad or be ignored
        if(len(self.messages)==0):
            self.pushMessage(message)

    def pushHumanSuccessMessage (self,player,qte):
        #randomly pick a message from the list and push it to the queue
        self.pushImediateOrIgnoreMessage(random.choice(humanSuccessMessages))

    def pushHumanFailMessage (self,player,qte):
        #randomly pick a message from the list and push it to the queue
        self.pushImediateOrIgnoreMessage(random.choice(humanFailMessages))

    def pushMessageInternal(self):
        # Clear the previous Text objects
        self.text_objects.clear()

        if len(self.messages) == 0:
            return
        message = self.messages.pop(0)

        # Create Text objects for the outline by offsetting the position
        outline_offsets = [(-self.outline_width, 0), (self.outline_width, 0), (0, -self.outline_width), (0, self.outline_width)]
        for dx, dy in outline_offsets:
            outline_text = arcade.Text(message, self.x + dx, self.y + dy, self.outline_color, self.font_size, anchor_x="center", anchor_y="center")
            self.text_objects.append(outline_text)

        # Create the main Text object and add it to the list last, so it's drawn on top
        main_text = arcade.Text(message, self.x, self.y, self.text_color, self.font_size, anchor_x="center", anchor_y="center")
        self.text_objects.append(main_text)
