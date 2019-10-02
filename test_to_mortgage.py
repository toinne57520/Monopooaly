from player import Player
from board import Board

#Ce test teste la méthode to_morgage de Player

game = Board('Boards/lands.json')
joueur = Player('Antoine',game)




for i in game.square_list:
    i.owner=joueur
    i.status=True
    joueur.assets.append(i)


joueur.to_mortgage()

print(joueur.position)
print(joueur.money)