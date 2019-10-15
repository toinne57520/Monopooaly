import pygame
from pygame.locals import *
from interface_constantes import *
import json
import board
import time


pygame.init()
#
# # Define the dimensions of screen object
# font = pygame.font.Font(None, 15)
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

def transform_actions(dict):
    actions = []
    for i in dict.keys():
        actions.append(i+ " - "+dict[i])
    return actions

def choose_actions_pygame():
    evenement = pygame.event.wait()
    if evenement.type == pygame.KEYDOWN:
        nom = pygame.key.name(evenement.key)
    return nom