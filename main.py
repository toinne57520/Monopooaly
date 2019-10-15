from board import Board
#import square
import json
import square
from player import Player
import os
import glob

#game = Board('data.json')
#joueur = Player('Antoine',game) #rajouter exception pour que les deux joueurs n'aient pas la meme position.
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
    players = [Player(name, board) for name in player_choice()]
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


board = new_game()
print("On lance la partie!")
players_turn = 0

while len(board.players) > 1: #on enleve les joueurs qui perdent au fur et à mesure et on s'arrete quand il n'en reste qu'un?
    player = board.players[int(players_turn%len(board.players))]
    print("C'est le tour de " + str(player.name))
    standard_turn(player)
    players_turn += 1

#gestion de fin de tour à faire, comment quitter la partie, comment l'enregistrer??
