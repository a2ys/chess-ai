import random
import time

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


def generate_legal_moves(gs: board.GameState) -> list:
    legal_moves = []

    for rank in gs.board:
        for piece in rank:
            if piece.get_alpha() != '--':
                if piece.get_color() == gs.active_player():
                    lgl_moves = gs.legal_moves(moves.legal_moves(piece, gs.board)) + gs.special_moves(piece)
                    legal_moves += lgl_moves

    return legal_moves


def make_move(gs: board.GameState) -> None:
    turn_multiplier = 1 if gs.white_to_move else -1
    opponent_minmax_score = const.CHECKMATE
    best_move = None
    player_moves = generate_legal_moves(gs)
    random.shuffle(player_moves)

    for player_move in player_moves:
        test_mv = const.get_move_from_id(player_move)
        r_mv = move.Move(test_mv[0], test_mv[1], gs.board)
        gs.make_move(r_mv, sound=False)
        opponent_max_score = -const.CHECKMATE
        opponent_moves = generate_legal_moves(gs)

        for opponent_move in opponent_moves:
            opp_mv = const.get_move_from_id(opponent_move)
            o_mv = move.Move(opp_mv[0], opp_mv[1], gs.board)
            gs.make_move(o_mv, sound=False)

            if gs.is_checkmate(gs.active_player()):
                score = -turn_multiplier * const.CHECKMATE
            elif gs.is_stalemate(gs.active_player()):
                score = const.STALEMATE
            else:
                score = -turn_multiplier * evaluate(gs)

            if score > opponent_max_score:
                opponent_max_score = score
            gs.undo_move()

        if opponent_max_score < opponent_minmax_score:
            opponent_minmax_score = opponent_max_score
            best_move = player_move
        gs.undo_move()

    tmv = const.get_move_from_id(best_move)
    mv = move.Move(tmv[0], tmv[1], gs.board)
    gs.make_move(mv)
