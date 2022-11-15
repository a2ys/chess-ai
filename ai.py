import random

import board
import move
import moves
from defs import const

knight_scores = [[-50, -40, -30, -30, -30, -30, -40, -50],
                 [-40, -20, 0, 0, 0, 0, -20, -40],
                 [-30, 0, 10, 15, 15, 10, 0, -30],
                 [-30, 5, 15, 20, 20, 15, 5, -30],
                 [-30, 0, 15, 20, 20, 15, 0, -30],
                 [-30, 5, 10, 15, 15, 10, 5, -30],
                 [-40, -20, 0, 5, 5, 0, -20, -40],
                 [-50, -40, -30, -30, -30, -30, -40, -50]]

bishop_scores = [[-20, -10, -10, -10, -10, -10, -10, -20],
                 [-10, 0, 0, 0, 0, 0, 0, -10],
                 [-10, 0, 5, 10, 10, 5, 0, -10],
                 [-10, 5, 5, 10, 10, 5, 5, -10],
                 [-10, 0, 10, 10, 10, 10, 0, -10],
                 [-10, 10, 10, 10, 10, 10, 10, -10],
                 [-10, 5, 0, 0, 0, 0, 5, -10],
                 [-20, -10, -10, -10, -10, -10, -10, -20]]

rook_scores = [[0, 0, 0, 0, 0, 0, 0, 0],
               [5, 10, 10, 10, 10, 10, 10, 5],
               [-5, 0, 0, 0, 0, 0, 0, -5],
               [-5, 0, 0, 0, 0, 0, 0, -5],
               [-5, 0, 0, 0, 0, 0, 0, -5],
               [-5, 0, 0, 0, 0, 0, 0, -5],
               [-5, 0, 0, 0, 0, 0, 0, -5],
               [0, 0, 0, 5, 5, 0, 0, 0]]

white_pawn_scores = [[0, 0, 0, 0, 0, 0, 0, 0],
                     [50, 50, 50, 50, 50, 50, 50, 50],
                     [10, 10, 20, 30, 30, 20, 10, 10],
                     [5, 5, 10, 25, 25, 10, 5, 5],
                     [0, 0, 0, 20, 20, 0, 0, 0],
                     [5, -5, -10, 0, 0, -10, -5, 5],
                     [5, 10, 10, -20, -20, 10, 10, 5],
                     [0, 0, 0, 0, 0, 0, 0, 0]]

black_pawn_scores = [[0, 0, 0, 0, 0, 0, 0, 0],
                     [5, 10, 10, -20, -20, 10, 10, 5],
                     [5, -5, -10, 0, 0, -10, -5, 5],
                     [0, 0, 0, 20, 20, 0, 0, 0],
                     [5, 5, 10, 25, 25, 10, 5, 5],
                     [10, 10, 20, 30, 30, 20, 10, 10],
                     [50, 50, 50, 50, 50, 50, 50, 50],
                     [0, 0, 0, 0, 0, 0, 0, 0]]

queen_scores = [[-20, -10, -10, -5, -5, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 5, 5, 5, 0, -10],
                [-5, 0, 5, 5, 5, 5, 0, -5],
                [0, 0, 5, 5, 5, 5, 0, -5],
                [-10, 5, 5, 5, 5, 5, 0, -10],
                [-10, 0, 5, 0, 0, 0, 0, -10],
                [-20, -10, -10, -5, -5, -10, -10, -20]]

king_scores = [[-30, -40, -40, -50, -50, -40, -40, -30],
               [-30, -40, -40, -50, -50, -40, -40, -30],
               [-30, -40, -40, -50, -50, -40, -40, -30],
               [-30, -40, -40, -50, -50, -40, -40, -30],
               [-20, -30, -30, -40, -40, -30, -30, -20],
               [-10, -20, -20, -20, -20, -20, -20, -10],
               [20, 20, 0, 0, 0, 0, 20, 20],
               [20, 30, 10, 0, 0, 10, 30, 20]]

piece_positional_scores = {'K': king_scores, 'Q': queen_scores, 'R': rook_scores, 'B': bishop_scores,
                           'N': knight_scores, 'p': black_pawn_scores, 'P': white_pawn_scores}


def evaluate(gs: board.GameState) -> int:
    board_eval = 0

    for rank in range(len(gs.board)):
        for file in range(len(gs.board[rank])):
            piece = gs.board[rank][file]
            if piece.get_alpha() != '--':
                temp_alpha = piece.get_alpha().upper()
                # if temp_alpha[1] == 'P':
                #     if temp_alpha[0] == 'w':
                #         piece_positional_score = piece_positional_scores['P'][rank][file]
                #     else:
                #         piece_positional_score = piece_positional_scores['p'][rank][file]
                # else:
                #     piece_positional_score = piece_positional_scores[temp_alpha[1]][rank][file]
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
