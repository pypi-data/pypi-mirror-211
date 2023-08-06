from typing import Union, List, Tuple

from src.main.game.Piece import domino_set, Piece
from src.main.player.Player import Player


class DominoRound:
    def __init__(self, brain1: "Brain", brain2: "Brain", begins: Union["Brain", None]):
        self.pool = domino_set()
        self.origin: Union[Piece, None] = None
        self.player1 = Player(brain1, self)
        self.player2 = Player(brain2, self)
        self.current_player = self.player1 if begins == brain1 else (self.player2 if begins == brain2 else None)
        self.has_crossing = False

    def deal_hand(self):
        # Each player receives 7 initial pieces
        for i in range(7):
            self.player1.draw()
            self.player2.draw()

    def get_required_starting_piece(self):
        """
        Find the piece a player is required to start with.

        If no starting player is defined, the player with [5|5] begins.
        If neither player has [5|5], the order goes [1|1], [2|2], ..., [6|6], [0|0].
        If neither player has any double pieces, they draw a piece each until one does.
        """
        if self.current_player is not None:
            return None

        while self.current_player is None:
            for i in [5, 1, 2, 3, 4, 6, 0]:
                piece = Piece(i, i)

                if piece in self.player1.hand:
                    self.current_player = self.player1
                    return piece
                if piece in self.player2.hand:
                    self.current_player = self.player1
                    return piece

    @staticmethod
    def score_piece(piece: Piece, depth=28) -> int:
        """
        Calculate the score for a piece and it's attached pieces
        """
        # Contingency against loops
        if depth < 0:
            raise Exception("Recursion too deep, some pieces linked in a loop?")

        score = 0

        # If no pieces are attached, the score is the value of the piece
        if piece.linked_to is None and not piece.linked:
            score += piece.points

        # If one of the sides is an end, the score is that side. For doubles, both sides are counted
        if (not piece.linked and piece.linked_to is not None) or (piece.linked_to is None and len(piece.linked) == 1):
            if piece.is_double:
                score += piece.points
            else:
                score += piece.unlinked_side(piece.linked_to)

        # For crossing pieces with exactly 3 connections, the open side is also counted
        if piece.is_crossing and len(piece.linked) == 3:
            score += piece.sides[0]

        # Score all connected pieces
        for linked_piece in piece.linked:
            score += Piece.score_piece(linked_piece, depth - 1)

        return score

    def score(self):
        score = self.score_piece(self.origin)
        self.current_player.score += score

    def play(self, player: Player, piece: Piece, origin: Union[Piece, None], close=False):
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
        self.score()

        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def valid_options(self, hand):
        return []

    def run(self):
        starting_piece = self.get_required_starting_piece()
        if starting_piece is not None:
            self.play(self.current_player, starting_piece, None)

        while True:
            pass
