#import pygame
from threading import Thread
from interface_constantes import *
from time import sleep
from pygame.locals import *
import socket
import struct
import json

class Clientthread(Thread):


    def __init__(self,sock):
        Thread.__init__(self)
        self.sock = sock
        self.action = {}
        self.message_hist = ["Bienvenue","Vous etes sur la case départ et vous possedez 200€"]
        self.board_state = {}


    def deal_with_instruction(self):
        print("Que voulez vous faire?")
        actions_loaded = json.loads(self.sock.recv(4048).decode())
        print(actions_loaded)
        self.action = actions_loaded
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
            self.sock.send(action.encode())
            validation_message = self.sock.recv(1024).decode()
        return

    def deal_with_board(self):
        board_loaded = json.loads(self.sock.recv(4048).decode())
        self.board_state = board_loaded
        return

    def deal_with_message(self):
        message = self.sock.recv(1024).decode()
        self.message_hist.append(message)
        return


    def run(self):
        while True:
            buf = bytes()
            while len(buf) < 1:
                buf += self.sock.recv(1)
            turn_status = struct.unpack('?', buf[:1])[0]

            if not turn_status:
                self.message_hist.append("Ce n'est pas à vous de jouer")
                message_received = 0
                if message_received == "board":
                    self.deal_with_board()

            if turn_status:
                self.message_hist.append("C'est à vous de jouer")
                message_received = 0
                while message_received != "stop":

                    message_received = self.sock.recv(1024).decode()

                    if message_received == "action":
                        self.deal_with_instruction()

                    if message_received == "message":
                        self.deal_with_message()

                    if message_received == "board":
                        self.deal_with_board()

                self.message_hist.append("C'est la fin de votre tour")

            turn_status = 0