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
                square_list.append(square.Land(element["name"], element["position"],element["value"],element["color"], element["rent"], element["construction_price"]))

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

    def get_nb_lands_of_a_color(self, color):
        i=0
        for land in self.square_list :
                if land.color==color:
                   i+=1
        return i


    def throw_dice(self, player):
        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6) #quand on rajoutera les tours, mettre l'option double = rejouer
        advance = dice1 + dice2
        print(f"Vous avancez de {advance} cases.")
        self.change_position(player, advance)


    def change_position(self, advance, player):

        self.square_list[player.position].present_player.remove(player)  # on retire le player de sa case.

        quotient = (player.position + advance) // len(self.square_list)
        player.position = (player.position + advance) % len(self.square_list)

        if quotient>0 :
            player.money += quotient * 200
            return (f"Vous êtes passés par la case départ. Félicitations ! vous avez gagné {quotient*200} €")

        self.square_list[player.position].present_player.append(player) #on l'enregistre sur sa nouvelle case
        return self.square_list[player.position]


