import pygame
from pygame.locals import *

#paramètre de la fenêtre

number_square_side = 13
square_dimension = 60
window_dimension = number_square_side*square_dimension
bandeau = 20
colonne = 300

#titre et icone de la fenêtre
icon_image = 'images/maison.png'
title = 'MonoPOOAly'


#liste des images pour le jeu
background_homepage = 'images/fond_rempli.png'
background_play = 'images/fond_rempli.png'

#corespondance des couleurs du plateau
colors_rgb = {"marron" : (148, 71, 43),
              "bleu ciel" : (186, 227, 253),
              "violet" : (218, 44, 139),
              "orange" : (247, 142, 0),
              "rouge" : (218, 5, 15),
              "jaune" : (253, 237, 0),
              "vert" : (27, 167, 72),
              "bleu fonce" : (0, 104, 180),
              "trainstation": (10,10,10),
              "grey": (167, 176, 183)}

# on veut une liste pour chaque case i avec
# [x_maison, y_maison, x_pion1, y_pion1, x_pion2, y_pion2, x_pion3, y_pion3, x_pion4, y_pion4]
coordonnees = [[0]]*41


for i in range(0, 11):  # ligne du bas en partant de la case départ
    #pour les maisons
    x_maison = (number_square_side - 2 - i) * square_dimension  # On compte à partir de 0
    y_maison = 11 * square_dimension  # dernière ligne

    #pour le pion 1 (haut gauche)
    x_pion1=(number_square_side - 2 - i) * square_dimension
    y_pion1=11 * square_dimension+ bandeau

    # pour le pion 2 (haut droit)
    x_pion2 = (number_square_side - 2 - i) * square_dimension + square_dimension/2
    y_pion2 = 11 * square_dimension + bandeau

    # pour le pion 3 (bas gauche)
    x_pion3 = (number_square_side - 2 - i) * square_dimension
    y_pion3 = 11 * square_dimension + bandeau + (2*square_dimension - bandeau)/2

    # pour le pion 4 (bas droit)
    x_pion4 = (number_square_side - 2 - i) * square_dimension + square_dimension/2
    y_pion4 = 11 * square_dimension + bandeau + (2*square_dimension - bandeau)/2

    coordonnees[i] = [x_maison, y_maison, x_pion1, y_pion1, x_pion2, y_pion2, x_pion3, y_pion3, x_pion4, y_pion4]

for i in range(11, 21):  # première colonne de la prison au parc gratuit
    # pour les maisons
    x_maison = 0 * square_dimension + (2*square_dimension-bandeau)
    y_maison = (number_square_side + 8 - i) * square_dimension

    # pour le pion 1 (haut gauche)
    x_pion1 = 0 * square_dimension
    y_pion1 = (number_square_side + 8 - i) * square_dimension

    # pour le pion 2 (haut droit)
    x_pion2 = 0 * square_dimension + (2*square_dimension-bandeau)/2
    y_pion2 = (number_square_side + 8 - i) * square_dimension

    # pour le pion 3 (bas gauche)
    x_pion3 = 0 * square_dimension
    y_pion3 = (number_square_side + 8 - i) * square_dimension + square_dimension/2

    # pour le pion 4 (bas droit)
    x_pion4 = 0 * square_dimension + (2*square_dimension-bandeau)/2
    y_pion4 = (number_square_side + 8 - i) * square_dimension + square_dimension/2

    coordonnees[i] = [x_maison, y_maison, x_pion1, y_pion1, x_pion2, y_pion2, x_pion3, y_pion3, x_pion4, y_pion4]

for i in range(21, 31):  # première ligne du parc gratuit à la case 'allez en prison'
    # pour les maisons
    x_maison = (i - 19) * square_dimension
    y_maison = 0 * square_dimension + (2*square_dimension-bandeau)

    # pour le pion 1 (haut gauche)
    x_pion1 = (i - 19) * square_dimension
    y_pion1 = 0

    # pour le pion 2 (haut droit)
    x_pion2 = (i - 19) * square_dimension + square_dimension/2
    y_pion2 = 0

    # pour le pion 3 (bas gauche)
    x_pion3 = (i - 19) * square_dimension
    y_pion3 = 0 + (2*square_dimension-bandeau)/2

    # pour le pion 4 (bas droit)
    x_pion4 = (i - 19) * square_dimension + square_dimension/2
    y_pion4 = 0 + (2*square_dimension-bandeau)/2

    coordonnees[i] = [x_maison, y_maison, x_pion1, y_pion1, x_pion2, y_pion2, x_pion3, y_pion3, x_pion4, y_pion4]

for i in range(31, 41):  # dernière colonne de 'allez en prison' à la case départ
    # pour les maisons
    x_maison = 11 * square_dimension
    y_maison = (i - 29) * square_dimension

    # pour le pion 1 (haut gauche)
    x_pion1 = 11 * square_dimension + bandeau
    y_pion1 = (i - 29) * square_dimension

    # pour le pion 2 (haut droit)
    x_pion2 = 11 * square_dimension + bandeau + (2*square_dimension-bandeau)/2
    y_pion2 = (i - 29) * square_dimension

    # pour le pion 3 (bas gauche)
    x_pion3 = 11 * square_dimension + bandeau
    y_pion3 = (i - 29) * square_dimension + square_dimension/2

    # pour le pion 4 (bas droit)
    x_pion4 = 11 * square_dimension + bandeau + (2*square_dimension-bandeau)/2
    y_pion4 = (i - 29) * square_dimension + square_dimension/2

    coordonnees[i] = [x_maison, y_maison, x_pion1, y_pion1, x_pion2, y_pion2, x_pion3, y_pion3, x_pion4, y_pion4]






