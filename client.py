import socket
from clientthread import Clientthread
import pygame
from interface_constantes import *

pygame.init()
message_hist = ["Bienvenue"]
def pygame_choice(dict):
    pass

def blit_text(surface, L, pos):
    word_height = 15
    x, y = pos
    font = pygame.font.Font(None, 14)
    for line in L[-4:]:
        to_blit = font.render(line, 11, (10,10,10))
        surface.blit(to_blit, (x, y))
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

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
        message_hist = clientthread.message_hist
        blit_text(window, message_hist, (200, 500))
        pygame.display.update()