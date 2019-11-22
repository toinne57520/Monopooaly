import pygame
from pygame.locals import *
from interface_constantes import *
import json
import board
import time

global piece_2, piece_3
global houses_1,houses_2,houses_3,houses_4,houses_5


pygame.init()
#
# # Define the dimensions of screen object
# font = pygame.font.Font(None, 15)
#screen = pygame.display.set_mode((window_dimension, window_dimension))
#background = pygame.image.load(background_homepage).convert()
#screen.blit(background, (0, 0))

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
    liste = ['a','b','c','d','e','f']
    for i in dict.keys():
        actions.append(liste[int(i)] + " - " +dict[i])
    return actions

def choose_actions_pygame():
    liste = ['a', 'b', 'c', 'd', 'e', 'f']
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key in [K_a,K_b,K_c,K_d,K_e,K_f]:
                nom = pygame.key.name(event.key)
                choice = liste.index(nom)
                return choice
    return -1

def blit_piece(surface,position, piece, indice_x, indice_y):
    """
    La position est la place de la case sur le plateau.
    Piece est le pion à coller à cette position.
    :param surface:
    :param position:
    :return:
    """

    pion = pygame.image.load('images/'+piece+'.png').convert_alpha()
    surface.blit(pion, (coordonnees[position][indice_x], coordonnees[position][indice_y]))

def blit_houses(surface,position, houses):
    """
    La position est la place de la case sur le plateau.
    Houses est le groupe de maison à coller à cette position.
    :param surface:
    :param position:
    :return:
    """
    maison = pygame.image.load('images/'+houses+'.png').convert_alpha()
    surface.blit(maison, (coordonnees[position][0], coordonnees[position][1]))

def blit_images_on_board(surface,dict_board_state):
    """
    on regarde chaque case du plateau et on va mettre les images de maisons et de pions nécessaires
    :param dict_board_state:
    :return:
    """
    for position in list(dict_board_state.keys())[1:]:
        #on colle le groupe de maison approprié

        nb_houses = dict_board_state[position]["nb_houses"]
        if nb_houses>0:
            image_house = 'houses_'+str(nb_houses)
            blit_houses(surface,int(position),image_house)

        #on colle les pions
        if len(dict_board_state[position]["players"])>0:
            for i in range(len(dict_board_state[position]["players"])):
                image_piece = dict_board_state[position]["pieces"][i]
                blit_piece(surface, int(position), image_piece,2*(i+1),2*(i+1)+1)
