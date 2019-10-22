import json
import random
#import player
#import main
#

class Square:

    def __init__(self,name,position):
        self.name = name
        self.position = position
        self.present_player = []


    #def __repr__(self,player):
        #player.send_message("Vous êtes tombés sur la case départ")

    #def str(self,player):
        #player.send_message("Vous êtes tombés sur la case départ")
        #return

    def get_actions(self,player):
        dict = { 1: "Terminer mon tour"}
        return dict


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

    def __init__(self, name, position, value, color, rent, construction_price):
        Square.__init__(self,name,position)
        self.value = value
        self.color = color
        self.rent = rent
        self.owner = ""
        self.status = False
        self.nb_houses = 0
        self.mortgage = False    #Vrai si le terrain est hypothéqué, faux sinon
        self.construction_price = construction_price


    @property
    def actions(self):
        return self.actions.keys()

    def get_actions(self,player):
        if self.status and player != self.owner:
            dict = { 1: "Payer le loyer"}
        else :
            dict = { 1: "Acheter le terrain", 2:"Terminer mon tour"}

        return dict


    # #def __repr__(self,player):
    #     if self.status :
    #         print(f"Cette case est {self.name}, détenue par le joueur {self.owner.name}. Il y a {self.nb_houses} maisons contruites."
    #                    f"Le loyer actuel est de {self.rent[self.nb_houses]} €")
    #     else :
    #         print(f"Cette case est libre ! C'est {self.name} de la couleur {self.color}. "
    #                 f"Elle coûte {self.value} €.")#voir plus tard pour le cout des maisons

    def str(self,player):
        if self.status :
            player.send_message (f"Cette case est {self.name}, détenue par le joueur {self.owner.name}. Il y a {self.nb_houses} maisons contruites."
                       f"Le loyer actuel est de {self.rent[self.nb_houses]} €")
        else :
            player.send_message (f"Cette case est libre ! C'est {self.name} de la couleur {self.color}. "
                    f"Elle coûte {self.value} €.")#voir plus tard pour le cout des maisons
        return

    def buy_land(self, player):
        player.money -= self.value
        self.owner = player
        self.status = True
        player.assets.append(self)
        #player.send_message(f"Le joueur {player.name} est maintenant propriétaire de {self.name}")

    def pay_rent(self, player):
        # si c'est une gare, on calcule le loyer en fonction du nombre de gare possédé par l'adversaire.
        if self.color == "trainstation":
            nb_trainstation = self.owner.get_nb_assets_of_a_color("trainstation", self.owner)
            rent = self.rent[nb_trainstation-1]
            #player.send_message(f"Le joueur {self.owner.name} possède {nb_trainstation} gares.")
        #si c'est un terrain, on calcule le loyer en fonction du nombre de maisons construites
        else:
            rent = self.rent[self.nb_houses]

        #si le joueur actif est capable de payer, il paye et l'autre reçoit l'argent
        if player.money >= rent:
            player.money -= rent
            self.owner.money+=rent
            #player.send_message(f"Le joueur {player.name} vient de payer {rent} € à {self.owner.name}")
        else:
            print("autre")
            #player.send_message(f"Aïe! Le joueur {player.name} n'a pas assez d'argent pour régler ses dettes! ")

    def to_mortgage(self):
        self.mortgage = True
        self.owner.money += self.value/2
        return(f"Le joueur {self.owner.name} a hypothéqué {self.name} et a gagné {self.value/2}€.")

    def to_clear_mortgage(self):
        self.mortgage = False
        self.owner.money -= self.value / 2
        print(f"Le joueur {self.owner.name} a deshypothéqué {self.name} et a payé {self.value/2}€.")

    def get_dict_houses_to_build(self):
        nb_max = 5 - self.nb_houses
        dict_nb_choice = {}
        for i in range(nb_max + 1):
            dict_nb_choice[i] = str(i)
        return dict_nb_choice

    def to_build(self, nb_houses_to_build):
        nb_max = 5 - self.nb_houses
        try:
            #on vérifie que le nombre de maisons rentré est bien un entier, compatible avec le nombre maximal de maisons par terrain
            assert (nb_houses_to_build < nb_max)
            self.nb_houses += nb_houses_to_build #on construit
            self.owner.money -= self.construction_price* nb_houses_to_build #on fait payer la construction
            return(f"Bravo, le joueur {self.owner.name} a désormais {self.nb_houses} maisons sur {self.name}.")

        except AssertionError:
            return(f"Impossible de construire autant de maisons : max {nb_max} maisons")

    def to_sell(self, nb_houses_to_sell):
        try:
            nb_max = self.nb_houses
            assert( nb_houses_to_sell < nb_max) #on ne peut pas vendre plus de maisons qu'on en a déjà sur le terrain
            self.nb_houses -= nb_houses_to_sell  # destruction de la maison
            self.owner.money += self.construction_price/2 * nb_houses_to_sell  # on vend pour la moitié du prix de construction
            return(f"Terrible, le joueur {self.owner.name} n'a désormais plus que {self.nb_houses} maisons sur {self.name}.")

        except AssertionError:
            return("Impossible de vendre plus de maisons que celles déjà construites")


class Luck(Square):

    def __init__(self, name, position):
        Square.__init__(self,name,position)
        with open("impact_luck.json") as impact_luck :
            self.impact_list = json.load(impact_luck)["dependencies"]
            self.nbre = len(self.impact_list)

        #définir méthode et voir comment gérer les impacts
        # voir méthode random qui pioche dans une liste d'impact

    #def __repr__(self):
        #return("Vous êtes tombés sur une carte chance !")

    def get_actions(self,player):
        dict = { 1: "Tirer une carte chance"}
        return dict

    def str(self,player):
        player.send_message("Vous êtes tombés sur une carte chance !")
        return

    def get_impact(self,player,board):
        luck_impact = random.randint(1,self.nbre)
        name = self.impact_list[1]["name"]
        description = self.impact_list[1]["description"]
        code = self.impact_list[1]["code"]
        player.send_message(name)
        player.send_message(description)
        if code[0] == "G":
            player.money += int(code[1:])
            player.send_message(f"Vous avez à présent {player.money}€")
            return
        elif code[0] == "P":
            player.money -= int(code[1:])
            player.send_message(f"Vous avez à présent {player.money}€")
            return
        elif code[0] == "A":
            board.change_position(player,int(code[1:]))
            board.square_list[player.position].str(player)
            return "new_pos"
        elif code[0] == "R":
            board.change_position(player,-int(code[1:]))
            board.square_list[player.position].str(player)
            return "new_pos"


class Tax(Square):

    def __init__(self, name, position, amount):
        Square.__init__(self, name, position)
        self.amount = amount

    #def __repr__(self):
     #       return (f"C'est une case de taxe ... Montant à payer : {self.amount}")

    def str(self,player):
            player.send_message(f"C'est une case de taxe ... Montant à payer : {self.amount}")
            return

    def get_actions(self,player):
        dict = { 1: "Payer la taxe"}
        return dict

    def pay_taxes(self,player):
        if player.money >= self.amount:
            player.money -= self.amount
            return(f"Le joueur {player.name} vient de payer {self.amount} € à la banque ... Il lui reste {player.money}€")
        else:
            return(f"Aïe! Le joueur {player.name} n'a pas assez d'argent pour régler ses dettes! ")
