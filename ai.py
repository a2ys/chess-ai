import random

import board
import move
import moves
from defs import const


def evaluate(gs: board.GameState) -> int:
    board_eval = 0

    for rank in gs.board:
        for piece in rank:
            if piece.get_alpha() != '--':
                temp_alpha = piece.get_alpha().upper()
                if piece.get_color().lower() == 'white':
                    board_eval += const.PIECE_VALUES[temp_alpha[1]]
                else:
                    board_eval -= const.PIECE_VALUES[temp_alpha[1]]
    return board_eval


def make_move(gs: board.GameState) -> None:
    more_feasible_moves = []
    less_feasible_moves = []

    for rank in gs.board:
        for piece in rank:
            if piece.get_color() == gs.active_player().lower():
                pseudo_legal_moves = moves.legal_moves(piece, gs.board)
                lgl_moves = const.legal_moves(pseudo_legal_moves, gs.illegal_moves(piece)) + gs.special_moves(piece)

                initial_eval = evaluate(gs)

                for legal_move in lgl_moves:
                    test_mv = const.get_move_from_id(legal_move)
                    r_mv = move.Move(test_mv[0], test_mv[1], gs.board)

                    gs.make_move(r_mv, sound=False)

                    for row in gs.board:
                        for p in row:
                            if p.get_alpha() != '--':
                                if p.get_color().lower() == gs.active_player():
                                    pseudo_legal_moves = moves.legal_moves(p, gs.board)
                                    lgl_moves = const.legal_moves(pseudo_legal_moves, gs.illegal_moves(p)) + gs.special_moves(p)

                                    eval2 = evaluate(gs)

                                    for m in lgl_moves:
                                        t = const.get_move_from_id(m)
                                        r = move.Move(t[0], t[1], gs.board)

                                        gs.make_move(r, sound=False)

                                        if evaluate(gs) < eval2:
                                            less_feasible_moves += [r_mv]
                                        else:
                                            more_feasible_moves += [r_mv]

                                        gs.undo_move()

                    gs.undo_move()

    if more_feasible_moves:
        random_move_id = random.randint(0, len(more_feasible_moves) - 1)
        gs.make_move(more_feasible_moves[random_move_id])
    else:
        gs.make_move(less_feasible_moves[random.randint(0, len(less_feasible_moves) - 1)])
