#import main_test
from board import Board
import json
from square import Land

board = Board('Boards/data.json')
square = board.square_list[0]

def serialize_board(obj):

    if isinstance(obj, Board):
        dictionnaire = {}
        dictionnaire["__class__"] =  "Board"
        for element in board.square_list:
               dictionnaire[element.position] = serialize_square(element)
        return dictionnaire
    #raise TypeError(repr(obj) + " n'est pas sérialisable !")

def serialize_square(square):
    if isinstance(square, Land):
        return {"players": square.present_player,
                "nb_houses": square.nb_houses}
    else:
        return {"players": square.present_player,
                "nb_houses": 0}



#with open("MonPlateau.json", "w", encoding="utf-8") as fichier:
#json.dumps(board, default=serialiseur_perso)

#print(serialize_board(board))
#print(board)