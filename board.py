import json
import square


class Board :

    def __init__(self,json_file):
        self.square_list = self.build_board(json_file)
        self.players = []

    def build_board(self,json_file):
        with open(json_file) as data :
            squares = json.load(data)["dependencies"]
        square_list = []
        for element in squares :
            #rajouter gestion de l'erreur pour voir si la case n'appartient pas aux bonnes catégories.
            if element["type"] == "Land":
                square_list.append(square.Land(element["name"], element["position"],element["value"],element["color"], element["rent"]))

            elif element["type"] == "Luck":
                square_list.append(square.Luck(element["name"], element["position"]))

            elif element["type"] == "Square":
                square_list.append(square.Square(element["name"], element["position"]))

            elif element["type"] == "Tax":
                square_list.append(square.Tax(element["name"], element["position"], element["amount"]))

            else :
                print("Pas une catégorie connue")
        return square_list

    def add_player(self, player):
        self.players.append(player)


