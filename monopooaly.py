from threading import Thread
import socket
import struct
import random
from board import Board
from player import Player
from time import sleep
import pickle
import threading

class MonopooalyThread(Thread):
    nbr_player = 0
    board = 0
    server = 0
    def __init__(self, sock,board,server):
        Thread.__init__(self)
        if not isinstance(sock, socket.socket) or sock is None:
            raise TypeError("Necessite une vraie socket")
        self.__socket = sock
        MonopooalyThread.board = board
        MonopooalyThread.nbr_player += 1
        MonopooalyThread.server = server

    def start_turn_active(self,player_number):
        print("ca rentre_actif")


        #self.__socket.send("Y".encode())
        self.__socket.send(struct.pack("?", True))
        self.__socket.send(struct.pack("!i", player_number))

        # Pickle the object and send it to the client
        data_string = pickle.dumps(MonopooalyThread.board)
        self.__socket.send(data_string)

        #receive the updated board
        data = self.__socket.recv(4096)
        data.seek(0)
        new_board = pickle.loads(data)
        MonopooalyThread.board = new_board

    def start_turn_passive(self,player_number):
        print("ca rentre_passif")
        #self.__socket.send("N".encode())
        self.__socket.send(struct.pack("?", False))

    def run(self):
        print("Just connected")

        board = MonopooalyThread.board
        # implementation du protocole
        #on boucle tant que le nombre de joueurs n'est pas atteint, a rajouter
        self.__socket.send("Bienvenue dans le Monopooaly! Que souhaitez-vous faire?".encode())
        name_player = self.__socket.recv(1024).decode()
        print(name_player)
        player = Player(name_player,board)
        board.add_player(player)
        print(board.players)
        print(MonopooalyThread.nbr_player)


        while MonopooalyThread.nbr_player !=2:
            sleep(1000)
            print("test")
        i=0
        starting_player = 0
        while True:
            print(f"Début du tour {i}")
            print(MonopooalyThread.server.client_list)

            # lancement des joueurs passifs
            for i in range(len(MonopooalyThread.server.client_list)):
                if i != starting_player:
                    client_passive = MonopooalyThread.server.client_list[i]
                    client_passive.start_turn_passive(i)

            #lancement du joueur actif
            client_active = MonopooalyThread.server.client_list[starting_player]
            client_active.start_turn_active(starting_player)



            starting_player = (starting_player + 1) % 2
            i+=1















        """if self.nbr_player == starting_player:
            print("ca rentre")
            print(self.nbr_player)
            variable = player
            # Pickle the object and send it to the server
            data_string = pickle.dumps(variable)

            self.__socket.send("yourturn".encode())

            self.__socket.send(data_string)

        else:
            print("ca rentre2")
            self.__socket.send("notyourturn".encode())"""




        #starting_player = abs(starting_player - 1)







