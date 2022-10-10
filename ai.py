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
    best_move = find_best_move(gs)
    tmv = const.get_move_from_id(best_move)
    mv = move.Move(tmv[0], tmv[1], gs.board)
    gs.make_move(mv)


def find_best_move(gs: board.GameState) -> str:
    global next_move

    next_move = None
    valid_moves = generate_legal_moves(gs)
    random.shuffle(valid_moves)
    find_move_nega_max_alpha_beta(gs, valid_moves, const.DEPTH, -const.CHECKMATE, const.CHECKMATE, 1 if gs.white_to_move else -1)

    return next_move


def find_move_nega_max(gs: board.GameState, valid_moves: list, depth: int, turn_multiplier: int) -> int:
    global next_move

    if depth == 0:
        return turn_multiplier * evaluate(gs)

    max_score = -const.CHECKMATE
    for valid_move in valid_moves:
        mv = const.get_move_from_id(valid_move)
        r = move.Move(mv[0], mv[1], gs.board)
        gs.make_move(r, sound=False)

        next_moves = generate_legal_moves(gs)
        score = -find_move_nega_max(gs, next_moves, depth - 1, -turn_multiplier)

        if score > max_score:
            max_score = score
            if depth == const.DEPTH:
                next_move = valid_move
        gs.undo_move()

    return max_score


def find_move_nega_max_alpha_beta(gs: board.GameState, valid_moves: list, depth: int, alpha: int, beta: int, turn_multiplier: int) -> int:
    global next_move

    if depth == 0:
        return turn_multiplier * evaluate(gs)

    max_score = -const.CHECKMATE
    for valid_move in valid_moves:
        mv = const.get_move_from_id(valid_move)
        r = move.Move(mv[0], mv[1], gs.board)
        gs.make_move(r, sound=False)

        next_moves = generate_legal_moves(gs)
        score = -find_move_nega_max_alpha_beta(gs, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)

        if score > max_score:
            max_score = score
            if depth == const.DEPTH:
                next_move = valid_move
        gs.undo_move()

        if max_score > alpha:
            alpha = max_score

        if alpha >= beta:
            break

    return max_score
