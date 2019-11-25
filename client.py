import socket
import pygame
import pygame_simple
from clientthread import Clientthread
from interface_constantes import *

pygame.init()



if __name__ == '__main__':
    # connexion au server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'
    port = 8080
    sock.connect((host,port))
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
    window = pygame.display.set_mode((window_dimension+ colonne, window_dimension))
    background = pygame.image.load(background_homepage).convert()
    window.blit(background, (0, 0))
    pygame.display.flip()

    while True:
        window = pygame.display.set_mode((window_dimension + colonne, window_dimension))
        window.fill((245, 255, 248))
        background = pygame.image.load(background_homepage).convert()
        window.blit(background, (0, 0))

        #on gère les messages reçus
        message_hist = clientthread.message_hist
        pygame_simple.blit_text(window, message_hist, (200, 560))

        #on affiche le choix des actions
        if clientthread.action != {}:
            actions= pygame_simple.transform_actions(clientthread.action)
            pygame_simple.blit_actions(window, actions, (300, 320))
            choice = pygame_simple.choose_actions_pygame()
            clientthread.choice = choice

        #print(clientthread.board_state)
        #on affiche les maisons et les pions sur chaque case
        # try :
        #if clientthread.board_state[-1] != {}:
        #     print(clientthread.board_state)
        if clientthread.board_state != {}:
            pygame_simple.blit_images_on_board(window,clientthread.board_state)
            coord = pygame_simple.blit_infos_in_column(window,clientthread.board_state)
            for player in coord:
                if player[0]==name_player and clientthread.turn_status==True:
                    x = player[1]
                    y = player[2]
                    pygame_simple.blit_dice(window,x,y)


            #status = clientthread.turn_status
            #name_player
        # except :
        #     print("pas de dico là")
        # #on met à jour la fenêtre
        pygame.display.update()