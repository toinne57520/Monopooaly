from player import Player
from board import Board

#Ce test teste la méthode pay_rent de Player avec un plateau constitué uniquement de gares.

game = Board('Boards/taxes.json')
joueur = Player('Antoine',game)
jean = Player('Jean', game)



for i in game.square_list:
    i.owner=jean
    i.status=True
    jean.assets.append(i)
joueur.throw_dice()

print(joueur.position)
print(joueur.money)