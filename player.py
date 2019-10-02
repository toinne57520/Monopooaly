from square import Land, Luck, Tax


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

        self.board.square_list[self.position].present_player.remove(self.name)  # on retire le player de sa case.

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

            if square.status and not square.mortgage : #si le terrain est habité
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

        elif isinstance(square, Tax):
            self.pay_taxes(square)

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

    def pay_taxes(self,square):
        if self.money >= square.amount:
            self.money -= square.amount
            print(f"Vous venez de payer {square.amount} € à la banque ... Il vous reste {self.money}€")

    def to_mortgage(self):
        #on vérifie que le joueur possède des terrains
        active_assets=[]
        try :
            for element in self.assets:
                if not element.mortgage:
                    active_assets.append(element)
            assert len(active_assets)>0
        except AssertionError :
            print("Cela s'annonce compliqué, vous n'avez pas de terrains à hypothéquer")

        #on liste les possessions actives du joueur et la valeur de l'hypothèque
        assets_mortgage = [[element.name,element.value/2] for element in active_assets]
        print(f"Vous possédez en ce moment {assets_mortgage}")
        #on propose au joueur de choisir son terrain à hypothéquer
        try :
            answer = input("Quel terrain souhaitez-vous hypothéquer ?")
            answer=answer.upper()
            assert answer in [element.name.upper() for element in active_assets]
        except AssertionError:
            print("Rentrez un terrain valide")
            self.to_mortgage()

        #on parcourt les assets pour retrouver le terrain à hypothéquer
        #essayer d'enlever cette boucle
        for element in active_assets :
            if element.name.upper() == answer :
                element.mortgage = True
                self.money += element.value/2
                print (f"Vous avez hypothéqué {element.name} et vous avez gagné {element.value/2}€.")
                print(element.mortgage)

    def to_clear_mortgage(self):
        passive_assets = []
        try:
            for element in self.assets:
                if element.mortgage:
                    passive_assets.append(element)
            assert len(passive_assets) > 0
        except AssertionError:
            print("Cela s'annonce compliqué, vous n'avez pas de terrains à deshypothéquer")

        # on liste les possessions hypothéquées du joueur et la valeur de l'hypothèque
        assets_mortgage = [[element.name, element.value / 2] for element in passive_assets]
        print(f"Vos terrains hypothéqués et leur valeur d'hypothèque sont {assets_mortgage}. ")
        # on propose au joueur de choisir son terrain à hypothéquer.
        try:
            answer = input("Quel terrain souhaitez-vous deshypothéquer ?")
            answer = answer.upper()
            assert answer in [element.name.upper() for element in passive_assets]
        except AssertionError:
            print("Rentrez un terrain valide")
            self.to_clear_mortgage()
        for element in passive_assets :
            if element.name.upper() == answer :
                element.mortgage = False
                self.money -= element.value/2
                print (f"Vous avez deshypothéqué {element.name} et vous avez payé {element.value/2}€.")
                print(element.mortgage)

    def get_building_lands(self):
        """
        Cette méthode renvoie tous les terrains constructibles (c'est à dire avec la couleur complète) du joueur s'il en a.

        """
        building_lands = []
        try:
            for element in self.assets:
                #on compare le nombre de terrains de la couleur détenus par le joueur et le nombre de ces terrains sur le plateau
                if self.get_nb_assets_of_a_color(element.color) == self.board.get_nb_lands_of_a_color(element.color) and element.color!="trainstation":
                    building_lands.append(element)
            assert len(building_lands) > 0
            building_lands_color_price = [[element.name, element.color, element.construction_price] for element in building_lands]
            # on affiche les terrains constructibles, leur couleur et leur prix de construction
            # affichage à améliorer
            print(f"Vous pouvez construire sur (et chaque maison coûte) {building_lands_color_price}")
            return True, building_lands
        except AssertionError:
            print("Cela s'annonce compliqué, vous n'avez pas de terrains constructibles. Vous n'avez aucun quartier complet, repartez à l'aventure.")
            return False

    def to_build(self):
        """
        Cette méthode permet de faire choisir au joueur la couleur sur laquelle il veut construire
        :return:
        """
        building_lands = self.get_building_lands()

        if building_lands[0]:
            want_to_build = True
            while want_to_build :
                try:
                    color = input("Sur quelle couleur souhaitez-vous construire? rentrez une couleur ou rentrez Annuler")
                    color = color.upper()
                    assert (color in [element.color.upper() for element in building_lands[1]] or color =="ANNULER")

                    if color=="ANNULER":
                        break
                    else :
                        #une fois la couleur choisie, on appelle la méthode qui permet de construire avec une couleur donnée
                        self.to_build_neighbourhood(building_lands[1], color)

                except AssertionError:
                    print("Rentrez une couleur constructible")
                    self.to_build()
                try :
                    answer = input ("Souhaitez-vous construire une autre couleur ? (oui/non)")
                    assert (answer.upper() == "OUI" or answer.upper()=="NON")
                    if answer.upper()=="NON":
                        break
                except AssertionError:
                    print("Merci de répondre par oui ou par non !")
                    self.to_build()


    def to_build_neighbourhood(self,building_lands, color):

        #on va afficher tous les terrains constructibles de la couleur choisie
        building_lands_of_color = [element for element in building_lands if element.color.upper() == color]
        print(building_lands_of_color)
        want_to_build = True
        while want_to_build :
            try:
                land = input("Sur quel terrain souhaitez-vous construire? rentrez un nom ou rentrez Annuler")
                land = land.upper()
                assert (land in [element.name.upper() for element in building_lands_of_color] or land =="ANNULER")
                if land=="ANNULER":
                    break
                else :
                    land_to_build = [element for element in building_lands_of_color if element.name.upper()==land][0]
                    self.to_build_one_land(land_to_build)

            except AssertionError:
                print("Rentrez un terrain constructible")
                self.to_build_neighbourhood(building_lands, color)
            try :
                answer = input ("Souhaitez-vous construire sur un autre terrain de cette couleur? (oui/non)")
                assert (answer.upper() == "OUI" or answer.upper()=="NON")
                if answer.upper()=="NON":
                    break
            except AssertionError:
                print("Merci de répondre par oui ou par non !")
                self.to_build_neighbourhood(building_lands, color)


    def to_build_one_land(self, land_to_build):
        """
        Cette méthode permet de construire un nombre de maisons choisi par l'utilisateur sur un terrain donné
        :param land_to_build:
        :return:
        """
        try:
            #on vérifie que le nombre de maisons rentré est bien un entier, compatible avec le nombre maximal de maisons par terrain
            nb_max = 5 - land_to_build.nb_houses
            nb_to_build = float(input(f"Combien de maisons voulez-vous construire sur {land_to_build.name}? (Maximum {nb_max} maisons)"))
            assert nb_to_build == int(nb_to_build)
            if nb_to_build > nb_max:
                raise ValueError("")

            land_to_build.nb_houses += int(nb_to_build) #construction de la maison
            land_to_build.owner.money -= int(land_to_build.construction_price * nb_to_build) #on fait payer le joueur nouvellement propriétaire
            print(f"Bravo, vous avez désormais {land_to_build.nb_houses} maisons sur {land_to_build.name}.")

        except AssertionError:
            print("Renseignez un nombre entier de maisons")
            self.to_build_one_land(land_to_build)

        except ValueError:
            print("Vous ne pavez pas construire plus qu'un hotel (soit 5 maisons)")
            self.to_build_one_land(land_to_build)
















