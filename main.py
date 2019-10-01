from board import Board
import square
import json
from player import Player
import os
import glob

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
            new_game()
        elif choice == 2:
            load_game()

    except Exception as e:
        #print(e)
        print("Vous devez choisir 1 ou 2")
        launch_game()


def new_game():
    board = Board(board_choice())
    print(board)



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
        return list_boards[int(choice) - 1]

    except Exception as e:
        print(e)
        print("Choisissez un plateau existant!")
        new_game()

new_game()