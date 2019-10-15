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
        self.board.square_list[self.position].present_player.append(self.name) #on place le joueur sur la case départ
        board.add_player(self)
        self.sock = sock


    def __repr__(self):
        pass

    def choose_actions(self,dict):
        sleep(1)
        self.sock.send("action".encode())
        sleep(1)
        data_string = json.dumps(dict).encode()
        self.sock.send(data_string)
        data_loaded = int(self.sock.recv(1024).decode())
        while data_loaded not in [x for x in list(dict.keys())]:
            self.sock.send("again".encode())
            data_loaded = int(self.sock.recv(1024).decode())

        self.sock.send("ok".encode())
        print(dict[data_loaded])
        return(dict[data_loaded])



    def send_message(self,message):
        sleep(1)
        self.sock.send("message".encode())
        sleep(1)
        self.sock.send(message.encode())
        return ()

    #def choose_clear_mortgage(self,dict,sock):
     #   pass

    #def choose_land_to_build(self,dict,sock):
    #    pass

    #def choose_mortgage(self,dict):
     #   pass

    #def choose_land_to_sell(self,dict,sock):
      #  pass

    def wait_for_your_turn(self,sock):
        sock.send("Ce n'est pas à vous de jouer".encode())


