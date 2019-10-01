import json
import random
import player
#import main

class Square:

    def __init__(self,name,position):
        self.name = name
        self.position = position
        self.present_player = []

    def __repr__(self):
        return("Vous êtes tombés sur la case départ")


class Land(Square):

    """
    Cette classe représente les cases du Monopoly qui sont des terrains, habités ou non, et les gares.
    Elle hérite de la classe Square et est définie par :
    son nom - name
    sa valeur - value
    sa couleur - color
    sa position - position
    ses loyers - rent
    son statut - true si habité, false sinon
    """

    def __init__(self, name, position, value, color, rent):
        Square.__init__(self,name,position)
        self.value = value
        self.color = color
        self.rent = rent
        self.owner = ""
        self.status = False
        self.nb_houses = 0
        self.mortage = False    #Vrai si le terrain est hypothéqué, faux sinon

    def __repr__(self):
        if self.status :
            if self.owner == self.present_player[-1]:
                return(f" La case est {self.name}, c'est chez vous.")
            else:
                return (f"Cette case est {self.name}, détenue par le joueur {self.owner.name}. Il y a {self.nb_houses} maisons contruites." 
                        f"Le loyer actuel est de {self.rent[self.nb_houses]} €")

        else :
            return (f"Cette case est libre ! C'est {self.name} de la couleur {self.color}. "
                    f"Elle coûte {self.value} €.")#voir plus tard pour le cout des maisons


class Luck(Square):

    def __init__(self, name, position):
        Square.__init__(self,name,position)
        with open("impact_luck.json") as impact_luck :
            self.impact_list = json.load(impact_luck)["dependencies"]
            self.nbre = len(self.impact_list)

        #définir méthode et voir comment gérer les impacts
        # voir méthode random qui pioche dans une liste d'impact

    def __repr__(self):
        return("Vous êtes tombés sur une carte chance !")

    def get_impact(self,player):
        luck_impact = random.randint(1,self.nbre)
        name = self.impact_list[1]["name"]
        description = self.impact_list[1]["description"]
        code = self.impact_list[1]["code"]
        print(name)
        print(description)
        if code[0] == "G":
            player.money += int(code[1:])
            print(f"Vous avez à présent {player.money}€")
        elif code[0] == "P":
            player.money -= int(code[1:])
            print(f"Vous avez à présent {player.money}€")
        elif code[0] == "A":
            player.change_position(int(code[1:]))
            print(player.board.square_list[player.position])
        elif code[0] == "R":
            player.change_position(-int(code[1:]))
            print(player.board.square_list[player.position])


class Tax(Square):

    def __init__(self, name, position, amount):
        Square.__init__(self, name, position)
        self.amount = amount

    def __repr__(self):
            return (f"C'est une case de taxe ... Montant à payer : {self.amount}")


