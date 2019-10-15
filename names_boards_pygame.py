import pygame
from pygame.locals import *
from interface_constantes import *
import json
import board


pygame.init()

#Ouverture de la fenêtre Pygame (carré : largeur = hauteur)
window = pygame.display.set_mode((window_dimension, window_dimension))
#Icone
icon = pygame.image.load(icon_image)
pygame.display.set_icon(icon)
#Titre
pygame.display.set_caption(title)

#Boucle principale pour empêcher la fenêtre de se fermer immédiatement
continuer = 1
background = pygame.image.load(background_homepage).convert()
window.blit(background, (0, 0))
while continuer:
    # Chargement et affichage de l'écran d'accueil


    # Actualisation

    pygame.display.flip()

    # On remet ces variables à 1 à chaque tour de boucle
    continuer_jeu = 1
    continuer_accueil = 1

    # Boucle de la page d'accueil
    while continuer_accueil:

        # On limite la vitesse de la boucle
        pygame.time.Clock().tick(30)

        for event in pygame.event.get():

            # Si l'utilisateur quitte le jeu, on met les variables des deux boucles à 0
            if event.type == QUIT :
                continuer_accueil = 0
                continuer_jeu = 0
                continuer = 0
                # Variable de choix du plateau
                choix = 0

            elif event.type == KEYDOWN:
                # Lancement du plateau 1
                if event.key == K_a:
                    continuer_accueil = 0  # On quitte la boucle d'accueil pour passer dans la boucle de jeu
                    choix = 'Boards/data.json'  # On enregistre le chemin du plateau à charger
                # Lancement du plateau 2
                elif event.key == K_b:
                    continuer_accueil = 0
                    choix = 'plateau2'

    if choix != 0: #on vérifie que le joueur a bien fait un choix
        # Chargement du fond
        fond = pygame.image.load(background_play).convert()

        # Génération d'un niveau à partir du json
        #board = board.Board(choix)
        #niveau.generer()
        #niveau.afficher(fenetre)


        with open(choix) as data :
            squares = json.load(data)["dependencies"]

        #en faire une méthode de board
        #affichage des noms des cases du plateau
        for i in range (0,11): #ligne du bas en partant de la case départ
            for square in squares :
                if square["position"]==i:
                    font = pygame.font.Font(None, 7)
                    name = font.render(square["name"], 1, (10, 10, 10))
                    name_x=(number_square_side-2-i)*square_dimension #On compte à partir de 0
                    name_y=12 *square_dimension+square_dimension/3 #dernière ligne
                    window.blit(name,(name_x,name_y))
                    #pour afficher les prix : faire distinction entre terrains et les cases particulieres qui n'ont pas de value
                    #price=str(square["value"])
                    #value = font.render((price), 1, (10, 10, 10))
                    #value_x = (number_square_side - 1 - i) * square_dimension  # On compte à partir de 0
                    #value_y = 12 * square_dimension + square_dimension / 2
                    # window.blit(value, (value_x,value_y))
        for i in range (11,21): #première colonne de la prison au parc gratuit
            for square in squares :
                if square["position"]==i:
                    font = pygame.font.Font(None, 13)
                    name = font.render(square["name"], 1, (10, 10, 10))
                    name_x=0 *square_dimension +square_dimension/3 #première colonne
                    name_y=(number_square_side+8-i) *square_dimension
                    window.blit(name,(name_x,name_y))

        for i in range (21,31): #première ligne du parc gratuit à la case 'allez en prison'
            for square in squares :
                if square["position"]==i:
                    font = pygame.font.Font(None, 13)
                    name = font.render(square["name"], 1, (10, 10, 10))
                    name_x=(i-19) *square_dimension
                    name_y= 0 *square_dimension +square_dimension/3 #première ligne
                    window.blit(name,(name_x,name_y))

        for i in range (31,40): #dernière colonne de 'allez en prison' à la case départ
            for square in squares :
                if square["position"]==i:
                    font = pygame.font.Font(None, 13)
                    name = font.render(square["name"], 1, (10, 10, 10))
                    name_x=12 *square_dimension+square_dimension/3 #dernière colonne
                    name_y=(i-29) *square_dimension
                    window.blit(name,(name_x,name_y))