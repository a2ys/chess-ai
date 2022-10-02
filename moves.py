import board
from defs import const
from main import Main
from piece import Piece, King, Queen, Bishop, Knight, Rook, Pawn, WhiteSpace


def diagonal_moves(rank: int, file: int, m_arg_board: list) -> list:
    moves = []

    for i in range(rank + 1, 8):
        if file + (i - rank) <= 7:
            if isinstance(m_arg_board[i][file + (i - rank)], WhiteSpace.WhiteSpace):
                moves.append((i, file + (i - rank)))
            elif m_arg_board[i][file + (i - rank)].get_color() != m_arg_board[rank][file].get_color():
                moves.append((i, file + (i - rank)))
                break
            else:
                break

    for i in range(rank + 1, 8):
        if file - (i - rank) >= 0:
            if isinstance(m_arg_board[i][file - (i - rank)], WhiteSpace.WhiteSpace):
                moves.append((i, file - (i - rank)))
            elif m_arg_board[i][file - (i - rank)].get_color() != m_arg_board[rank][file].get_color():
                moves.append((i, file - (i - rank)))
                break
            else:
                break

    for i in range(rank - 1, -1, -1):
        if file + (rank - i) <= 7:
            if isinstance(m_arg_board[i][file + (rank - i)], WhiteSpace.WhiteSpace):
                moves.append((i, file + (rank - i)))
            elif m_arg_board[i][file + (rank - i)].get_color() != m_arg_board[rank][file].get_color():
                moves.append((i, file + (rank - i)))
                break
            else:
                break

    for i in range(rank - 1, -1, -1):
        if file - (rank - i) >= 0:
            if isinstance(m_arg_board[i][file - (rank - i)], WhiteSpace.WhiteSpace):
                moves.append((i, file - (rank - i)))
            elif m_arg_board[i][file - (rank - i)].get_color() != m_arg_board[rank][file].get_color():
                moves.append((i, file - (rank - i)))
                break
            else:
                break

    return moves


def straight_moves(rank: int, file: int, m_arg_board: list) -> list:
    moves = []

    for i in range(rank + 1, 8):
        if isinstance(m_arg_board[i][file], WhiteSpace.WhiteSpace):
            moves.append((i, file))
        elif m_arg_board[i][file].get_color() != m_arg_board[rank][file].get_color():
            moves.append((i, file))
            break
        else:
            break

    for i in range(rank - 1, -1, -1):
        if isinstance(m_arg_board[i][file], WhiteSpace.WhiteSpace):
            moves.append((i, file))
        elif m_arg_board[i][file].get_color() != m_arg_board[rank][file].get_color():
            moves.append((i, file))
            break
        else:
            break

    for i in range(file + 1, 8):
        if isinstance(m_arg_board[rank][i], WhiteSpace.WhiteSpace):
            moves.append((rank, i))
        elif m_arg_board[rank][i].get_color() != m_arg_board[rank][file].get_color():
            moves.append((rank, i))
            break
        else:
            break

    for i in range(file - 1, -1, -1):
        if isinstance(m_arg_board[rank][i], WhiteSpace.WhiteSpace):
            moves.append((rank, i))
        elif m_arg_board[rank][i].get_color() != m_arg_board[rank][file].get_color():
            moves.append((rank, i))
            break
        else:
            break

    return moves


def pawn_moves(rank: int, file: int, m_arg_board: list) -> list:
    moves = []

    if m_arg_board[rank][file].get_color() == "white":
        if rank > 0:
            if isinstance(m_arg_board[rank - 1][file], WhiteSpace.WhiteSpace):
                moves.append((rank - 1, file))
            if rank == 6:
                if isinstance(m_arg_board[rank - 1][file], WhiteSpace.WhiteSpace):
                    if isinstance(m_arg_board[rank - 2][file], WhiteSpace.WhiteSpace):
                        moves.append((rank - 2, file))
        if file - 1 >= 0:
            if m_arg_board[rank - 1][file - 1].get_color() == "black":
                moves.append((rank - 1, file - 1))
        if file + 1 <= 7:
            if m_arg_board[rank - 1][file + 1].get_color() == "black":
                moves.append((rank - 1, file + 1))
    else:
        if rank < 7:
            if isinstance(m_arg_board[rank + 1][file], WhiteSpace.WhiteSpace):
                moves.append((rank + 1, file))
            if rank == 1:
                if isinstance(m_arg_board[rank + 1][file], WhiteSpace.WhiteSpace):
                    if isinstance(m_arg_board[rank + 2][file], WhiteSpace.WhiteSpace):
                        moves.append((rank + 2, file))
        if file - 1 >= 0:
            if m_arg_board[rank + 1][file - 1].get_color() == "white":
                moves.append((rank + 1, file - 1))
        if file + 1 <= 7:
            if m_arg_board[rank + 1][file + 1].get_color() == "white":
                moves.append((rank + 1, file + 1))

    return moves


def knight_moves(rank: int, file: int, m_arg_board: list) -> list:
    moves = []

    if file + 2 <= 7:
        if rank + 1 <= 7:
            if isinstance(m_arg_board[rank + 1][file + 2], WhiteSpace.WhiteSpace):
                moves.append((rank + 1, file + 2))
            elif m_arg_board[rank + 1][file + 2].get_color() != m_arg_board[rank][file].get_color():
                moves.append((rank + 1, file + 2))
        if rank - 1 >= 0:
            if isinstance(m_arg_board[rank - 1][file + 2], WhiteSpace.WhiteSpace):
                moves.append((rank - 1, file + 2))
            elif m_arg_board[rank - 1][file + 2].get_color() != m_arg_board[rank][file].get_color():
                moves.append((rank - 1, file + 2))
    if file - 2 >= 0:
        if rank + 1 <= 7:
            if isinstance(m_arg_board[rank + 1][file - 2], WhiteSpace.WhiteSpace):
                moves.append((rank + 1, file - 2))
            elif m_arg_board[rank + 1][file - 2].get_color() != m_arg_board[rank][file].get_color():
                moves.append((rank + 1, file - 2))
        if rank - 1 >= 0:
            if isinstance(m_arg_board[rank - 1][file - 2], WhiteSpace.WhiteSpace):
                moves.append((rank - 1, file - 2))
            elif m_arg_board[rank - 1][file - 2].get_color() != m_arg_board[rank][file].get_color():
                moves.append((rank - 1, file - 2))
    if rank + 2 <= 7:
        if file + 1 <= 7:
            if isinstance(m_arg_board[rank + 2][file + 1], WhiteSpace.WhiteSpace):
                moves.append((rank + 2, file + 1))
            elif m_arg_board[rank + 2][file + 1].get_color() != m_arg_board[rank][file].get_color():
                moves.append((rank + 2, file + 1))
        if file - 1 >= 0:
            if isinstance(m_arg_board[rank + 2][file - 1], WhiteSpace.WhiteSpace):
                moves.append((rank + 2, file - 1))
            elif m_arg_board[rank + 2][file - 1].get_color() != m_arg_board[rank][file].get_color():
                moves.append((rank + 2, file - 1))
    if rank - 2 >= 0:
        if file + 1 <= 7:
            if isinstance(m_arg_board[rank - 2][file + 1], WhiteSpace.WhiteSpace):
                moves.append((rank - 2, file + 1))
            elif m_arg_board[rank - 2][file + 1].get_color() != m_arg_board[rank][file].get_color():
                moves.append((rank - 2, file + 1))
        if file - 1 >= 0:
            if isinstance(m_arg_board[rank - 2][file - 1], WhiteSpace.WhiteSpace):
                moves.append((rank - 2, file - 1))
            elif m_arg_board[rank - 2][file - 1].get_color() != m_arg_board[rank][file].get_color():
                moves.append((rank - 2, file - 1))

    return moves


def king_moves(rank: int, file: int, m_arg_board: list) -> list:
    moves = []

    if file + 1 <= 7:
        if rank + 1 <= 7:
            if isinstance(m_arg_board[rank + 1][file + 1], WhiteSpace.WhiteSpace):
                moves.append((rank + 1, file + 1))
            elif m_arg_board[rank + 1][file + 1].get_color() != m_arg_board[rank][file].get_color():
                moves.append((rank + 1, file + 1))
        if rank - 1 >= 0:
            if isinstance(m_arg_board[rank - 1][file + 1], WhiteSpace.WhiteSpace):
                moves.append((rank - 1, file + 1))
            elif m_arg_board[rank - 1][file + 1].get_color() != m_arg_board[rank][file].get_color():
                moves.append((rank - 1, file + 1))
    if file - 1 >= 0:
        if rank + 1 <= 7:
            if isinstance(m_arg_board[rank + 1][file - 1], WhiteSpace.WhiteSpace):
                moves.append((rank + 1, file - 1))
            elif m_arg_board[rank + 1][file - 1].get_color() != m_arg_board[rank][file].get_color():
                moves.append((rank + 1, file - 1))
        if rank - 1 >= 0:
            if isinstance(m_arg_board[rank - 1][file - 1], WhiteSpace.WhiteSpace):
                moves.append((rank - 1, file - 1))
            elif m_arg_board[rank - 1][file - 1].get_color() != m_arg_board[rank][file].get_color():
                moves.append((rank - 1, file - 1))
    if rank + 1 <= 7:
        if isinstance(m_arg_board[rank + 1][file], WhiteSpace.WhiteSpace):
            moves.append((rank + 1, file))
        elif m_arg_board[rank + 1][file].get_color() != m_arg_board[rank][file].get_color():
            moves.append((rank + 1, file))
    if rank - 1 >= 0:
        if isinstance(m_arg_board[rank - 1][file], WhiteSpace.WhiteSpace):
            moves.append((rank - 1, file))
        elif m_arg_board[rank - 1][file].get_color() != m_arg_board[rank][file].get_color():
            moves.append((rank - 1, file))
    if file + 1 <= 7:
        if isinstance(m_arg_board[rank][file + 1], WhiteSpace.WhiteSpace):
            moves.append((rank, file + 1))
        elif m_arg_board[rank][file + 1].get_color() != m_arg_board[rank][file].get_color():
            moves.append((rank, file + 1))
    if file - 1 >= 0:
        if isinstance(m_arg_board[rank][file - 1], WhiteSpace.WhiteSpace):
            moves.append((rank, file - 1))
        elif m_arg_board[rank][file - 1].get_color() != m_arg_board[rank][file].get_color():
            moves.append((rank, file - 1))

    return moves


def queen_moves(rank: int, file: int, m_arg_board: list) -> list:
    return straight_moves(rank, file, m_arg_board) + diagonal_moves(rank, file, m_arg_board)


def legal_moves(piece: Piece, arg_board: list) -> list:
    if isinstance(piece, King.King):
        moves = []
        for move in king_moves(piece.get_rank(), piece.get_file(), arg_board):
            moves.append(const.get_move_id([(piece.get_rank(), piece.get_file()), (move[0], move[1])]))
        return moves
    elif isinstance(piece, Queen.Queen):
        moves = []
        for move in queen_moves(piece.get_rank(), piece.get_file(), arg_board):
            moves.append(const.get_move_id([(piece.get_rank(), piece.get_file()), (move[0], move[1])]))
        return moves
    elif isinstance(piece, Bishop.Bishop):
        moves = []
        for move in diagonal_moves(piece.get_rank(), piece.get_file(), arg_board):
            moves.append(const.get_move_id([(piece.get_rank(), piece.get_file()), (move[0], move[1])]))
        return moves
    elif isinstance(piece, Knight.Knight):
        moves = []
        for move in knight_moves(piece.get_rank(), piece.get_file(), arg_board):
            moves.append(const.get_move_id([(piece.get_rank(), piece.get_file()), (move[0], move[1])]))
        return moves
    elif isinstance(piece, Rook.Rook):
        moves = []
        for move in straight_moves(piece.get_rank(), piece.get_file(), arg_board):
            moves.append(const.get_move_id([(piece.get_rank(), piece.get_file()), (move[0], move[1])]))
        return moves
    elif isinstance(piece, Pawn.Pawn):
        moves = []
        for move in pawn_moves(piece.get_rank(), piece.get_file(), arg_board):
            moves.append(const.get_move_id([(piece.get_rank(), piece.get_file()), (move[0], move[1])]))
        return moves
    else:
        return []
