import socket
from server import Server
from time import sleep
import struct
import pickle
import player

if __name__ == '__main__':
    # connexion au server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 11100))

    # Welcome message
    welcome_message = sock.recv(1024).decode()
    if welcome_message != u"Bienvenue dans le Monopooaly! Que souhaitez-vous faire?":
        raise ValueError("Erreur protocole: attendu welcome message (cote client)")
    print(welcome_message)
    print("Quel est votre nom de joueur ?")
    name_player = input("> ")
    sock.send(name_player.encode())

    #if commande != u"HLO":
        #raise ValueError("Erreur protocole: attendu HLO (cote client)")
    #while true
    while True:

        #turn_status = bytes()
        #print(turn_status.decode())
        #turn_status += sock.recv(1024)
        #print(turn_status.decode())

        buf = bytes()
        while len(buf) < 1:
            buf += sock.recv(1)
        turn_status = struct.unpack('?', buf[:1])[0]
        print(turn_status)


        if not turn_status:
            print("Ce n'est pas à vous de jouer")

        if turn_status:
            print("C'est à vous de jouer")
            #receive the designator of the player
            buf = bytes()
            while len(buf) < 4:
                buf += sock.recv(8)
            player_number = struct.unpack('!i', buf[:4])[0]

            #receive the board from the server and start turn
            data = sock.recv(4096)
            data.seek(0)
            try :
                board = pickle.loads(data)
            except :
                print(data)
                print("il y a bien une erreur")

            print(board)
            player = board.players[player_number]
            player.throw_dice()

            # Pickle the updated object and send it to the server
            data_update = pickle.dumps(board)
            sock.send(data_update)




