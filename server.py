from threading import Thread
import socket
from monopooaly import MonopooalyThread

#serveur utilise dans le corrige du TP3

class Server(Thread):

    def __init__(self, port, board):
        Thread.__init__(self)
        if not isinstance(port, int):
            raise TypeError("Le port doit etre un entier")

        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind(('localhost', port))
        self.__continuer = True
        self.board = board
        self.client_list = []

    def run(self):
        i = 0
        self.__sock.listen(1)  # on autorise une seule connexion en attente à la fois
        while self.__continuer:
            try:
                connexion, client = self.__sock.accept()
                self.client_list.append(connexion)
            except OSError:
                # se produit quand on coupe la socket
                pass
            except IOError as e:
                # a priori, il y a eu un probleme
                print(e)

        print("Arret du serveur")

    def stoplistening(self):
        self.__continuer = False
        if self.__sock:
            self.__sock.close()




