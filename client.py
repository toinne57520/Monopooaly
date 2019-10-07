import socket
import struct
import json
import pygame
from pygame.locals import *
from interface_constantes import *
pygame.init()
import datetime

#
message_hist = []

def deal_with_instruction():
    print("Que voulez vous faire?")
    actions_loaded = json.loads(sock.recv(4048).decode())
    print(actions_loaded)
    #print(list(actions_loaded.keys()))
    validation_message = "again"
    while validation_message == "again":
        action = input("Que voulez vous faire ? (Choisissez un nombre dans la liste au dessus)")
        while True:
            try:
                int(action)
            except ValueError:
                # Not a valid number

                print("Vous devez entrer un nombre entier")
                action = input("Que voulez vous faire ? (Choisissez dans la liste au dessus)")
            else:
                # No error; stop the loop
                break
        sock.send(action.encode())
        validation_message = sock.recv(1024).decode()
    return


def deal_with_message():
    message = sock.recv(1024).decode()
    message_hist.append(message)
    print(message)
    print(message_hist)
    window = pygame.display.set_mode((window_dimension, window_dimension))
    background = pygame.image.load(background_homepage).convert()
    window.blit(background, (0, 0))
    font = pygame.font.Font(None, 13)
    name = font.render(message, 11, (10, 10, 10))
    name_x = (7) * square_dimension
    name_y = 7 * square_dimension
    window.blit(name, (name_x, name_y))
    print ("boucle de la fenetre")
    pygame.display.flip()
    if message_hist[-1]!= message_hist[-2]:
        pygame.display.flip()






if __name__ == '__main__':
    while True :
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
        print("Vous etes sur la case départ et vous possedez 200€")

        while True:
            buf = bytes()
            while len(buf) < 1:
                buf += sock.recv(1)
            turn_status = struct.unpack('?', buf[:1])[0]

            if not turn_status:
                print("Ce n'est pas à vous de jouer")


            if turn_status:
                print("C'est à vous de jouer")
                message_received = 0
                while message_received != "stop":

                    message_received = sock.recv(1024).decode()

                    if message_received == "action":
                        deal_with_instruction()

                    if message_received =="message":
                        deal_with_message()
                        print(datetime.time)


                print("C'est la fin de votre tour")




            turn_status = 0