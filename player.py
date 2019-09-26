import random
from square import Square, Land, Luck



class Player :


    def __init__(self,name,board):
        self.name = name
        self. money = 200
        self.position = 0
        self.assets = []
        self.board = board #le plateau sur lequel le joueur joue
        self.board.square_list[self.position].present_player.append(self.name) #on place le joueur sur la case départ


    def throw_dice(self):

        self.board.square_list[self.position].present_player.remove(self.name) #on retire le player de sa case

        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6) #quand on rajoutera les tours, mettre l'option double = rejouer

        advance = dice1 + dice2
        print(f"Vous avancez de {advance} cases.")

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
                try :
                    answer = input(f"Vous avez {self.money}€ et vous possédez {self.assets} maison(s), souhaitez-vous acheter ? (oui/non)")
                    answer= answer.upper()
                    assert answer == ("OUI" or "NON")

                    if answer == "OUI": #si on veut l'acheter
                        return self.buy_land(square)

                    #apres avoir refusé d'acheter, que fait on ?
                except Exception as e:
                    print(e)
                    print ("Vous devez répondre par oui ou non ! ")

        # cas où on tombe sur une case chance
        if isinstance(square, Luck):
            square.get_impact(self)





    def buy_land(self, square):
        self.money -= square.value
        square.owner = self.name
        square.status = True
        self.assets.append(square)
        print(f"Vous êtes maintenant propriétaire de {square.name}")


    def pay_rent(self, square):
        rent = square.rent[square.nb_houses]
        if self.money >= rent:
            print("Vous venez de payer " + str(rent) + "€ à " + str(square.owner) +
                  f"... Il vous reste {self.money}€.")
        else:
            print("Aïe! Vous n'avez pas assez d'argent pour régler vos dettes! "
                  "Que voulez vous faire?")
            #Hypothéquer?
            #Proposer un échange
            #Fin de partie?
            #puis nouvel appel à fonction pay_rent






