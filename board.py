import json
import square
import random
from square import Land
#
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

            elif element["type"] == "Jail":
                square_list.append(square.Jail(element["name"], element["position"]))

            elif element["type"] == "GoJail":
                square_list.append(square.Go_Jail(element["name"], element["position"]))

            else :
                print("Pas une catégorie connue")
        return square_list

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def remove_loser(self, player):
        for asset in player.assets:
            asset.owner = ""
            asset.status = False
            asset.nb_houses = 0
            asset.mortgage = False
        self.remove_player(player)
        player.send_message(f"Vous n'avez plus les moyens de payer vos dettes.. Vous avez perdu! Retentez votre chance une prochaine fois..")
        player.send_break()

    def build_starting_dict(self,player):

        if player.in_dept :
            player.in_dept = False
            early_action = (self.square_list[player.position].get_actions(player))
        else :
            early_action = {0: 'Lancer les dés'}
            i = 0
            if self.get_building_lands(player)[0]:
                i+=1
                early_action[int(i)] = 'Construire une maison'

            if self.get_morgageable_assets(player)[0]:
                i += 1
                early_action[int(i)] = 'Hypothéquer'

            if self.get_inactive_assets(player)[0]:
                i += 1
                early_action[int(i)] = 'Déshypothéquer'

        return early_action


    def get_nb_lands_of_a_color(self, color):
        i=0
        for land in self.square_list :
            if type(land) == square.Land:
                if land.color==color:
                   i+=1
        return i


    def throw_dice(self, player):
        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6) #quand on rajoutera les tours, mettre l'option double = rejouer

        if player.in_jail == 0:
            advance = dice1 + dice2
            player.send_message(f"Vous avancez de {advance} cases.")
        elif player.in_jail == 1:
            player.in_jail = 0
            advance = dice1 + dice2
            player.send_message(f"Vous sortez de prison et avancez de {advance} cases.")
        else:
            if dice1 == dice2:
                advance = dice1 + dice2
                player.send_message(f"Vous sortez de prison et avancez de {advance} cases.")
            else:
                player.in_jail -= 1
                player.send_message(f"Pas de double pour ce tour..")
                advance = 0
        return advance


    def change_position(self, player, advance):

        self.square_list[player.position].present_player.remove(player)  # on retire le player de sa case.

        quotient = (player.position + advance) // len(self.square_list)
        player.position = (player.position + advance) % len(self.square_list)

        if quotient>0 :
            player.money += quotient * 200
            player.send_message(f"Vous êtes passés par la case départ. Félicitations ! vous avez gagné {quotient*200} €")

        self.square_list[player.position].present_player.append(player) #on l'enregistre sur sa nouvelle case
        return self.square_list[player.position]


    def get_nb_assets_of_a_color(self, player, color): #les passer en statique, hors classe? Bizarre parce que méthode de board sans faire appel à board
        i = 0
        for asset in player.assets:
            if asset.color == color and not asset.mortgage:
                i += 1
        return i

    def get_morgageable_assets(self, player):
        mortgageable_assets = {}
        i = 0
        for element in player.assets:
            print(self.get_built_lands(player)[2])
            if not element.mortgage and element.nb_houses == 0 and element.color not in [self.get_built_lands(player)[2][i][3] for i in range(len(self.get_built_lands(player)[2]))]:
                mortgageable_assets[int(i)] = element.name + " - " + str(element.value/2) + "€"
                #affichage.append(str(element.name) + " pour une valeur de " + str(element.value / 2) + "€.")
                i += 1
        if mortgageable_assets == {}:
            return False, False
        else:
            #player.send_message(f"Les terrains que vous pouvez hypothéquer sont {affichage}")
            mortgageable_assets[int(i)] = "Ne pas hypothéquer"
            return True, mortgageable_assets

    def get_dict_funds(self, player):
        possible_actions = {}
        if self.get_built_lands(player)[0] and self.get_morgageable_assets(player)[0]:
            possible_actions[0] = "Vendre une maison"
            possible_actions[1] = "Hypothéquer"
        else:
            if self.get_built_lands(player)[0]:
                possible_actions[0] = "Vendre une maison"
            elif self.get_morgageable_assets(player)[0]:
                possible_actions[0] = "Hypothéquer"
        return possible_actions

    def get_inactive_assets(self, player):
        inactive_assets = {}
        i = 0
        affichage = []
        for index, element in enumerate(player.assets):
            if element.mortgage:
                inactive_assets[int(i)] = element.name + " - " + str(element.value/2) + "€"
                affichage.append(str(element.name) + " pour une valeur de " + str(element.value/2) + "€")
                i += 1
        if affichage == []:
            return False, False
        else :
            #player.send_message(f"Les terrains que vous pouvez déshypothéquer sont {affichage}")
            inactive_assets[int(i)] = "Ne pas déshypothéquer"
            return True, inactive_assets, affichage

    def get_building_lands(self, player):
        """
               Cette méthode renvoie tous les terrains constructibles (c'est à dire avec la couleur complète) du joueur s'il en a.

               """
        building_lands = {}
        building_lands_color_price = []
        try:
            i = 0
            for element in player.assets:
                # on compare le nombre de terrains de la couleur détenus par le joueur et le nombre de ces terrains sur le plateau
                if self.get_nb_assets_of_a_color(player, element.color) == self.get_nb_lands_of_a_color(
                        element.color) and element.color != "trainstation":
                    building_lands[int(i)] = element.name + " - " + str(element.construction_price) + "€"
                    i+=1
                    building_lands_color_price.append([element.name, element.color, element.construction_price])
            assert len(building_lands) > 0
            # on affiche les terrains constructibles, leur couleur et leur prix de construction
            # affichage à améliorer
            #player.send_message(f"Vous pouvez construire sur (et chaque maison coûte) {building_lands_color_price}")
            building_lands[int(i)] = "Ne pas construire"
            return True, building_lands
        except AssertionError:
            return False, False

    def get_built_lands(self, player):
        """
                Cette méthode renvoie tous les terrains sur lesquelles des maisons sont construites.
                """
        built_lands = {}
        built_lands_nb_houses_price = []
        i = 0
        for element in player.assets:
            if element.nb_houses > 0:
                built_lands[int(i)] = element.name + " - " + str(element.construction_price/2) + "€"
                built_lands_nb_houses_price.append([element.name, element.nb_houses, element.construction_price / 2,element.color])
                i += 1
            # on affiche les terrains construits, leur nombre de maison et leur prix de revente
            # affichage à améliorer
        if len(built_lands) == 0 :
            return False, False, [[0,0,0,0],[0,0,0,0]]

        else :
            #player.send_message(f"Vous pouvez revendre sur (et chaque maison rapporte) {built_lands_nb_houses_price}")
            return True, built_lands, built_lands_nb_houses_price


    def get_square_from_name(self, name):
        name = name.split('-')[0][:-1]
        for i in range(len(self.square_list)):
            if self.square_list[i].name == name:
                return self.square_list[i]
        return "Désolé, le nom saisi n'est pas dans la liste" #quand on appelle la fonction, voir comment gérer cette erreur


    def serialize_board(self):
        dictionnaire = {}
        dictionnaire["__class__"] = "Board"
        dictionnaire["nb_players"] = len(self.players)
        for element in self.square_list:
            dictionnaire[str(element.position)] = self.serialize_square(element)
        for player in self.players:
            dictionnaire[player.name]={"assets": [[player.assets[i].name,player.assets[i].color,player.assets[i].mortgage] for i in range(len(player.assets))],
                                       "money":player.money,
                                       "piece":player.piece}
        return dictionnaire

    def serialize_square(self, square):
        if isinstance(square, Land):
            return {"players": [square.present_player[i].name for i in range(len(square.present_player))],
                    "pieces": [square.present_player[i].piece for i in range(len(square.present_player))],
                    "nb_houses": square.nb_houses}
        else:
            return {"players": [square.present_player[i].name for i in range(len(square.present_player))],
                    "pieces": [square.present_player[i].piece for i in range(len(square.present_player))],
                    "nb_houses": 0}

