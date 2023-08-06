from typing import Union
import random

from src.main.game.Piece import domino_set, Piece
from src.main.player.Player import Player
from src.main.player.Hand import Hand
from src.main.game.Scorer import AllFivesScorer


class DominoRound:
    def __init__(self, brain1: "Brain", brain2: "Brain", begins: Union["Brain", None] = None):
        self.pool = domino_set()
        random.shuffle(self.pool)
        self.origin: Union[Piece, None] = None
        self.player1 = Player(brain1, self)
        self.player2 = Player(brain2, self)
        self.current_player = self.player1 if begins == brain1 else (self.player2 if begins == brain2 else None)
        self.has_crossing = False
        self.scorer = AllFivesScorer

        self.start()

    def deal_hand(self):
        # Each player receives 7 initial pieces
        for i in range(7):
            self.player1.draw()
            self.player2.draw()

    def check_required_starting_piece(self):
        """
        Find the piece a player is required to start with.

        If no starting player is defined, the player with [5|5] begins.
        If neither player has [5|5], the order goes [1|1], [2|2], ..., [6|6], [0|0].
        If neither player has any double pieces, they draw a piece each until one does.
        """
        if self.current_player is not None:
            return

        piece = None
        while self.current_player is None:
            for i in [5, 1, 2, 3, 4, 6, 0]:
                piece = Piece(i, i)

                if piece in self.player1.hand:
                    self.current_player = self.player1
                    break
                if piece in self.player2.hand:
                    self.current_player = self.player2
                    break

            if self.current_player is None:
                self.player1.draw()
                self.player2.draw()

        self.play(piece)

    def award_score(self):
        self.current_player.score += self.scorer.score(self.scorer.count(self.origin))

    def play(self, piece: Piece, origin: Union[Piece, None] = None, close=False):
        player = self.current_player

        if piece not in player.hand:
            raise Exception(f"Player attempted to play {piece}, but it's not in their hand")

        if piece.is_double and self.has_crossing and close:
            piece.closed = True

        player.hand.pop(piece)

        if origin is None:
            if self.origin is not None:
                raise Exception(f"Player attempted to play {piece} as origin, "
                                f"but there is already origin piece {self.origin}")
            self.origin = piece
        else:
            origin.append(piece)

        if self.has_crossing and origin is not None:
            origin.is_crossing = False
        else:
            if origin is not None and origin.is_crossing:
                self.has_crossing = True

        self.award_score()

        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def get_pieces(self, piece: Piece = None):
        # Default to origin piece
        if piece is None:
            piece = self.origin

        pieces = [piece]
        for linked_piece in piece.linked:
            pieces += self.get_pieces(linked_piece)
        return pieces

    def open_ends(self, piece: Piece = None):
        # Default to origin piece
        if piece is None:
            piece = self.origin

        ends = [(piece, side) for side in piece.open_sides]
        for linked_piece in piece.linked:
            ends += self.open_ends(linked_piece)

        return sorted(ends)

    def valid_options(self):
        origins = self.get_pieces()
        options = []

        for piece in self.current_player.hand:
            options += [(piece, origin) for origin in origins if origin.can_append(piece)]

        return options

    def start(self):
        self.deal_hand()
        self.check_required_starting_piece()
