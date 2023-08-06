from src.main.game.DominoRound import DominoRound
from src.main.player.Brain import RandomBrain


def test_round_initialization():
    # Initialize a bunch of rounds and check there's a valid starting setup every time
    for i in range(10):
        round = DominoRound(RandomBrain(), RandomBrain())

        assert round.origin is not None
        assert round.origin.is_double


