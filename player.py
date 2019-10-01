from square import Land, Luck


import random

class Player :


    def __init__(self,name,board):
        self.name = name
        self.money = 200
        self.position = 0
        self.assets = []
        self.board = board #le plateau sur lequel le joueur joue
        self.board.square_list[self.position].present_player.append(self.name) #on place le joueur sur la case départ
        board.add_player(self)

    def get_nb_assets_of_a_color(self, color):
        i=0
        for asset in self.assets :
                if asset.color==color:
                   i+=1
        return i


    def throw_dice(self):
        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6) #quand on rajoutera les tours, mettre l'option double = rejouer
        advance = dice1 + dice2
        print(f"Vous avancez de {advance} cases.")
        self.change_position(advance)


    def change_position(self, advance):

        self.board.square_list[self.position].present_player.remove(self.name)  # on retire le player de sa case

        quotient =(self.position + advance) // len(self.board.square_list)
        self.position = (self.position + advance) % len(self.board.square_list)

        if quotient>0 :
            self.money += quotient * 200
            print (f"Vous êtes passés par la case départ. Félicitations ! vous avez gagné {quotient*200} €")

        self.board.square_list[self.position].present_player.append(self.name) #on l'enregistre sur sa nouvelle case
        print(self.board.square_list[self.position])
        #on appelle la méthode qui ensuite nous redirige vers la bonne action
        self.action_choice()


    def action_choice(self):
        square = self.board.square_list[self.position]

        if isinstance(square,Land): #cas où on tombe sur une case terrain

            if square.status : #si le terrain est habité
                self.pay_rent(square)

            else :
                #à changer car renvoie juste une liste de cases
                answer = 0
                try:
                    answer = input(f"Vous avez {self.money}€ et vous possédez {self.get_nb_assets_of_a_color(square.color)} terrains de cette famille, souhaitez-vous acheter ? (oui/non)")
                    answer = answer.upper()
                    assert answer=="OUI" or answer=="NON"
                except AssertionError:
                    print ("Vous devez répondre par oui ou non ! ")
                    self.action_choice()
                if answer == "OUI": #si on veut l'acheter
                        return self.buy_land(square)

        # cas où on tombe sur une case chance
        elif isinstance(square,Luck):
            square.get_impact(self)


    def buy_land(self, square):
        self.money -= square.value
        square.owner = self
        square.status = True
        self.assets.append(square)
        print(f"Vous êtes maintenant propriétaire de {square.name}")


    def pay_rent(self, square):
        # si c'est une gare, on calcule le loyer en fonction du nombre de gare possédé par l'adversaire.
        if square.color == "trainstation":
            nb_trainstation = square.owner.get_nb_assets_of_a_color("trainstation")
            rent = square.rent[nb_trainstation-1]
            print(f"Le joueur {square.owner.name} possède {nb_trainstation} gares.")
        #si c'est un terrain, on calcule le loyer en fonction du nombre de maisons construites
        else:
            rent = square.rent[square.nb_houses]

        #si le joueur actif est capable de payer, il paye et l'autre reçoit l'argent
        if self.money >= rent:
            self.money -= rent
            square.owner.money+=rent
            print("Vous venez de payer " + str(rent) + "€ à " + str(square.owner.name) +
                  f"... Il vous reste {self.money}€.")
            print(f"Le joueur {square.owner.name} a désormais {square.owner.money}.")
        else:
            print("Aïe! Vous n'avez pas assez d'argent pour régler vos dettes! "
                  "Que voulez vous faire?")
            #Hypothéquer?
            #Proposer un échange
            #Fin de partie?
            #puis nouvel appel à fonction pay_rent





