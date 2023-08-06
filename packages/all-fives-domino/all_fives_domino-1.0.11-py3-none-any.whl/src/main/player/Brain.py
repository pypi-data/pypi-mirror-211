import random

from src.main.player.Player import Player
from src.main.game.DominoRound import DominoRound


class Brain:
    def play(self, player: Player, round: DominoRound):
        raise NotImplementedError("The basic Player does not know how to play, please use a subclass!")


class RandomBrain(Brain):
    def play(self, player: Player, round: DominoRound):
        return random.choice(round.valid_options())
