import pygame
from pygame.locals import *
from interface_constantes import *
import json
import board
import time


pygame.init()

# Define the dimensions of screen object
font = pygame.font.Font(None, 15)
screen = pygame.display.set_mode((window_dimension, window_dimension))
background = pygame.image.load(background_homepage).convert()
screen.blit(background, (0, 0))

def blit_text(surface, L, pos):
    word_height = 15
    x, y = pos
    font = pygame.font.Font(None, 14)
    for line in L[-4:]:
        to_blit = font.render(line, 11, (10,10,10))
        surface.blit(to_blit, (x, y))
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
        print(line)
    pygame.display.flip()
    pygame.display.update()

gameOn = True

# Our game loop
while gameOn:
    background = pygame.image.load(background_homepage).convert()
    screen.blit(background, (0, 0))
    # for loop through the event queue
    for event in pygame.event.get():

        # Check for KEYDOWN event
        if event.type == KEYDOWN:

            # If the Backspace key has been pressed set
            # running to false to exit the main loop
            if event.key == K_BACKSPACE:
                gameOn = False

        # Check for QUIT event
        elif event.type == QUIT:
            gameOn = False

    # Define where the squares will appear on the screen
    # Use blit to draw them on the screen surface



    # Update the display using flip
    pygame.display.flip()

