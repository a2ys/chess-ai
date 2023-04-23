import move
from defs.enums.Colors import Color
from piece import Piece, King, Queen, Bishop, Knight, Rook, Pawn, WhiteSpace


def diagonal_moves(rank: int, file: int, m_arg_board: list) -> set:
    start_pos = (rank, file)
    moves = set()

    for i in range(rank + 1, 8):
        if file + (i - rank) <= 7:
            if isinstance(m_arg_board[i][file + (i - rank)], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (i, file + (i - rank)), m_arg_board))
            elif m_arg_board[i][file + (i - rank)].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (i, file + (i - rank)), m_arg_board))
                break
            else:
                break

    for i in range(rank + 1, 8):
        if file - (i - rank) >= 0:
            if isinstance(m_arg_board[i][file - (i - rank)], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (i, file - (i - rank)), m_arg_board))
            elif m_arg_board[i][file - (i - rank)].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (i, file - (i - rank)), m_arg_board))
                break
            else:
                break

    for i in range(rank - 1, -1, -1):
        if file + (rank - i) <= 7:
            if isinstance(m_arg_board[i][file + (rank - i)], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (i, file + (rank - i)), m_arg_board))
            elif m_arg_board[i][file + (rank - i)].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (i, file + (rank - i)), m_arg_board))
                break
            else:
                break

    for i in range(rank - 1, -1, -1):
        if file - (rank - i) >= 0:
            if isinstance(m_arg_board[i][file - (rank - i)], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (i, file - (rank - i)), m_arg_board))
            elif m_arg_board[i][file - (rank - i)].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (i, file - (rank - i)), m_arg_board))
                break
            else:
                break

    return moves


def straight_moves(rank: int, file: int, m_arg_board: list) -> set:
    start_pos = (rank, file)
    moves = set()

    for i in range(rank + 1, 8):
        if isinstance(m_arg_board[i][file], WhiteSpace.WhiteSpace):
            moves.add(move.Move(start_pos, (i, file), m_arg_board))
        elif m_arg_board[i][file].get_color() != m_arg_board[rank][file].get_color():
            moves.add(move.Move(start_pos, (i, file), m_arg_board))
            break
        else:
            break

    for i in range(rank - 1, -1, -1):
        if isinstance(m_arg_board[i][file], WhiteSpace.WhiteSpace):
            moves.add(move.Move(start_pos, (i, file), m_arg_board))
        elif m_arg_board[i][file].get_color() != m_arg_board[rank][file].get_color():
            moves.add(move.Move(start_pos, (i, file), m_arg_board))
            break
        else:
            break

    for i in range(file + 1, 8):
        if isinstance(m_arg_board[rank][i], WhiteSpace.WhiteSpace):
            moves.add(move.Move(start_pos, (rank, i), m_arg_board))
        elif m_arg_board[rank][i].get_color() != m_arg_board[rank][file].get_color():
            moves.add(move.Move(start_pos, (rank, i), m_arg_board))
            break
        else:
            break

    for i in range(file - 1, -1, -1):
        if isinstance(m_arg_board[rank][i], WhiteSpace.WhiteSpace):
            moves.add(move.Move(start_pos, (rank, i), m_arg_board))
        elif m_arg_board[rank][i].get_color() != m_arg_board[rank][file].get_color():
            moves.add(move.Move(start_pos, (rank, i), m_arg_board))
            break
        else:
            break

    return moves


def pawn_moves(rank: int, file: int, m_arg_board: list) -> set:
    start_pos = (rank, file)
    moves = set()

    if m_arg_board[rank][file].get_color() == Color.WHITE:
        if rank > 0:
            if isinstance(m_arg_board[rank - 1][file], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (rank - 1, file), m_arg_board))
            if rank == 6:
                if isinstance(m_arg_board[rank - 1][file], WhiteSpace.WhiteSpace):
                    if isinstance(m_arg_board[rank - 2][file], WhiteSpace.WhiteSpace):
                        moves.add(move.Move(start_pos, (rank - 2, file), m_arg_board))
        if file - 1 >= 0:
            if m_arg_board[rank - 1][file - 1].get_color() == Color.BLACK:
                moves.add(move.Move(start_pos, (rank - 1, file - 1), m_arg_board))
        if file + 1 <= 7:
            if m_arg_board[rank - 1][file + 1].get_color() == Color.BLACK:
                moves.add(move.Move(start_pos, (rank - 1, file + 1), m_arg_board))
    else:
        if rank < 7:
            if isinstance(m_arg_board[rank + 1][file], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (rank + 1, file), m_arg_board))
            if rank == 1:
                if isinstance(m_arg_board[rank + 1][file], WhiteSpace.WhiteSpace):
                    if isinstance(m_arg_board[rank + 2][file], WhiteSpace.WhiteSpace):
                        moves.add(move.Move(start_pos, (rank + 2, file), m_arg_board))
        if file - 1 >= 0:
            if m_arg_board[rank + 1][file - 1].get_color() == Color.WHITE:
                moves.add(move.Move(start_pos, (rank + 1, file - 1), m_arg_board))
        if file + 1 <= 7:
            if m_arg_board[rank + 1][file + 1].get_color() == Color.WHITE:
                moves.add(move.Move(start_pos, (rank + 1, file + 1), m_arg_board))

    return moves


def knight_moves(rank: int, file: int, m_arg_board: list) -> set:
    start_pos = (rank, file)
    moves = set()

    if file + 2 <= 7:
        if rank + 1 <= 7:
            if isinstance(m_arg_board[rank + 1][file + 2], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (rank + 1, file + 2), m_arg_board))
            elif m_arg_board[rank + 1][file + 2].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (rank + 1, file + 2), m_arg_board))
        if rank - 1 >= 0:
            if isinstance(m_arg_board[rank - 1][file + 2], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (rank - 1, file + 2), m_arg_board))
            elif m_arg_board[rank - 1][file + 2].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (rank - 1, file + 2), m_arg_board))
    if file - 2 >= 0:
        if rank + 1 <= 7:
            if isinstance(m_arg_board[rank + 1][file - 2], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (rank + 1, file - 2), m_arg_board))
            elif m_arg_board[rank + 1][file - 2].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (rank + 1, file - 2), m_arg_board))
        if rank - 1 >= 0:
            if isinstance(m_arg_board[rank - 1][file - 2], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (rank - 1, file - 2), m_arg_board))
            elif m_arg_board[rank - 1][file - 2].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (rank - 1, file - 2), m_arg_board))
    if rank + 2 <= 7:
        if file + 1 <= 7:
            if isinstance(m_arg_board[rank + 2][file + 1], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (rank + 2, file + 1), m_arg_board))
            elif m_arg_board[rank + 2][file + 1].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (rank + 2, file + 1), m_arg_board))
        if file - 1 >= 0:
            if isinstance(m_arg_board[rank + 2][file - 1], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (rank + 2, file - 1), m_arg_board))
            elif m_arg_board[rank + 2][file - 1].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (rank + 2, file - 1), m_arg_board))
    if rank - 2 >= 0:
        if file + 1 <= 7:
            if isinstance(m_arg_board[rank - 2][file + 1], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (rank - 2, file + 1), m_arg_board))
            elif m_arg_board[rank - 2][file + 1].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (rank - 2, file + 1), m_arg_board))
        if file - 1 >= 0:
            if isinstance(m_arg_board[rank - 2][file - 1], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (rank - 2, file - 1), m_arg_board))
            elif m_arg_board[rank - 2][file - 1].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (rank - 2, file - 1), m_arg_board))

    return moves


def king_moves(rank: int, file: int, m_arg_board: list) -> set:
    start_pos = (rank, file)
    moves = set()

    if file + 1 <= 7:
        if rank + 1 <= 7:
            if isinstance(m_arg_board[rank + 1][file + 1], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (rank + 1, file + 1), m_arg_board))
            elif m_arg_board[rank + 1][file + 1].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (rank + 1, file + 1), m_arg_board))
        if rank - 1 >= 0:
            if isinstance(m_arg_board[rank - 1][file + 1], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (rank - 1, file + 1), m_arg_board))
            elif m_arg_board[rank - 1][file + 1].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (rank - 1, file + 1), m_arg_board))
    if file - 1 >= 0:
        if rank + 1 <= 7:
            if isinstance(m_arg_board[rank + 1][file - 1], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (rank + 1, file - 1), m_arg_board))
            elif m_arg_board[rank + 1][file - 1].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (rank + 1, file - 1), m_arg_board))
        if rank - 1 >= 0:
            if isinstance(m_arg_board[rank - 1][file - 1], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (rank - 1, file - 1), m_arg_board))
            elif m_arg_board[rank - 1][file - 1].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (rank - 1, file - 1), m_arg_board))
    if rank + 1 <= 7:
        if isinstance(m_arg_board[rank + 1][file], WhiteSpace.WhiteSpace):
            moves.add(move.Move(start_pos, (rank + 1, file), m_arg_board))
        elif m_arg_board[rank + 1][file].get_color() != m_arg_board[rank][file].get_color():
            moves.add(move.Move(start_pos, (rank + 1, file), m_arg_board))
    if rank - 1 >= 0:
        if isinstance(m_arg_board[rank - 1][file], WhiteSpace.WhiteSpace):
            moves.add(move.Move(start_pos, (rank - 1, file), m_arg_board))
        elif m_arg_board[rank - 1][file].get_color() != m_arg_board[rank][file].get_color():
            moves.add(move.Move(start_pos, (rank - 1, file), m_arg_board))
    if file + 1 <= 7:
        if isinstance(m_arg_board[rank][file + 1], WhiteSpace.WhiteSpace):
            moves.add(move.Move(start_pos, (rank, file + 1), m_arg_board))
        elif m_arg_board[rank][file + 1].get_color() != m_arg_board[rank][file].get_color():
            moves.add(move.Move(start_pos, (rank, file + 1), m_arg_board))
    if file - 1 >= 0:
        if isinstance(m_arg_board[rank][file - 1], WhiteSpace.WhiteSpace):
            moves.add(move.Move(start_pos, (rank, file - 1), m_arg_board))
        elif m_arg_board[rank][file - 1].get_color() != m_arg_board[rank][file].get_color():
            moves.add(move.Move(start_pos, (rank, file - 1), m_arg_board))

    return moves


def queen_moves(rank: int, file: int, m_arg_board: list) -> set:
    start_pos = (rank, file)
    moves = set()

    for i in range(rank + 1, 8):
        if file + (i - rank) <= 7:
            if isinstance(m_arg_board[i][file + (i - rank)], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (i, file + (i - rank)), m_arg_board))
            elif m_arg_board[i][file + (i - rank)].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (i, file + (i - rank)), m_arg_board))
                break
            else:
                break

    for i in range(rank + 1, 8):
        if file - (i - rank) >= 0:
            if isinstance(m_arg_board[i][file - (i - rank)], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (i, file - (i - rank)), m_arg_board))
            elif m_arg_board[i][file - (i - rank)].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (i, file - (i - rank)), m_arg_board))
                break
            else:
                break

    for i in range(rank - 1, -1, -1):
        if file + (rank - i) <= 7:
            if isinstance(m_arg_board[i][file + (rank - i)], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (i, file + (rank - i)), m_arg_board))
            elif m_arg_board[i][file + (rank - i)].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (i, file + (rank - i)), m_arg_board))
                break
            else:
                break

    for i in range(rank - 1, -1, -1):
        if file - (rank - i) >= 0:
            if isinstance(m_arg_board[i][file - (rank - i)], WhiteSpace.WhiteSpace):
                moves.add(move.Move(start_pos, (i, file - (rank - i)), m_arg_board))
            elif m_arg_board[i][file - (rank - i)].get_color() != m_arg_board[rank][file].get_color():
                moves.add(move.Move(start_pos, (i, file - (rank - i)), m_arg_board))
                break
            else:
                break

    for i in range(rank + 1, 8):
        if isinstance(m_arg_board[i][file], WhiteSpace.WhiteSpace):
            moves.add(move.Move(start_pos, (i, file), m_arg_board))
        elif m_arg_board[i][file].get_color() != m_arg_board[rank][file].get_color():
            moves.add(move.Move(start_pos, (i, file), m_arg_board))
            break
        else:
            break

    for i in range(rank - 1, -1, -1):
        if isinstance(m_arg_board[i][file], WhiteSpace.WhiteSpace):
            moves.add(move.Move(start_pos, (i, file), m_arg_board))
        elif m_arg_board[i][file].get_color() != m_arg_board[rank][file].get_color():
            moves.add(move.Move(start_pos, (i, file), m_arg_board))
            break
        else:
            break

    for i in range(file + 1, 8):
        if isinstance(m_arg_board[rank][i], WhiteSpace.WhiteSpace):
            moves.add(move.Move(start_pos, (rank, i), m_arg_board))
        elif m_arg_board[rank][i].get_color() != m_arg_board[rank][file].get_color():
            moves.add(move.Move(start_pos, (rank, i), m_arg_board))
            break
        else:
            break

    for i in range(file - 1, -1, -1):
        if isinstance(m_arg_board[rank][i], WhiteSpace.WhiteSpace):
            moves.add(move.Move(start_pos, (rank, i), m_arg_board))
        elif m_arg_board[rank][i].get_color() != m_arg_board[rank][file].get_color():
            moves.add(move.Move(start_pos, (rank, i), m_arg_board))
            break
        else:
            break

    return moves


def legal_moves(piece: Piece, arg_board: list) -> set:
    if isinstance(piece, King.King):
        return king_moves(piece.get_rank(), piece.get_file(), arg_board)
    elif isinstance(piece, Queen.Queen):
        return queen_moves(piece.get_rank(), piece.get_file(), arg_board)
    elif isinstance(piece, Bishop.Bishop):
        return diagonal_moves(piece.get_rank(), piece.get_file(), arg_board)
    elif isinstance(piece, Knight.Knight):
        return knight_moves(piece.get_rank(), piece.get_file(), arg_board)
    elif isinstance(piece, Rook.Rook):
        return straight_moves(piece.get_rank(), piece.get_file(), arg_board)
    elif isinstance(piece, Pawn.Pawn):
        return pawn_moves(piece.get_rank(), piece.get_file(), arg_board)
    else:
        return set()
