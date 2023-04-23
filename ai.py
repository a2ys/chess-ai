import random

import board
import move_generator
import move
from defs import Constants
from defs.enums.Colors import Color


def make_move(gs: board.GameState) -> None:
    best_move = find_best_move(gs)
    gs.make_move(best_move)


def find_best_move(gs: board.GameState) -> move.Move:
    global next_move

    next_move = None
    valid_moves = generate_legal_moves(gs)

    find_move_nega_max_alpha_beta(gs, valid_moves, Constants.DEPTH, -Constants.CHECKMATE, Constants.CHECKMATE,
                                  1 if gs.white_to_move else -1)

    if next_move is None:
        next_move = random.sample(sorted(valid_moves), 1)[0]

    return next_move


def generate_legal_moves(gs: board.GameState) -> set:
    legal_moves = set()

    for rank in gs.board:
        for piece in rank:
            if piece.get_color() == gs.active_player():
                piece_legal_moves = gs.legal_moves(move_generator.legal_moves(piece, gs.board))
                legal_moves = legal_moves.union(piece_legal_moves)

    return legal_moves


def evaluate(gs: board.GameState) -> int:
    board_eval = 0

    for rank in gs.board:
        for piece in rank:
            if piece.get_alpha() != '--':
                temp_alpha = piece.get_alpha().upper()
                if piece.get_color() == Color.WHITE:
                    board_eval += Constants.PIECE_VALUES[temp_alpha]
                else:
                    board_eval -= Constants.PIECE_VALUES[temp_alpha]
    return board_eval


def find_move_nega_max_alpha_beta(gs: board.GameState, valid_moves: set, depth: int, alpha: int, beta: int,
                                  turn_multiplier: int) -> int:
    global next_move

    if depth == 0:
        return turn_multiplier * evaluate(gs)

    max_score = -Constants.CHECKMATE

    for valid_move in valid_moves:
        gs.make_move(valid_move)

        next_moves = generate_legal_moves(gs)
        score = -find_move_nega_max_alpha_beta(gs, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)

        if score > max_score:
            max_score = score
            if depth == Constants.DEPTH:
                next_move = valid_move
        gs.undo_move()

        if max_score > alpha:
            alpha = max_score

        if alpha >= beta:
            break

    return max_score
