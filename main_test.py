from board import Board
import json
import square
from player import Player
import os
import glob
import socket
from server import Server
from time import sleep
import struct
#

#game = Board('data.json')
#joueur = Player('Antoine',game) #rajouter exception pour que les deux joueurs n'aient pas la meme position
#joueur.throw_dice()

#print(joueur.position)
#print(joueur.money)

def launch_game():
    try:
        choice = int(input("""Bienvenue dans le Monopooaly! Que souhaitez-vous faire?
          1) Démarrer une nouvelle partie
          2) Charger une partie existante
           (taper 1 ou 2)"""))
        assert (choice == 1 or choice == 2)

        if choice == 1:
            board = new_game()
        elif choice == 2:
            #load_game()
            print("to do") #reflechir à la manière d'enregistrer (dans la méthode de gestion d'un tour

    except Exception as e:
        #print(e)
        print("Vous devez choisir 1 ou 2")
        launch_game()

    return board


def new_game():
    board = Board(board_choice())
    return board



def board_choice():
    path = os.path.join(os.getcwd(), "Boards/*.json")
    list_boards = glob.glob(path)

    print("Voici la liste des plateaux disponibles: ")

    for index, board in enumerate(list_boards):
        print(str(index + 1) + " : " + str(os.path.basename(board)))

    try:
        choice = input("Quel plateau souhaitez-vous utiliser? " 
              "(Taper un nombre entre 1 et " + str(len(list_boards)) + ")")
        assert (1 <= int(choice) <= len(list_boards))
        print("Vous jouez sur le plateau " + str(os.path.basename(list_boards[int(choice) - 1])) + "!")
        return list_boards[int(choice) - 1]

    except Exception as e:
        print(e)
        print("Choisissez un plateau existant!")
        new_game()


def player_choice():
    try:
        nb_players = input("Combien de joueurs participent à la partie?")
        assert (1 <= int(nb_players) <= 4)
        players_list = [input("Quel est le nom du joueur " + str(i + 1) + "?") for i in range(int(nb_players))]
        return players_list

    except:
        print("Le nombre de joueurs doit être un entier entre 1 et 4")
        player_choice()

def standard_turn(player):
    #ajout des fonctions possibles pour un joueur
    player.throw_dice()

early_action = { 1 : 'Lancer les dés' , 2 : 'Construire une maison', 3 : 'Hypothéquer'}
end_action = {1 : 'Terminer mon tour'}


if __name__ == '__main__':
    board = new_game()
    print("On lance la partie!")
    players_turn = 0

    # lancement du serveur
    server = Server(11100,board)
    server.start()

    # on attend un peu
    while len(server.client_list) != 2:
        sleep(1)

    for client in server.client_list :
        client.send("Bienvenue dans le Monopooaly!".encode())
        player_name = client.recv(1024).decode()
        player = Player(player_name,board,client)

    starting_player = 0

    while True:
        player_active = board.players[(starting_player + 1) % 2]
        player_inactive = board.players[(starting_player % 2)]
        player_inactive.sock.send(struct.pack("?", False))
        player_active.sock.send(struct.pack("?", True))

        action = True
        while action!= False :
            action = player_active.choose_actions(early_action)

            if action == "Lancer les dés":
                advance = board.throw_dice(player_active)
                board.change_position(player_active,advance)
                board.square_list[player_active.position].str(player_active)
                action = player_active.choose_actions(board.square_list[player_active.position].get_actions(player_active))
                print(action)

            if action == "Hypothéquer":
                print(action)

            if action == "Tirer une carte chance":
                print(action)
                sleep(1)
                action = board.square_list[player_active.position].get_impact(player_active,board)
                if action =="new_pos":
                    action = player_active.choose_actions(board.square_list[player_active.position].get_actions(player_active))

            if action == "Construire une maison":
                print(action)

            if action == "Payer le loyer":
                print(action)
                sleep(1)
                board.square_list[player_active.position].pay_rent(player_active)
                action = player_active.choose_actions(end_action)

            if action == "Acheter le terrain":
                print(action)
                sleep(1)
                board.square_list[player_active.position].buy_land(player_active)
                action = player_active.choose_actions(end_action)


            if action == "Terminer mon tour":
                print(action)
                sleep(1)
                player_active.sock.send("stop".encode())
                action = False

            #gérer le cas de terminer son tour après avoir lancé les dés

        starting_player += 1




