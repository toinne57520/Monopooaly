import socket
import struct
import json
import pygame
from pygame.locals import *
from interface_constantes import *
pygame.init()
from time import sleep
import datetime

#
message_hist = ["Bienvenue"]
def bouton():
    pass

def pygame_choice(dict):
    pass

def deal_with_instruction():
    print("Que voulez vous faire?")
    actions_loaded = json.loads(sock.recv(4048).decode())
    print(actions_loaded)
    pygame_choice(actions_loaded)
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

def blit_text(surface, L, pos):
    word_height = 15
    x, y = pos
    font = pygame.font.Font(None, 14)
    for line in L[-4:]:
        to_blit = font.render(line, 11, (10,10,10))
        surface.blit(to_blit, (x, y))
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.



def deal_with_message():
    message = sock.recv(1024).decode()
    message_hist.append(message)
    for i in range(2):
        window = pygame.display.set_mode((window_dimension, window_dimension))
        background = pygame.image.load(background_homepage).convert()
        window.blit(background, (0, 0))
        blit_text(window, message_hist, (200,500))
        pygame.display.update()
    return

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
            message_hist.append("C'est à vous de jouer")
            message_received = 0
            while message_received != "stop":

                message_received = sock.recv(1024).decode()

                if message_received == "action":
                    deal_with_instruction()

                if message_received =="message":
                    deal_with_message()


                if message_received =="etat":
                    pass
                    #deal_with_etat()

            print("C'est la fin de votre tour")
            message_hist.append("C'est la fin de votre tour")




        turn_status = 0