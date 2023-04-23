import pygame

import move
import move_generator
from defs import ChessErrors, Constants
from defs.enums.MoveType import MoveType
from defs.enums.Colors import Color
from piece import King, Queen, Bishop, Knight, Rook, Pawn, WhiteSpace
from piece.Piece import Piece


class GameState:
    def __init__(self) -> None:
        self.white_to_move = None
        self.move_check = False
        self.castle_rights = {Color.WHITE: [False, False],
                              Color.BLACK: [False, False]}  # 'color': [King-Side Castle, Queen-Side Castle]
        self.board = self.fen_to_board(Constants.initial_board)
        self.move_log = []
        self.white_king_position = (7, 4)
        self.black_king_position = (0, 4)
        
        pygame.init()        

    def fen_to_board(self, fen: str) -> list:
        fen_list = fen.split(' ')
        board = []
        rank, file = 0, 0

        if fen_list[1] == 'w':
            self.white_to_move = True
        elif fen_list[1] == 'b':
            self.white_to_move = False
        else:
            raise ChessErrors.InvalidFenError(Constants.fen_error)

        if fen_list[2] != '-':
            for rights in fen_list[2]:
                match rights:
                    case 'K':
                        self.castle_rights[Color.WHITE][0] = True
                    case 'Q':
                        self.castle_rights[Color.WHITE][1] = True
                    case 'k':
                        self.castle_rights[Color.BLACK][0] = True
                    case 'q':
                        self.castle_rights[Color.BLACK][1] = True
                    case _:
                        raise ChessErrors.InvalidFenError(Constants.fen_error)

        if ('K' not in fen_list[0]) or ('k' not in fen_list[0]):
            raise ChessErrors.NoKingError(Constants.no_king_error)

        for char in fen_list[0]:
            if char == '/':
                rank += 1
                file = 0
            elif char.isdigit():
                for _ in range(int(char)):
                    board.append(WhiteSpace.WhiteSpace(rank, file))
                    file += 1
            else:
                match char:
                    case 'K':
                        board.append(King.King(rank, file, Color.WHITE))
                    case 'Q':
                        board.append(Queen.Queen(rank, file, Color.WHITE))
                    case 'B':
                        board.append(Bishop.Bishop(rank, file, Color.WHITE))
                    case 'N':
                        board.append(Knight.Knight(rank, file, Color.WHITE))
                    case 'R':
                        board.append(Rook.Rook(rank, file, Color.WHITE))
                    case 'P':
                        board.append(Pawn.Pawn(rank, file, Color.WHITE))
                    case 'k':
                        board.append(King.King(rank, file, Color.BLACK))
                    case 'q':
                        board.append(Queen.Queen(rank, file, Color.BLACK))
                    case 'b':
                        board.append(Bishop.Bishop(rank, file, Color.BLACK))
                    case 'n':
                        board.append(Knight.Knight(rank, file, Color.BLACK))
                    case 'r':
                        board.append(Rook.Rook(rank, file, Color.BLACK))
                    case 'p':
                        board.append(Pawn.Pawn(rank, file, Color.BLACK))
                    case _:
                        raise ChessErrors.InvalidFenError(Constants.fen_error)
                file += 1

        if len(board) != 64:
            raise ChessErrors.InvalidFenError(Constants.invalid_fen_error)

        return Constants.to_matrix(board, 8)

    def make_move(self, given_move: move.Move, testing: bool = False) -> bool:
        if given_move.get_piece_moved().get_color() == given_move.get_piece_captured().get_color():  # If you are trying to overlap pieces, it will not be allowed.
            return False
        elif (given_move.get_piece_moved().get_color() == Color.WHITE and not self.white_to_move) or (given_move.get_piece_moved().get_color() == Color.BLACK and self.white_to_move):  # If it's not your move, it will not be allowed.
            return False
        else:
            # When you're not checking for legal moves, this piece of code will run.
            if not testing:
                # This piece of code will filter out illegal moves from pseudo-legal moves and give out a legal-move list
                piece = given_move.get_piece_moved()
                pseudo_legal_moves = move_generator.legal_moves(piece, self.board)
                legal_moves = self.legal_moves(pseudo_legal_moves).union(self.special_moves(piece))

                if isinstance(piece, Pawn.Pawn):
                    if piece.get_color() == Color.WHITE and given_move.end_rank == 0:
                        given_move.set_move_type(MoveType.PROMOTION)
                    elif piece.get_color() == Color.BLACK and given_move.end_rank == 7:
                        given_move.set_move_type(MoveType.PROMOTION)

                if given_move in legal_moves:  # If the move is legal, it will be executed.
                    if isinstance(given_move.piece_captured, King.King):
                        raise ChessErrors.KingCapturedError(Constants.king_captured_error)

                    piece.set_rank(given_move.end_rank)
                    piece.set_file(given_move.end_file)
                    self.board[given_move.end_rank][given_move.end_file] = piece
                    piece.update_move_history((given_move.end_rank, given_move.end_file))
                    self.board[given_move.start_rank][given_move.start_file] = WhiteSpace.WhiteSpace(given_move.start_file, given_move.start_rank)

                    given_move = self.refine_move(given_move)

                    match (given_move.get_move_type()):
                        case MoveType.CASTLE:
                            if given_move.end_file == 6:
                                self.board[given_move.start_rank][5] = self.board[given_move.start_rank][7]
                                self.board[given_move.start_rank][5].set_rank(given_move.start_rank)
                                self.board[given_move.start_rank][5].set_file(5)
                                self.board[given_move.start_rank][5].update_move_history((given_move.start_rank, 5))
                                print(self.board[given_move.start_rank][5].get_move_history())
                                self.board[given_move.start_rank][7] = WhiteSpace.WhiteSpace(given_move.start_rank, 7)
                                given_move.set_extra_piece(self.board[given_move.start_rank][5])
                                given_move.set_special_pos((given_move.start_rank, 7))
                            elif given_move.end_file == 2:
                                self.board[given_move.start_rank][3] = self.board[given_move.start_rank][0]
                                self.board[given_move.start_rank][3].set_rank(given_move.start_rank)
                                self.board[given_move.start_rank][3].set_file(3)
                                self.board[given_move.start_rank][3].update_move_history((given_move.start_rank, 3))
                                self.board[given_move.start_rank][0] = WhiteSpace.WhiteSpace(given_move.start_rank, 0)
                                given_move.set_extra_piece(self.board[given_move.start_rank][3])
                                given_move.set_special_pos((given_move.start_rank, 0))
                            self.move_log.append(given_move)
                        case MoveType.PROMOTION:
                            given_move.set_extra_piece(self.board[given_move.end_rank][given_move.end_file])
                            given_move.set_special_pos((given_move.start_rank, given_move.start_file))
                            self.board[given_move.end_rank][given_move.end_file] = Queen.Queen(given_move.end_rank, given_move.end_file, piece.get_color())

                            self.move_log.append(given_move)
                        case MoveType.EN_PASSANT:
                            if piece.get_color() == Color.WHITE:
                                given_move.set_extra_piece(self.board[given_move.end_rank + 1][given_move.end_file])
                                given_move.set_special_pos((given_move.start_rank, given_move.end_file))
                                self.board[given_move.end_rank + 1][given_move.end_file] = WhiteSpace.WhiteSpace(given_move.end_rank + 1, given_move.end_file)
                            elif piece.get_color() == Color.BLACK:
                                given_move.set_extra_piece(self.board[given_move.end_rank - 1][given_move.end_file])
                                given_move.set_special_pos((given_move.start_rank, given_move.end_file))
                                self.board[given_move.end_rank - 1][given_move.end_file] = WhiteSpace.WhiteSpace(given_move.end_rank - 1, given_move.end_file)
                            
                            self.move_log.append(given_move)
                        case MoveType.NORMAL:
                            self.move_log.append(given_move)
                        case MoveType.NONE:
                            raise ChessErrors.InvalidMoveIdentifier(Constants.invalid_move_identifier_error)

                    # If any of the kings were moved, update their positions.
                    if given_move.piece_moved.get_alpha() == "K":
                        self.white_king_position = (given_move.end_rank, given_move.end_file)
                    elif given_move.piece_moved.get_alpha() == "k":
                        self.black_king_position = (given_move.end_rank, given_move.end_file)

                    self.white_to_move = not self.white_to_move
                return True
            elif testing:
                piece = given_move.get_piece_moved()
                if given_move in move_generator.legal_moves(piece, self.board):  # If the move is legal, it will be executed.
                    piece.set_rank(given_move.end_rank)
                    piece.set_file(given_move.end_file)
                    self.board[given_move.end_rank][given_move.end_file] = piece
                    self.board[given_move.start_rank][given_move.start_file] = WhiteSpace.WhiteSpace(given_move.start_file, given_move.start_rank)
                    self.move_log.append(given_move)

                    # If any of the kings were moved, update their positions.
                    if piece.get_alpha() == "K":
                        self.white_king_position = (given_move.end_rank, given_move.end_file)
                    elif piece.get_alpha() == "k":
                        self.black_king_position = (given_move.end_rank, given_move.end_file)
                    self.white_to_move = not self.white_to_move
                return True
            else:
                return False

    def undo_move(self, testing: bool = False) -> bool:
        if len(self.move_log) > 0:
            last_move = self.move_log.pop()
            last_piece = last_move.get_piece_moved()

            last_piece.set_rank(last_move.start_rank)
            last_piece.set_file(last_move.start_file)
            self.board[last_move.start_rank][last_move.start_file] = last_piece

            if last_move.get_move_type() == MoveType.CASTLE:
                special_rank = last_move.get_special_pos()[0]
                special_file = last_move.get_special_pos()[1]
                special_piece = last_move.get_extra_piece()

                self.board[special_piece.get_rank()][special_piece.get_file()] = WhiteSpace.WhiteSpace(special_piece.get_rank(), special_piece.get_file())
                self.board[special_rank][special_file] = special_piece

                self.board[special_rank][special_file].set_rank(special_rank)
                self.board[special_rank][special_file].set_file(special_file)
                self.board[special_rank][special_file].undo_last_move()
            elif last_move.get_move_type() == MoveType.EN_PASSANT:
                special_piece = last_move.get_extra_piece()

                self.board[special_piece.get_rank()][special_piece.get_file()] = special_piece

            if not testing:
                last_piece.undo_last_move()
            
            self.board[last_move.end_rank][last_move.end_file] = last_move.get_piece_captured()

            if last_piece.get_alpha() == "K":
                self.white_king_position = (last_move.start_rank, last_move.start_file)
            elif last_piece.get_alpha() == "k":
                self.black_king_position = (last_move.start_rank, last_move.start_file)

            self.white_to_move = not self.white_to_move
            return True
        else:
            return False

    @staticmethod
    def refine_move(given_move: move.Move) -> move.Move:
        match (type(given_move.get_piece_moved())):
            case King.King:
                if given_move.get_pos_tuple() in Constants.CASTLES:
                    given_move.set_move_type(MoveType.CASTLE)

                    return given_move
            case Pawn.Pawn:
                if given_move.get_pos_tuple() in Constants.EN_PASSANTS:
                    given_move.set_move_type(MoveType.EN_PASSANT)

                    return given_move

        if given_move.move_type == MoveType.NONE:
            given_move.set_move_type(MoveType.NORMAL)

        return given_move

    def is_square_under_attack(self, rank: int, file: int) -> bool:
        piece = self.board[rank][file]

        # DIAGONAL
        for i in range(rank + 1, 8):
            if file + (i - rank) <= 7:
                if isinstance(self.board[i][file + (i - rank)], WhiteSpace.WhiteSpace):
                    continue
                elif (isinstance(self.board[i][file + (i - rank)], Queen.Queen) or isinstance(self.board[i][file + (i - rank)], Bishop.Bishop)) and self.board[i][file + (i - rank)].get_color() != piece.get_color():
                    return True
                else:
                    break

        for i in range(rank + 1, 8):
            if file - (i - rank) >= 0:
                if isinstance(self.board[i][file - (i - rank)], WhiteSpace.WhiteSpace):
                    continue
                elif (isinstance(self.board[i][file - (i - rank)], Queen.Queen) or isinstance(self.board[i][file - (i - rank)], Bishop.Bishop)) and self.board[i][file - (i - rank)].get_color() != piece.get_color():
                    return True
                else:
                    break

        for i in range(rank - 1, -1, -1):
            if file + (rank - i) <= 7:
                if isinstance(self.board[i][file + (rank - i)], WhiteSpace.WhiteSpace):
                    continue
                elif (isinstance(self.board[i][file + (rank - i)], Queen.Queen) or isinstance(self.board[i][file + (rank - i)], Bishop.Bishop)) and self.board[i][file + (rank - i)].get_color() != piece.get_color():
                    return True
                else:
                    break

        for i in range(rank - 1, -1, -1):
            if file - (rank - i) >= 0:
                if isinstance(self.board[i][file - (rank - i)], WhiteSpace.WhiteSpace):
                    continue
                elif (isinstance(self.board[i][file - (rank - i)], Queen.Queen) or isinstance(self.board[i][file - (rank - i)], Bishop.Bishop)) and self.board[i][file - (rank - i)].get_color() != piece.get_color():
                    return True
                else:
                    break

        # STRAIGHT
        for i in range(rank + 1, 8):
            if isinstance(self.board[i][file], WhiteSpace.WhiteSpace):
                continue
            elif (isinstance(self.board[i][file], Queen.Queen) or isinstance(self.board[i][file], Rook.Rook)) and self.board[i][file].get_color() != piece.get_color():
                return True
            else:
                break

        for i in range(rank - 1, -1, -1):
            if isinstance(self.board[i][file], WhiteSpace.WhiteSpace):
                continue
            elif (isinstance(self.board[i][file], Queen.Queen) or isinstance(self.board[i][file], Rook.Rook)) and self.board[i][file].get_color() != piece.get_color():
                return True
            else:
                break

        for i in range(file + 1, 8):
            if isinstance(self.board[rank][i], WhiteSpace.WhiteSpace):
                continue
            elif (isinstance(self.board[rank][i], Queen.Queen) or isinstance(self.board[rank][i], Rook.Rook)) and self.board[rank][i].get_color() != piece.get_color():
                return True
            else:
                break

        for i in range(file - 1, -1, -1):
            if isinstance(self.board[rank][i], WhiteSpace.WhiteSpace):
                continue
            elif (isinstance(self.board[rank][i], Queen.Queen) or isinstance(self.board[rank][i], Rook.Rook)) and self.board[rank][i].get_color() != piece.get_color():
                return True
            else:
                break

        # PAWN
        if self.board[rank][file].get_color() == Color.WHITE:
            if rank > 0:
                if file - 1 >= 0:
                    if self.board[rank - 1][file - 1].get_color() == Color.BLACK and isinstance(self.board[rank - 1][file - 1], Pawn.Pawn):
                        return True
                if file + 1 <= 7:
                    if self.board[rank - 1][file + 1].get_color() == Color.BLACK and isinstance(self.board[rank - 1][file + 1], Pawn.Pawn):
                        return True
        else:
            if rank < 7:
                if file - 1 >= 0:
                    if self.board[rank + 1][file - 1].get_color() == Color.WHITE and isinstance(self.board[rank + 1][file - 1], Pawn.Pawn):
                        return True
                if file + 1 <= 7:
                    if self.board[rank + 1][file + 1].get_color() == Color.WHITE and isinstance(self.board[rank + 1][file + 1], Pawn.Pawn):
                        return True

        # KNIGHT
        if file + 2 <= 7:
            if rank + 1 <= 7:
                if isinstance(self.board[rank + 1][file + 2], Knight.Knight) and self.board[rank + 1][file + 2].get_color() != piece.get_color():
                    return True
            if rank - 1 >= 0:
                if isinstance(self.board[rank - 1][file + 2], Knight.Knight) and self.board[rank - 1][file + 2].get_color() != piece.get_color():
                    return True
        if file - 2 >= 0:
            if rank + 1 <= 7:
                if isinstance(self.board[rank + 1][file - 2], Knight.Knight) and self.board[rank + 1][file - 2].get_color() != piece.get_color():
                    return True
            if rank - 1 >= 0:
                if isinstance(self.board[rank - 1][file - 2], Knight.Knight) and self.board[rank - 1][file - 2].get_color() != piece.get_color():
                    return True
        if rank + 2 <= 7:
            if file + 1 <= 7:
                if isinstance(self.board[rank + 2][file + 1], Knight.Knight) and self.board[rank + 2][file + 1].get_color() != piece.get_color():
                    return True
            if file - 1 >= 0:
                if isinstance(self.board[rank + 2][file - 1], Knight.Knight) and self.board[rank + 2][file - 1].get_color() != piece.get_color():
                    return True
        if rank - 2 >= 0:
            if file + 1 <= 7:
                if isinstance(self.board[rank - 2][file + 1], Knight.Knight) and self.board[rank - 2][file + 1].get_color() != piece.get_color():
                    return True
            if file - 1 >= 0:
                if isinstance(self.board[rank - 2][file - 1], Knight.Knight) and self.board[rank - 2][file - 1].get_color() != piece.get_color():
                    return True

        # KING
        if file + 1 <= 7:
            if rank + 1 <= 7:
                if isinstance(self.board[rank + 1][file + 1], King.King) and self.board[rank + 1][file + 1].get_color() != piece.get_color():
                    return True
            if rank - 1 >= 0:
                if isinstance(self.board[rank - 1][file + 1], King.King) and self.board[rank - 1][file + 1].get_color() != piece.get_color():
                    return True
        if file - 1 >= 0:
            if rank + 1 <= 7:
                if isinstance(self.board[rank + 1][file - 1], King.King) and self.board[rank + 1][file - 1].get_color() != piece.get_color():
                    return True
            if rank - 1 >= 0:
                if isinstance(self.board[rank - 1][file - 1], King.King) and self.board[rank - 1][file - 1].get_color() != piece.get_color():
                    return True
        if rank + 1 <= 7:
            if isinstance(self.board[rank + 1][file], King.King) and self.board[rank + 1][file].get_color() != piece.get_color():
                return True
        if rank - 1 >= 0:
            if isinstance(self.board[rank - 1][file], King.King) and self.board[rank - 1][file].get_color() != piece.get_color():
                return True
        if file + 1 <= 7:
            if isinstance(self.board[rank][file + 1], King.King) and self.board[rank][file + 1].get_color() != piece.get_color():
                return True
        if file - 1 >= 0:
            if isinstance(self.board[rank][file - 1], King.King) and self.board[rank][file - 1].get_color() != piece.get_color():
                return True

        return False

    def is_whitespace_under_attack(self, rank: int, file: int, friendly_color: Color) -> bool:
        # DIAGONAL
        for i in range(rank + 1, 8):
            if file + (i - rank) <= 7:
                if isinstance(self.board[i][file + (i - rank)], WhiteSpace.WhiteSpace):
                    continue
                elif (isinstance(self.board[i][file + (i - rank)], Queen.Queen) or isinstance(self.board[i][file + (i - rank)], Bishop.Bishop)) and self.board[i][file + (i - rank)].get_color() != friendly_color:
                    return True
                else:
                    break

        for i in range(rank + 1, 8):
            if file - (i - rank) >= 0:
                if isinstance(self.board[i][file - (i - rank)], WhiteSpace.WhiteSpace):
                    continue
                elif (isinstance(self.board[i][file - (i - rank)], Queen.Queen) or isinstance(self.board[i][file - (i - rank)], Bishop.Bishop)) and self.board[i][file - (i - rank)].get_color() != friendly_color:
                    return True
                else:
                    break

        for i in range(rank - 1, -1, -1):
            if file + (rank - i) <= 7:
                if isinstance(self.board[i][file + (rank - i)], WhiteSpace.WhiteSpace):
                    continue
                elif (isinstance(self.board[i][file + (rank - i)], Queen.Queen) or isinstance(self.board[i][file + (rank - i)], Bishop.Bishop)) and self.board[i][file + (rank - i)].get_color() != friendly_color:
                    return True
                else:
                    break

        for i in range(rank - 1, -1, -1):
            if file - (rank - i) >= 0:
                if isinstance(self.board[i][file - (rank - i)], WhiteSpace.WhiteSpace):
                    continue
                elif (isinstance(self.board[i][file - (rank - i)], Queen.Queen) or isinstance(self.board[i][file - (rank - i)], Bishop.Bishop)) and self.board[i][file - (rank - i)].get_color() != friendly_color:
                    return True
                else:
                    break

        # STRAIGHT
        for i in range(rank + 1, 8):
            if isinstance(self.board[i][file], WhiteSpace.WhiteSpace):
                continue
            elif (isinstance(self.board[i][file], Queen.Queen) or isinstance(self.board[i][file], Rook.Rook)) and self.board[i][file].get_color() != friendly_color:
                return True
            else:
                break

        for i in range(rank - 1, -1, -1):
            if isinstance(self.board[i][file], WhiteSpace.WhiteSpace):
                continue
            elif (isinstance(self.board[i][file], Queen.Queen) or isinstance(self.board[i][file], Rook.Rook)) and self.board[i][file].get_color() != friendly_color:
                return True
            else:
                break

        for i in range(file + 1, 8):
            if isinstance(self.board[rank][i], WhiteSpace.WhiteSpace):
                continue
            elif (isinstance(self.board[rank][i], Queen.Queen) or isinstance(self.board[rank][i], Rook.Rook)) and self.board[rank][i].get_color() != friendly_color:
                return True
            else:
                break

        for i in range(file - 1, -1, -1):
            if isinstance(self.board[rank][i], WhiteSpace.WhiteSpace):
                continue
            elif (isinstance(self.board[rank][i], Queen.Queen) or isinstance(self.board[rank][i], Rook.Rook)) and self.board[rank][i].get_color() != friendly_color:
                return True
            else:
                break

        # PAWN
        if self.board[rank][file].get_color() == Color.WHITE:
            if rank > 0:
                if file - 1 >= 0:
                    if self.board[rank - 1][file - 1].get_color() == Color.BLACK and isinstance(self.board[rank - 1][file - 1], Pawn.Pawn):
                        return True
                if file + 1 <= 7:
                    if self.board[rank - 1][file + 1].get_color() == Color.BLACK and isinstance(self.board[rank - 1][file + 1], Pawn.Pawn):
                        return True
        else:
            if rank < 7:
                if file - 1 >= 0:
                    if self.board[rank + 1][file - 1].get_color() == Color.WHITE and isinstance(self.board[rank + 1][file - 1], Pawn.Pawn):
                        return True
                if file + 1 <= 7:
                    if self.board[rank + 1][file + 1].get_color() == Color.WHITE and isinstance(self.board[rank + 1][file + 1], Pawn.Pawn):
                        return True

        # KNIGHT
        if file + 2 <= 7:
            if rank + 1 <= 7:
                if isinstance(self.board[rank + 1][file + 2], Knight.Knight) and self.board[rank + 1][file + 2].get_color() != friendly_color:
                    return True
            if rank - 1 >= 0:
                if isinstance(self.board[rank - 1][file + 2], Knight.Knight) and self.board[rank - 1][file + 2].get_color() != friendly_color:
                    return True
        if file - 2 >= 0:
            if rank + 1 <= 7:
                if isinstance(self.board[rank + 1][file - 2], Knight.Knight) and self.board[rank + 1][file - 2].get_color() != friendly_color:
                    return True
            if rank - 1 >= 0:
                if isinstance(self.board[rank - 1][file - 2], Knight.Knight) and self.board[rank - 1][file - 2].get_color() != friendly_color:
                    return True
        if rank + 2 <= 7:
            if file + 1 <= 7:
                if isinstance(self.board[rank + 2][file + 1], Knight.Knight) and self.board[rank + 2][file + 1].get_color() != friendly_color:
                    return True
            if file - 1 >= 0:
                if isinstance(self.board[rank + 2][file - 1], Knight.Knight) and self.board[rank + 2][file - 1].get_color() != friendly_color:
                    return True
        if rank - 2 >= 0:
            if file + 1 <= 7:
                if isinstance(self.board[rank - 2][file + 1], Knight.Knight) and self.board[rank - 2][file + 1].get_color() != friendly_color:
                    return True
            if file - 1 >= 0:
                if isinstance(self.board[rank - 2][file - 1], Knight.Knight) and self.board[rank - 2][file - 1].get_color() != friendly_color:
                    return True

        # KING
        if file + 1 <= 7:
            if rank + 1 <= 7:
                if isinstance(self.board[rank + 1][file + 1], King.King) and self.board[rank + 1][file + 1].get_color() != friendly_color:
                    return True
            if rank - 1 >= 0:
                if isinstance(self.board[rank - 1][file + 1], King.King) and self.board[rank - 1][file + 1].get_color() != friendly_color:
                    return True
        if file - 1 >= 0:
            if rank + 1 <= 7:
                if isinstance(self.board[rank + 1][file - 1], King.King) and self.board[rank + 1][file - 1].get_color() != friendly_color:
                    return True
            if rank - 1 >= 0:
                if isinstance(self.board[rank - 1][file - 1], King.King) and self.board[rank - 1][file - 1].get_color() != friendly_color:
                    return True
        if rank + 1 <= 7:
            if isinstance(self.board[rank + 1][file], King.King) and self.board[rank + 1][file].get_color() != friendly_color:
                return True
        if rank - 1 >= 0:
            if isinstance(self.board[rank - 1][file], King.King) and self.board[rank - 1][file].get_color() != friendly_color:
                return True
        if file + 1 <= 7:
            if isinstance(self.board[rank][file + 1], King.King) and self.board[rank][file + 1].get_color() != friendly_color:
                return True
        if file - 1 >= 0:
            if isinstance(self.board[rank][file - 1], King.King) and self.board[rank][file - 1].get_color() != friendly_color:
                return True

        return False

    def special_moves(self, piece: Piece) -> set:
        special_move_set = set()

        board = self.get_board()
        rank = piece.get_rank()
        file = piece.get_file()

        if self.active_player() == piece.get_color():
            
            # CASTLE
            if isinstance(piece, King.King) and not piece.move_history:
                if not self.in_check(self.active_player()):
                    if piece.get_color() == Color.WHITE:
                        if self.castle_rights[Color.WHITE][0]:
                            if isinstance(board[7][7], Rook.Rook) and not board[7][7].move_history:
                                if isinstance(board[7][6], WhiteSpace.WhiteSpace):
                                    if isinstance(board[7][5], WhiteSpace.WhiteSpace):
                                        if not self.is_whitespace_under_attack(7, 6, piece.get_color()) and not self.is_whitespace_under_attack(7, 5, piece.get_color()):
                                            special_move = move.Move((7, 4), (7, 6), board)
                                            special_move.set_move_type(MoveType.CASTLE)
                                            special_move_set.add(special_move)
                        if self.castle_rights[Color.WHITE][1]:
                            if isinstance(board[7][0], Rook.Rook) and not board[7][0].move_history:
                                if isinstance(board[7][1], WhiteSpace.WhiteSpace):
                                    if isinstance(board[7][2], WhiteSpace.WhiteSpace):
                                        if isinstance(board[7][3], WhiteSpace.WhiteSpace):
                                            if not self.is_whitespace_under_attack(7, 1, piece.get_color()) and not self.is_whitespace_under_attack(7, 2, piece.get_color()) and not self.is_whitespace_under_attack(7, 3, piece.get_color()):
                                                special_move = move.Move((7, 4), (7, 2), board)
                                                special_move.set_move_type(MoveType.CASTLE)
                                                special_move_set.add(special_move)
                    if piece.get_color() == Color.BLACK:
                        if self.castle_rights[Color.BLACK][0]:
                            if isinstance(board[0][7], Rook.Rook) and not board[0][7].move_history:
                                if isinstance(board[0][6], WhiteSpace.WhiteSpace):
                                    if isinstance(board[0][5], WhiteSpace.WhiteSpace):
                                        if not self.is_whitespace_under_attack(0, 6, piece.get_color()) and not self.is_whitespace_under_attack(0, 5, piece.get_color()):
                                            special_move = move.Move((0, 4), (0, 6), board)
                                            special_move.set_move_type(MoveType.CASTLE)
                                            special_move_set.add(special_move)
                        if self.castle_rights[Color.WHITE][1]:
                            if isinstance(board[0][0], Rook.Rook) and not board[7][0].move_history:
                                if isinstance(board[0][1], WhiteSpace.WhiteSpace):
                                    if isinstance(board[0][2], WhiteSpace.WhiteSpace):
                                        if isinstance(board[0][3], WhiteSpace.WhiteSpace):
                                            if not self.is_whitespace_under_attack(0, 1, piece.get_color()) and not self.is_whitespace_under_attack(0, 2, piece.get_color()) and not self.is_whitespace_under_attack(0, 3, piece.get_color()):
                                                special_move = move.Move((0, 4), (0, 2), board)
                                                special_move.set_move_type(MoveType.CASTLE)
                                                special_move_set.add(special_move)

            # EN-PASSANT
            # TODO: Fix the bug in FEN "k7/6p1/8/q4P1K/8/8/8/8 b KQkq - 0 1"
            if len(self.move_log) > 0:
                if isinstance(piece, Pawn.Pawn):
                    if piece.color == Color.WHITE and piece.get_rank() == 3:
                        if file > 0:
                            enemy = self.board[rank][file - 1]
                            if isinstance(enemy, Pawn.Pawn) and self.move_log[-1].piece_moved == enemy:
                                if len(enemy.get_move_history()) == 1:
                                    special_move = move.Move((rank, file), (rank - 1, file - 1), board)
                                    special_move.set_move_type(MoveType.EN_PASSANT)
                                    special_move_set.add(special_move)
                        if file < 7:
                            enemy = self.board[rank][file + 1]
                            if isinstance(enemy, Pawn.Pawn) and self.move_log[-1].piece_moved == enemy:
                                if len(enemy.get_move_history()) == 1:
                                    special_move = move.Move((rank, file), (rank - 1, file + 1), board)
                                    special_move.set_move_type(MoveType.EN_PASSANT)
                                    special_move_set.add(special_move)
                    elif piece.color == Color.BLACK and piece.get_rank() == 4:
                        if file > 0:
                            enemy = self.board[rank][file - 1]
                            if isinstance(enemy, Pawn.Pawn) and self.move_log[-1].piece_moved == enemy:
                                if len(enemy.get_move_history()) == 1:
                                    special_move = move.Move((rank, file), (rank + 1, file - 1), board)
                                    special_move.set_move_type(MoveType.EN_PASSANT)
                                    special_move_set.add(special_move)
                        if file < 7:
                            enemy = self.board[rank][file + 1]
                            if isinstance(enemy, Pawn.Pawn) and self.move_log[-1].piece_moved == enemy:
                                if len(enemy.get_move_history()) == 1:
                                    special_move = move.Move((rank, file), (rank + 1, file + 1), board)
                                    special_move.set_move_type(MoveType.EN_PASSANT)
                                    special_move_set.add(special_move)

        return special_move_set

    def in_check(self, color: Color) -> bool:
        if color == Color.WHITE:
            king_position = self.white_king_position
        else:
            king_position = self.black_king_position

        return self.is_square_under_attack(king_position[0], king_position[1])

    def is_checkmate(self, color: Color) -> bool:
        if self.in_check(color):
            for rank in self.board:
                for piece in rank:
                    if piece.get_color() == color:
                        if self.legal_moves(move_generator.legal_moves(piece, self.board)):
                            return False
            return True
        else:
            return False

    def is_stalemate(self, color: Color) -> bool:
        if not self.in_check(color):
            for rank in self.board:
                for piece in rank:
                    if piece.get_color() == color:
                        if self.legal_moves(move_generator.legal_moves(piece, self.board)):
                            return False
            return True
        else:
            return False

    def legal_moves(self, pseudo_legal_moves: set) -> set:
        legal_moves = set()

        for pseudo_legal_move in pseudo_legal_moves:
            self.make_move(pseudo_legal_move, True)
            if not self.in_check(self.opponent()):
                legal_moves.add(pseudo_legal_move)
            self.undo_move(True)

        return legal_moves

    def get_board(self) -> list:
        return self.board

    def set_board(self, board: list) -> None:
        self.board = board

    def active_player(self) -> Color:
        return Color.WHITE if self.white_to_move else Color.BLACK

    def opponent(self) -> Color:
        return Color.BLACK if self.white_to_move else Color.WHITE
