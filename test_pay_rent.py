from player import Player
from board import Board


game = Board('data.json')
joueur = Player('Antoine',game)
jean = Player('Jean', game)



for i in game.square_list:
    i.owner=jean
    i.status=True
joueur.throw_dice()

print(joueur.position)
print(joueur.money)