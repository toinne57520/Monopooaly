from board import Board
import json
from square import Land
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
        nb_players = input("Combien de joueurs participent à la partie??")
        assert (1 <= int(nb_players) <= 4)
        players_list = [input("Quel est le nom du joueur " + str(i + 1) + "?") for i in range(int(nb_players))]
        return players_list

    except:
        print("Le nombre de joueurs doit être un entier entre 1 et 4")
        player_choice()

def standard_turn(player):
    #ajout des fonctions possibles pour un joueur
    player.throw_dice()

early_action = { 0 : 'Lancer les dés' , 1 : 'Construire une maison', 2 : 'Hypothéquer', 3 : 'Déshypothéquer'}
end_action = {0 : 'Terminer mon tour', 1 : 'Sauvegarder la partie'}


if __name__ == '__main__':
    board = new_game()
    print("On lance la partie!")
    players_turn = 0

    # lancement du serveur
    server = Server(11100,board)
    server.start()

    print("A combien allez vous jouer ?")
    numberplayer = input("> ")
    while numberplayer[0] not in ['2','3','4'] :
        print("Vous devez indiquer un nombre de joueurs entre 2 et 4")
        numberplayer = input("> ")

    print("Vous pouvez à présent lancer " + numberplayer + " clients" )


    while len(server.client_list) < int(numberplayer[0]):
        sleep(0.5)

    for client in server.client_list :
        client.send("Bienvenue dans le Monopooaly!".encode())
        player_name = client.recv(1024).decode()
        player = Player(player_name,board,client)
        player.piece = "piece_" + str(server.client_list.index(client) + 1)

    if True : #gérer le sauvegarde et le chargement des parties
        pass

    starting_player = 0
    for square in board.square_list[1:2]:
        if type(square) == Land:
            square.owner = board.players[starting_player]
            board.players[starting_player].assets.append(square)
            square.status = True

    for square in board.square_list[3:4]:
        if type(square) == Land:
            square.owner = board.players[starting_player]
            board.players[starting_player].assets.append(square)
            square.status = True


    while True:
        player_active = board.players[(starting_player + 1) % 2]
        player_inactive = board.players[(starting_player % 2)]
        player_inactive.sock.send(struct.pack("?", False))
        player_active.sock.send(struct.pack("?", True))
        player_active.send_board()
        player_inactive.send_board()

        action = True
        while action!= False :
            action = player_active.choose_actions(board.build_starting_dict(player_active))

            if action == "Lancer les dés":
                advance = board.throw_dice(player_active)
                board.change_position(player_active,advance)
                board.square_list[player_active.position].str(player_active)
                player_active.send_board()
                player_inactive.send_board()
                action = player_active.choose_actions(board.square_list[player_active.position].get_actions(player_active))
                print(action)

            if action == "Hypothéquer":
                print(action)
                name_land_to_mortgage = player_active.choose_actions(board.get_morgageable_assets(player_active)[1])
                print(name_land_to_mortgage)
                if name_land_to_mortgage :
                    player_active.send_message(board.get_square_from_name(name_land_to_mortgage).to_mortgage())

            if action == "Déshypothéquer":
                print(action)
                name_land_to_clear_mortgage = player_active.choose_actions(board.get_inactive_assets(player_active)[1])
                print(name_land_to_clear_mortgage)
                if name_land_to_clear_mortgage :
                    player_active.send_message(board.get_square_from_name(name_land_to_clear_mortgage).to_clear_mortgage())


            if action == "Tirer une carte chance":
                print("on rentre dans tirer une carte chance")
                action = board.square_list[player_active.position].get_impact(player_active,board)
                if action =="new_pos":
                    action = player_active.choose_actions(board.square_list[player_active.position].get_actions(player_active))
                    player_active.send_board()
                    player_inactive.send_board()
                if action == "same_pos":
                    action = player_active.choose_actions(end_action)

            if action == "Construire une maison":
                print(action)
                if board.get_building_lands(player_active)[0]:
                    name_land_to_build = player_active.choose_actions(board.get_building_lands(player_active)[1])
                    square = board.get_square_from_name(name_land_to_build)
                    nbr_houses_to_build = player_active.choose_actions(square.get_dict_houses_to_build())
                    player_active.send_message(square.to_build(int(nbr_houses_to_build)))
                else :
                    player_active.send_message("Vous n'avez pas de terrain constructible")


            if action == "Payer la taxe":
                print("on rentre dans action: payer la taxe")
                missing_funds = board.square_list[player_active.position].pay_taxes(player_active)
                if missing_funds == 0:
                    action = player_active.choose_actions(end_action)
                else:
                    action = "Trouver des fonds"

            if action == "Payer le loyer":
                print(action)
                missing_funds = board.square_list[player_active.position].pay_rent(player_active)
                if missing_funds == 0:
                    action = player_active.choose_actions(end_action)
                else:
                    action = "Trouver des fonds"

            if action == "Sauvegarder la partie":
                print(action)


            if action == "Trouver des fonds":
                print(action, missing_funds)
                possible_actions = board.get_dict_funds(player_active)
                if len(possible_actions) > 0:
                    action = player_active.choose_actions(possible_actions)
                else:
                    action == "Gérer fin de partie"

            if action == "Acheter le terrain":
                print("on rentre dans action: acheter terrain")
                board.square_list[player_active.position].buy_land(player_active)
                action = player_active.choose_actions(end_action)

            if action == "Aller en prison":
                print(action)
                board.square_list[player_active.position].go_to_jail(player_active)
                action = player_active.choose_actions(end_action)

            if action == "Terminer mon tour":
                print(action)
                sleep(1)
                player_active.sock.send("stop".encode())
                player_inactive.sock.send("stop".encode())
                sleep(1)
                action = False

            if action == "Gérer fin de partie":



        starting_player += 1




