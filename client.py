import socket
import struct
import json
#

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
                print
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
    print(message)
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
            message_received = 0
            while message_received != "stop":

                message_received = sock.recv(1024).decode()

                if message_received == "action":
                    deal_with_instruction()

                if message_received =="message":
                    deal_with_message()

            print("C'est la fin de votre tour")



        turn_status = 0