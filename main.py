from board import Board
import square
import json
from player import Player


game = Board('data.json')
joueur = Player('Antoine',game)
joueur.throw_dice()

print(joueur.position)
print(joueur.money)

