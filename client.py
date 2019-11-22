import socket
from clientthread import Clientthread
import pygame
from interface_constantes import *
import pygame_simple
pygame.init()



if __name__ == '__main__':
    # connexion au server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 11100))
    print("En attente des autres joueurs")
    # Welcome message
    welcome_message = sock.recv(1024).decode()
    if welcome_message != u"Bienvenue dans le Monopooaly!":
        raise ValueError("Erreur protocole: attendu welcome message (cote client)")
    print(welcome_message)
    print("Quel est votre nom de joueur ?")
    name_player = input("> ")
    sock.send(name_player.encode())
    clientthread = Clientthread(sock)
    clientthread.start()
    window = pygame.display.set_mode((window_dimension, window_dimension))
    background = pygame.image.load(background_homepage).convert()
    window.blit(background, (0, 0))
    pygame.display.flip()

    while True:
        window = pygame.display.set_mode((window_dimension, window_dimension))
        background = pygame.image.load(background_homepage).convert()
        window.blit(background, (0, 0))

        #on gère les messages reçus
        message_hist = clientthread.message_hist
        pygame_simple.blit_text(window, message_hist, (200, 500))

        #on affiche le choix des actions
        if clientthread.action != {}:
            actions= pygame_simple.transform_actions(clientthread.action)
            pygame_simple.blit_text(window, actions, (300, 320))
            choice = pygame_simple.choose_actions_pygame()
            clientthread.choice = choice

        #print(clientthread.board_state)
        #on affiche les maisons et les pions sur chaque case
        # try :
        #if clientthread.board_state[-1] != {}:
        #     print(clientthread.board_state)
        if clientthread.board_state != {}:
            pygame_simple.blit_images_on_board(window,clientthread.board_state)
        # except :
        #     print("pas de dico là")
        # #on met à jour la fenêtre
        pygame.display.update()