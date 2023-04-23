import unittest

import board
import move_generator


class Tests(unittest.TestCase):
    def total_moves(self, depth: int, gs: board.GameState) -> int:
        board_array = gs.board
        active_player = gs.active_player()
        total = 0

        for rank in board_array:
            for piece in rank:
                if piece.get_color() == active_player:
                    lgl_moves = gs.legal_moves(move_generator.legal_moves(piece, gs.board))
                    for _ in lgl_moves:
                        if depth == 1:
                            total += 1
                        else:
                            gs.make_move(_, False)
                            total += self.total_moves(depth - 1, gs)
                            gs.undo_move(False)
        return total

    def test_first(self) -> None:
        gs = board.GameState()
        self.assertEqual(self.total_moves(1, gs), 20)

    def test_second(self) -> None:
        gs = board.GameState()
        self.assertEqual(self.total_moves(2, gs), 400)

    def test_third(self) -> None:
        gs = board.GameState()
        self.assertEqual(self.total_moves(3, gs), 8902)

    def test_fourth(self) -> None:
        gs = board.GameState()
        self.assertEqual(self.total_moves(4, gs), 197281)

    def test_fifth(self) -> None:
        gs = board.GameState()
        self.assertEqual(self.total_moves(5, gs), 4865609)
