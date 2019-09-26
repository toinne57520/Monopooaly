import json

class Square:

    def __init__(self,name,position):
        self.name = name
        self.position = position
        self.present_player = []


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

    def __repr__(self):
        if self.status :
            return (f"Coup dur ! Cette case est {self.name}, détenue par le joueur {self.owner}. Il y a {self.nb_houses}, "
                    f"vous devez donc payer {self.rent[self.nb_houses]} €")
        else :
            return (f"Quelle aubaine ! Cette case est libre ! C'est {self.name} de la couleur {self.color}. "
                    f"Elle coûte {self.value} €.")#voir plus tard pour le cout des maisons


class Luck(Square):

    def __init__(self, name, position):
        Square.__init__(self,name,position)
        with open("impact_luck.json") as impact_luck :
            self.impact_list = json.load(impact_luck)["dependencies"]
        #définir méthode et voir comment gérer les impacts
        # voir méthode random qui pioche dans une liste d'impact
