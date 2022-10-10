import unittest

import board
import move
import moves
from defs import const


class Tests(unittest.TestCase):
    def test_first(self):
        gs = board.GameState()
        total = 0

        for rank in gs.board:
            for piece in rank:
                if piece.get_alpha() != '--':
                    if piece.get_color().lower() == 'white':
                        for _ in gs.legal_moves(moves.legal_moves(piece, gs.board)):
                            total += 1

        self.assertEqual(total, 20)

    def test_second(self):
        gs = board.GameState()
        total = 0

        for rank in gs.board:
            for piece in rank:
                if piece.get_alpha() != "--":
                    if piece.get_color().lower() == 'white':
                        for legal_move in gs.legal_moves(moves.legal_moves(piece, gs.board)):
                            pos = const.get_move_from_id(legal_move)
                            mv = move.Move(pos[0], pos[1], gs.board)
                            gs.make_move(mv, sound=False)

                            for r in gs.board:
                                for p in r:
                                    if p.get_alpha() != "--":
                                        if p.get_color().lower() == 'black':
                                            for _ in gs.legal_moves(moves.legal_moves(p, gs.board)):
                                                total += 1

                            gs.undo_move()

        self.assertEqual(total, 400)

    def test_third(self):
        gs = board.GameState()
        total = 0

        for rank in gs.board:
            for piece in rank:
                if piece.get_alpha() != "--":
                    if piece.get_color().lower() == 'white':
                        for legal_move in gs.legal_moves(moves.legal_moves(piece, gs.board)):
                            pos = const.get_move_from_id(legal_move)
                            m = move.Move(pos[0], pos[1], gs.board)
                            gs.make_move(m, sound=False)

                            for r in gs.board:
                                for p in r:
                                    if p.get_alpha() != "--":
                                        if p.get_color().lower() == 'black':
                                            for lgl_move in gs.legal_moves(moves.legal_moves(p, gs.board)):
                                                pos = const.get_move_from_id(lgl_move)
                                                mv = move.Move(pos[0], pos[1], gs.board)
                                                gs.make_move(mv, sound=False)

                                                for i in gs.board:
                                                    for j in i:
                                                        if j.get_alpha() != "--":
                                                            if j.get_color().lower() == 'white':
                                                                for _ in gs.legal_moves(moves.legal_moves(j, gs.board)):
                                                                    total += 1
                                                gs.undo_move()
                            gs.undo_move()
        self.assertEqual(total, 8902)

    def test_fourth(self):
        gs = board.GameState()
        total = 0

        for rank in gs.board:
            for piece in rank:
                if piece.get_alpha() != "--":
                    if piece.get_color().lower() == 'white':
                        for legal_move in gs.legal_moves(moves.legal_moves(piece, gs.board)):
                            pos = const.get_move_from_id(legal_move)
                            m = move.Move(pos[0], pos[1], gs.board)
                            gs.make_move(m, sound=False)

                            for r in gs.board:
                                for p in r:
                                    if p.get_alpha() != "--":
                                        if p.get_color().lower() == 'black':
                                            for lgl_move in gs.legal_moves(moves.legal_moves(p, gs.board)):
                                                pos = const.get_move_from_id(lgl_move)
                                                mv = move.Move(pos[0], pos[1], gs.board)
                                                gs.make_move(mv, sound=False)

                                                for i in gs.board:
                                                    for j in i:
                                                        if j.get_alpha() != "--":
                                                            if j.get_color().lower() == 'white':
                                                                for lgl in gs.legal_moves(moves.legal_moves(j, gs.board)):
                                                                    pos = const.get_move_from_id(lgl)
                                                                    mv = move.Move(pos[0], pos[1], gs.board)
                                                                    gs.make_move(mv, sound=False)

                                                                    for a in gs.board:
                                                                        for b in a:
                                                                            if b.get_alpha() != "--":
                                                                                if b.get_color().lower() == 'black':
                                                                                    for _ in gs.legal_moves(moves.legal_moves(b, gs.board)):
                                                                                        total += 1
                                                                    gs.undo_move()
                                                gs.undo_move()
                            gs.undo_move()
        self.assertEqual(total, 197281)

    def test_fifth(self):
        gs = board.GameState()
        total = 0

        for rank in gs.board:
            for piece in rank:
                if piece.get_alpha() != "--":
                    if piece.get_color().lower() == 'white':
                        for legal_move in gs.legal_moves(moves.legal_moves(piece, gs.board)):
                            pos = const.get_move_from_id(legal_move)
                            m = move.Move(pos[0], pos[1], gs.board)
                            gs.make_move(m, sound=False)

                            for r in gs.board:
                                for p in r:
                                    if p.get_alpha() != "--":
                                        if p.get_color().lower() == 'black':
                                            for lgl_move in gs.legal_moves(moves.legal_moves(p, gs.board)):
                                                pos = const.get_move_from_id(lgl_move)
                                                mv = move.Move(pos[0], pos[1], gs.board)
                                                gs.make_move(mv, sound=False)

                                                for i in gs.board:
                                                    for j in i:
                                                        if j.get_alpha() != "--":
                                                            if j.get_color().lower() == 'white':
                                                                for lgl in gs.legal_moves(moves.legal_moves(j, gs.board)):
                                                                    pos = const.get_move_from_id(lgl)
                                                                    mv = move.Move(pos[0], pos[1], gs.board)
                                                                    gs.make_move(mv, sound=False)

                                                                    for a in gs.board:
                                                                        for b in a:
                                                                            if b.get_alpha() != "--":
                                                                                if b.get_color().lower() == 'black':
                                                                                    pos = const.get_move_from_id(lgl)
                                                                                    mv = move.Move(pos[0], pos[1], gs.board)
                                                                                    gs.make_move(mv, sound=False)

                                                                                    for c in gs.board:
                                                                                        for d in c:
                                                                                            for _ in gs.legal_moves(moves.legal_moves(d, gs.board)):
                                                                                                total += 1
                                                                                    gs.undo_move()
                                                                    gs.undo_move()
                                                gs.undo_move()
                            gs.undo_move()
        self.assertEqual(total, 4865609)


if __name__ == '__main__':
    unittest.main()
