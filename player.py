from square import Land, Luck, Tax
import json
import random
from time import sleep
#

class Player :


    def __init__(self,name,board,sock):
        self.name = name
        self.money = 200
        self.position = 0
        self.assets = []
        self.board = board #le plateau sur lequel le joueur joue
        self.board.square_list[self.position].present_player.append(self) #on place le joueur sur la case départ
        board.add_player(self)
        self.sock = sock
        self.in_jail = 0


    def choose_actions(self,dict):
        if len(dict) == 0:
            return
        sleep(0.5)
        self.sock.send("action".encode())
        sleep(0.5)
        data_string = json.dumps(dict).encode()
        print(data_string)
        self.sock.send(data_string)
        data_loaded = int(self.sock.recv(1024).decode())
        while data_loaded not in [x for x in list(dict.keys())]:
            self.sock.send("again".encode())
            data_loaded = int(self.sock.recv(1024).decode())

        self.sock.send("ok".encode())
        print("on est dans choose actions ",dict[data_loaded])
        return(dict[data_loaded])

    def send_board(self):
        sleep(1)
        self.sock.send("board".encode())
        sleep(1)
        board_dict = self.board.serialize_board()
        data_string = json.dumps(board_dict).encode()
        self.sock.send(data_string)
        return ()


    def send_message(self,message):
        sleep(0.5)
        self.sock.send("message".encode())
        sleep(0.5)
        self.sock.send(message.encode())
        return ()


    def wait_for_your_turn(self,sock):
        sock.send("Ce n'est pas à vous de jouer".encode())


