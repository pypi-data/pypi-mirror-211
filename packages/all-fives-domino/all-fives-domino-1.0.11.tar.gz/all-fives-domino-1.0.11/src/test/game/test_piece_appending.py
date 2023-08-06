from src.main.game.Piece import Piece


def test_append_sequence():
    p_5_5 = Piece(5, 5)
    p_5_2 = Piece(5, 2)
    p_5_5.append(p_5_2)

    assert p_5_2.linked_to == p_5_5
    assert p_5_2.linked == []
    assert p_5_5.linked_to is None
    assert p_5_5.linked == [p_5_2]