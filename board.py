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

            else :
                print("Pas une catégorie connue")
        return square_list

    def add_player(self, player):
        self.players.append(player)

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
        advance = dice1 + dice2
        player.send_message(f"Vous avancez de {advance} cases.")
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
            if asset.color == color:
                i += 1
        return i

    def get_morgageable_assets(self, player):
        mortgageable_assets = {}
        i = 0
        affichage = []
        for index, element in enumerate(player.assets):
            if not element.mortgage and element.nb_houses == 0:
                mortgageable_assets[index] = element.name
                affichage.append(str(element.name) + " pour une valeur de " + str(element.value / 2) + "€.")
                i += 1
        player.send_message(f"Les terrains que vous pouvez hypothéquer sont {affichage}")
        return mortgageable_assets


    def get_inactive_assets(self, player):
        inactive_assets = {}
        i = 0
        affichage = []
        for index, element in enumerate(player.assets):
            if element.mortgage:
                inactive_assets[index] = element.name
                affichage.append(str(element.name) + " pour une valeur de " + str(element.value/2) + "€")
                i += 1
        player.send_message(f"Les terrains que vous pouvez déshypothéquer sont {affichage}")
        return inactive_assets

    def get_building_lands(self, player):
        """
               Cette méthode renvoie tous les terrains constructibles (c'est à dire avec la couleur complète) du joueur s'il en a.

               """
        building_lands = {}
        building_lands_color_price = []
        try:
            for index, element in enumerate(player.assets):
                # on compare le nombre de terrains de la couleur détenus par le joueur et le nombre de ces terrains sur le plateau
                if self.get_nb_assets_of_a_color(player, element.color) == self.get_nb_lands_of_a_color(
                        element.color) and element.color != "trainstation":
                    building_lands[str(index)] = element.name
                    building_lands_color_price.append([element.name, element.color, element.construction_price])
            assert len(building_lands) > 0
            # on affiche les terrains constructibles, leur couleur et leur prix de construction
            # affichage à améliorer
            player.send_message(f"Vous pouvez construire sur (et chaque maison coûte) {building_lands_color_price}")
            return True, building_lands
        except AssertionError:
            player.send_message(
                "Cela s'annonce compliqué, vous n'avez pas de terrains constructibles. Vous n'avez aucun quartier complet, repartez à l'aventure.")
            return False, False

    def get_built_lands(self, player):
        """
                Cette méthode renvoie tous les terrains sur lesquelles des maisons sont construites.
                """
        built_lands = {}
        built_lands_nb_houses_price = []
        try:
            for index, element in enumerate(player.assets):
                if element.nb_houses > 0:
                    built_lands[str(index)] = element.name
                    built_lands_nb_houses_price.append([element.name, element.nb_houses, element.construction_price / 2])
            assert len(built_lands) > 0
            # on affiche les terrains construits, leur nombre de maison et leur prix de revente
            # affichage à améliorer
            player.send_message(f"Vous pouvez revendre sur (et chaque maison rapporte) {built_lands_nb_houses_price}")
            return True, built_lands
        except AssertionError:
            player.send_message(
                "Cela s'annonce compliqué, vous n'avez pas de terrains construits. Vous n'avez aucune maison à revendre, ne vendez pas la peau de l'ours avant de l'avoir tué!")
            return False


    def get_square_from_name(self, name):
        for i in range(len(self.square_list)):
            if self.square_list[i].name == name:
                return self.square_list[i]
        return "Désolé, le nom saisi n'est pas dans la liste" #quand on appelle la fonction, voir comment gérer cette erreur


    def serialize_board(self):
        dictionnaire = {}
        dictionnaire["__class__"] = "Board"
        for element in self.square_list:
            dictionnaire[str(element.position)] = self.serialize_square(element)
        return dictionnaire

    def serialize_square(self, square):
        if isinstance(square, Land):
            return {"players": [square.present_player[i].name for i in range(len(square.present_player))],
                    "nb_houses": square.nb_houses}
        else:
            return {"players": [square.present_player[i].name for i in range(len(square.present_player))],
                    "nb_houses": 0}

