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

def blit_actions(surface, L, pos):
    word_height = 15
    x, y = pos
    font = pygame.font.Font(None, 14)
    for line in L:
        to_blit = font.render(line, 11, (10,10,10))
        surface.blit(to_blit, (x, y))
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def transform_actions(dict):
    actions = []
    liste = ['a', 'b', 'c', 'd', 'e', 'f','g', 'h', 'i', 'j', 'k', 'l','m','n','o','p','q','r']
    for i in dict.keys():
        actions.append(liste[int(i)] + " - " +dict[i])
    return actions

def choose_actions_pygame():
    liste = ['a', 'b', 'c', 'd', 'e', 'f','g', 'h', 'i', 'j', 'k', 'l','m','n','o','p','q','r']
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key in [K_a,K_b,K_c,K_d,K_e,K_f,K_g,K_h,K_i,K_j,K_k,K_l,K_m,K_n,K_o,K_p,K_q,K_r]:
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
    #les rangées horizontales
    if (position <= 10) or (position >= 20 and position <= 30):
        maison = pygame.image.load('images/'+houses+'.png').convert_alpha()
        surface.blit(maison, (coordonnees[position][0], coordonnees[position][1]))

    #les rangées verticales
    if (position >= 10 and position <= 20) or (position > 30):
        maison = pygame.image.load('images/'+houses+'_v.png').convert_alpha()
        surface.blit(maison, (coordonnees[position][0], coordonnees[position][1]))

def blit_images_on_board(surface,dict_board_state):
    """
    on regarde chaque case du plateau et on va mettre les images de maisons et de pions nécessaires
    :param dict_board_state:
    :return:
    """
    for position in list(dict_board_state.keys())[2:-int(dict_board_state["nb_players"])]:
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

def blit_infos_in_column(surface,dict_board_state):
    x, y = 900, 100
    coord = []
    for player in list(dict_board_state.keys())[42:]:
        word_height = 16

        L = [player] + ["Argent : " + str(dict_board_state[player]["money"])]

        #afficher le pion du joueur
        image_piece = dict_board_state[player]["piece"]
        pion = pygame.image.load('images/' + image_piece + '.png').convert_alpha()
        surface.blit(pion, (x, y-40))

        #Afficher le nom et l'argent
        L = [player] + ["Argent : " + str(dict_board_state[player]["money"])]
        word_height = 16
        font = pygame.font.Font(None, 16)
        coord.append([player,x-40,y])
        for line in L:
            to_blit = font.render(line, 11, (10, 10, 10))
            surface.blit(to_blit, (x, y))
            y += word_height  # Start on new row.

        #Afficher les possessions d'une certaine couleur
        for asset in dict_board_state[player]["assets"]:
            color = asset[1]
            if asset[2]==True:
                color="grey"
            to_blit2 = font.render(asset[0], 11, colors_rgb[color])
            surface.blit(to_blit2, (x, y))
            y += word_height
        y+=100 #affichage du joueur suivant décalé
    return coord

def blit_dice(surface,x,y):
    """
    affiche des dés à côté du nom du joueur dont c'est le tour
    :param surface:
    :param status:
    :return:
    """
    dice = pygame.image.load('images/dice.png').convert_alpha()
    surface.blit(dice,(x,y))