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
import random
#

#game = Board('Nouvelle_partie.json')
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
    chosen_board = board_choice()
    chosen_board_simplified = chosen_board.split("/")[-1]
    board = Board(chosen_board)
    print(chosen_board_simplified)
    return board, chosen_board_simplified

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



def standard_turn(player):
    #ajout des fonctions possibles pour un joueur
    player.throw_dice()

early_action = { 0 : 'Lancer les dés' , 1 : 'Construire une maison', 2 : 'Hypothéquer', 3 : 'Déshypothéquer'}
end_action = {0 : 'Terminer mon tour'}

def mid_game_launch(board):
    list_player_1 = [1, 3, 8, 15, 16, 18, 19, 23, 37]  # joueur 1 a violet, orange
    list_houses_1 = [1, 3, 16, 18, 19]
    list_player_2 = [5, 6, 11, 13, 14, 25, 29, 31, 32, 34]  # joueur 2 a violet clair, vert
    list_houses_2 = [11, 13, 14, 31, 32, 34]
    board.players[0].money = 630
    board.players[1].money = 450

    for i in list_player_1:
        square = board.square_list[i]
        square.owner = board.players[0]
        board.players[0].assets.append(square)
        square.status = True

    for i in list_player_2:
        square = board.square_list[i]
        square.owner = board.players[1]
        board.players[1].assets.append(square)
        square.status = True

    for i in list_houses_1:
        board.square_list[i].nb_houses += random.randint(0, 5)

    for i in list_houses_2:
        board.square_list[i].nb_houses += random.randint(0, 5)

    board.change_position(board.players[0], int(random.randint(0, 40)))
    board.change_position(board.players[1], int(random.randint(0, 40)))

    return board

def end_game_launch(board):
    list_player_1 = [1, 3, 8, 15, 16, 18, 19, 23,31, 32, 34, 37]  # joueur 1 a violet, orange et vert
    list_houses_1 = [1, 3, 16, 18, 19, 31, 32, 34]
    list_player_2 = [11, 13, 14]  # joueur 2 a violet clair
    list_houses_2 = [11, 13, 14]
    board.players[0].money = 630
    board.players[1].money = 100
    for i in list_player_1:
        square = board.square_list[i]
        square.owner = board.players[0]
        board.players[0].assets.append(square)
        square.status = True

    for i in list_player_2:
        square = board.square_list[i]
        square.owner = board.players[1]
        board.players[1].assets.append(square)
        square.status = True

    for i in list_houses_1:
        board.square_list[i].nb_houses += random.randint(0, 5)

    for i in list_houses_2:
        board.square_list[i].nb_houses += random.randint(0, 5)

    board.change_position(board.players[0], int(random.randint(0, 40)))
    board.change_position(board.players[1], int(random.randint(0, 40)))
    return board

if __name__ == '__main__':
    boards = new_game()
    board = boards[0]
    board_simplified = boards[1]
    print("On lance la partie!")
    players_turn = 0

    # lancement du serveur
    server = Server(11100,board)
    server.start()

    if board_simplified == 'Partie_en_cours.json':
        numberplayer = "2"
        print("La partie en cours est uniquement simulée pour 2 joueurs")
        print("Vous pouvez à présent lancer " + numberplayer + " clients")


    elif board_simplified == 'Fin_de_partie.json':
        numberplayer = "2"
        print("La fin de partie est uniquement simulée pour 2 joueurs")
        print("Vous pouvez à présent lancer " + numberplayer + " clients")

    else:
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

    if board_simplified == 'Partie_en_cours.json':
        board = mid_game_launch(board)

    elif board_simplified == 'Fin_de_partie.json':
        board = end_game_launch(board)

    starting_player = 0
    party = True

    while party:
        player_active = board.players[starting_player % len(board.players)]
        player_inactive = board.players.copy()
        player_inactive.remove(player_active)
        player_active.sock.send(struct.pack("?", True))
        player_active.send_board()
        for players in player_inactive :
            players.sock.send(struct.pack("?", False))
            players.send_board()

        action = True
        while action!= False :
            action = player_active.choose_actions(board.build_starting_dict(player_active))

            if action == "Lancer les dés":
                advance = board.throw_dice(player_active)
                board.change_position(player_active,advance)
                board.square_list[player_active.position].str(player_active)
                player_active.send_board()
                for players in player_inactive :
                    players.send_board()
                action = player_active.choose_actions(board.square_list[player_active.position].get_actions(player_active))



            if action == "Déshypothéquer":
                name_land_to_clear_mortgage = player_active.choose_actions(board.get_inactive_assets(player_active)[1])
                if name_land_to_clear_mortgage != "Ne pas déshypothéquer":
                    message = board.get_square_from_name(name_land_to_clear_mortgage).to_clear_mortgage()
                    player_active.send_message(message)
                    player_active.send_board()
                    for players in player_inactive:
                        players.send_message(message)
                        players.send_board()


            if action == "Tirer une carte chance":
                action = board.square_list[player_active.position].get_impact(player_active,board)
                if action =="new_pos":
                    action = player_active.choose_actions(board.square_list[player_active.position].get_actions(player_active))
                    player_active.send_board()
                    for players in player_inactive:
                        players.send_board()
                if action == "same_pos":
                    action = player_active.choose_actions(end_action)

            if action == "Construire une maison":
                if board.get_building_lands(player_active)[0]:
                    name_land_to_build = player_active.choose_actions(board.get_building_lands(player_active)[1])
                    if name_land_to_build != "Ne pas construire":
                        square = board.get_square_from_name(name_land_to_build)
                        nbr_houses_to_build = player_active.choose_actions(square.get_dict_houses_to_build())
                        message = square.to_build(int(nbr_houses_to_build[0]))
                        player_active.send_message(message)
                        player_active.send_board()
                        for players in player_inactive:
                            players.send_message(message)
                            players.send_board()
                else :
                    player_active.send_message("Vous n'avez pas de terrain constructible")


            if action == "Payer la taxe":
                missing_funds = board.square_list[player_active.position].pay_taxes(player_active, player_inactive)
                if missing_funds == 0:
                    action = player_active.choose_actions(end_action)
                else:
                    action = "Trouver des fonds"

            if action == "Payer le loyer":
                missing_funds = board.square_list[player_active.position].pay_rent(player_active, board)
                if missing_funds == 0:
                    action = player_active.choose_actions(end_action)
                else:
                    action = "Trouver des fonds"

            if action == "Trouver des fonds":
                possible_actions = board.get_dict_funds(player_active)
                if len(possible_actions) > 0:
                    action = player_active.choose_actions(possible_actions)
                    player_active.in_dept = True
                else:
                    action = "Gérer défaite joueur"

            if action == "Hypothéquer":
                name_land_to_mortgage = player_active.choose_actions(board.get_morgageable_assets(player_active)[1])
                if name_land_to_mortgage != "Ne pas hypothéquer":
                        message = board.get_square_from_name(name_land_to_mortgage).to_mortgage()
                        player_active.send_message(message)
                        player_active.send_board()
                        for players in player_inactive:
                            players.send_message(message)
                            players.send_board()

            if action == "Acheter le terrain":
                message = board.square_list[player_active.position].buy_land(player_active, board)
                action = player_active.choose_actions(end_action)
                player_active.send_board()
                for players in player_inactive:
                    players.send_board()

            if action == "Aller en prison":
                board.square_list[player_active.position].go_to_jail(player_active, board)
                player_active.send_board()
                for players in player_inactive:
                    players.send_board()
                action = player_active.choose_actions(end_action)



            if action == "Vendre une maison":
                name_land_to_sell = player_active.choose_actions(board.get_built_lands(player_active)[1])
                square = board.get_square_from_name(name_land_to_sell)
                nbr_houses_to_sell = player_active.choose_actions(square.get_dict_houses_to_sell())
                message = square.to_sell(int(nbr_houses_to_sell[0]))
                for players in board.players:
                    players.send_message(message)
                player_active.send_board()
                for players in player_inactive:
                    players.send_board()

            if action == "Terminer mon tour":
                sleep(0.5)
                player_active.sock.send("stop".encode())
                for players in player_inactive:
                    players.sock.send("stop".encode())
                sleep(0.5)
                action = False

            if action == "Gérer défaite joueur":
                board.remove_loser(player_active)
                if len(board.players) == 1:
                    action = "Gérer fin de partie"

            if action == "Gérer fin de partie":
                board.players[0].send_message("Félicitations! Vous êtes le grand gagnant du Monopooaly!!")
                board.players[0].send_break()
                party = False
                action = False

        starting_player += 1




