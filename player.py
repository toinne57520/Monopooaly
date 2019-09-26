import random
from square import Square, Land, Luck



class Player :


    def __init__(self,name,board):
        self.name = name
        self. money = 200
        self.position = 0
        self.assets = []
        self.board = board #le plateau sur lequel le joueur joue

    def throw_dice(self):
        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)
        advance = dice1 + dice2
        print(f"Vous avancez de {advance} cases.")
        quotient =(self.position + advance) // len(self.board.square_list)
        self.position = (self.position + advance) % len(self.board.square_list)
        if quotient>0 :
            self.money += quotient * 200
            print (f"Vous êtes passés par la case départ. Félicitations ! vous avez gagné {quotient*200} €")
        print(self.board.square_list[self.position])
        #on appelle la méthode qui ensuite nous redirige vers la bonne action
        self.action_choice()

    def action_choice(self):
        square = square = self.board.square_list[self.position]
        #cas où on tombe sur une case terrain
        if isinstance(square,Land):
            #si le terrain est habité
            if square.status :
                #payer
                #si le terrain est vide
                print("ok")
            else :
                #à changer car renvoie juste une liste de cases
                try :
                    answer = input(f"Vous avez {self.money}€ et vous possédez {self.assets}, souhaitez-vous acheter ? (oui/non)")
                    answer= answer.upper()
                    assert answer == ("OUI" or "NON")
                    #si on veut l'acheter
                    if answer == "OUI":
                        return self.buy_land()
                    #apres avoir refusé d'acheter, que fait on ?
                except :
                    print ("Vous devez répondre par oui ou non ! ")

        # cas où on tombe sur une case terrain
       # if isinstance(square, Luck):
            #methode de Luck





    def buy_land(self):
        square = self.board.square_list[self.position]
        self.money -= square.value
        square.owner = self.name
        square.status = True
        self.assets.append(square)
        print(f"Vous êtes maintenant propriétaire de {square.name}")

