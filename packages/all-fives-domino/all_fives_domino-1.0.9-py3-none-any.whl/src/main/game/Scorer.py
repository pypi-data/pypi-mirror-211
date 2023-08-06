class Scorer:
    @classmethod
    def count(cls, piece: "Piece", depth=28) -> int:
        """Calculate the current point value for a board by its origin piece"""
        raise NotImplementedError("No counting method, override this!")

    @classmethod
    def score(cls, count: int) -> int:
        """Calculate the score that should be awarded for a board state"""
        raise NotImplementedError("No scoring method, override this!")


class AllFivesScorer(Scorer):
    @classmethod
    def count(cls, piece: "Piece", depth=28) -> int:
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
            print("Adding for crossing")
            score += piece.sides[0]

        # Score all connected pieces
        for linked_piece in piece.linked:
            score += cls.count(linked_piece, depth - 1)

        print(piece, score)
        return score

    @classmethod
    def score(cls, count: int) -> int:
        return count if (count % 5 == 0) else 0

