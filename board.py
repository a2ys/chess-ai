import pygame
import time

import move
import moves
from defs import const, ChessErrors
from piece import Piece, King, Queen, Bishop, Knight, Rook, Pawn, WhiteSpace


class GameState:
    def __init__(self) -> None:
        self.white_to_move = None
        self.move_check = False
        self.castle_rights = {'white': [False, False],
                              'black': [False, False]}  # 'color': [King-Side Castle, Queen-Side Castle]
        self.board = self.fen_to_board(const.initial_board)
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
            raise ChessErrors.InvalidFenError(const.fen_error)

        if fen_list[2] != '-':
            for rights in fen_list[2]:
                match rights:
                    case 'K':
                        self.castle_rights['white'][0] = True
                    case 'Q':
                        self.castle_rights['white'][1] = True
                    case 'k':
                        self.castle_rights['black'][0] = True
                    case 'q':
                        self.castle_rights['black'][1] = True
                    case _:
                        raise ChessErrors.InvalidFenError(const.fen_error)

        if ('K' not in fen_list[0]) or ('k' not in fen_list[0]):
            raise ChessErrors.NoKingError(const.no_king_error)

        for char in fen_list[0]:
            if char == '/':
                rank += 1
                file = 0
            elif char.isdigit():
                for i in range(int(char)):
                    board.append(WhiteSpace.WhiteSpace(rank, file))
                    file += 1
            else:
                match char:
                    case 'K':
                        board.append(King.King(rank, file, "white"))
                    case 'Q':
                        board.append(Queen.Queen(rank, file, "white"))
                    case 'B':
                        board.append(Bishop.Bishop(rank, file, "white"))
                    case 'N':
                        board.append(Knight.Knight(rank, file, "white"))
                    case 'R':
                        board.append(Rook.Rook(rank, file, "white"))
                    case 'P':
                        board.append(Pawn.Pawn(rank, file, "white"))
                    case 'k':
                        board.append(King.King(rank, file, "black"))
                    case 'q':
                        board.append(Queen.Queen(rank, file, "black"))
                    case 'b':
                        board.append(Bishop.Bishop(rank, file, "black"))
                    case 'n':
                        board.append(Knight.Knight(rank, file, "black"))
                    case 'r':
                        board.append(Rook.Rook(rank, file, "black"))
                    case 'p':
                        board.append(Pawn.Pawn(rank, file, "black"))
                    case _:
                        raise ChessErrors.InvalidFenError(const.fen_error)
                file += 1

        if len(board) != 64:
            raise ChessErrors.InvalidFenError(const.invalid_fen_error)
        return const.to_matrix(board, 8)

    def make_move(self, given_move: move.Move, testing: bool = False, sound: bool = True) -> bool:
        if self.board[given_move.start_rank][given_move.start_file].color == self.board[given_move.end_rank][given_move.end_file].color:  # If you are trying to overlap pieces, it will not be allowed.
            return False
        elif (self.board[given_move.start_rank][given_move.start_file].color == "white" and not self.white_to_move) or (self.board[given_move.start_rank][given_move.start_file].color == "black" and self.white_to_move):  # If it's not your move, it will not be allowed.
            return False
        else:
            # When you're not checking for legal moves, this piece of code will run.
            if not testing:
                # This piece of code will filter out illegal moves from pseudo-legal moves and give out a legal-move list
                piece = self.board[given_move.start_rank][given_move.start_file]
                pseudo_legal_moves = moves.legal_moves(piece, self.board)
                legal_moves = self.legal_moves(pseudo_legal_moves) + self.special_moves(piece)
                move_id = const.get_move_id([(given_move.start_rank, given_move.start_file), (given_move.end_rank, given_move.end_file)])
                is_legal = const.is_move_id_equal(move_id[:-1], legal_moves)

                if isinstance(piece, Pawn.Pawn):
                    if piece.get_color().lower() == 'white' and given_move.end_rank == 0:
                        for i in range(len(legal_moves)):
                            legal_moves[i] = legal_moves[i][:-1] + 'p'
                    elif piece.get_color().lower() == 'black' and given_move.end_rank == 7:
                        for i in range(len(legal_moves)):
                            legal_moves[i] = legal_moves[i][:-1] + 'p'

                if is_legal:  # If the move is legal, it will be executed.
                    self.board[given_move.end_rank][given_move.end_file] = self.board[given_move.start_rank][given_move.start_file]
                    self.board[given_move.end_rank][given_move.end_file].set_rank(given_move.end_rank)
                    self.board[given_move.end_rank][given_move.end_file].set_file(given_move.end_file)
                    self.board[given_move.end_rank][given_move.end_file].update_move_history((given_move.end_rank, given_move.end_file))
                    self.board[given_move.start_rank][given_move.start_file] = WhiteSpace.WhiteSpace(given_move.start_file, given_move.start_rank)

                    match const.get_move_type(move_id[:-1], legal_moves).lower():
                        case 'c':
                            given_move.set_move_type('c')

                            if given_move.start_file - given_move.end_file < 0:
                                self.board[given_move.end_rank][5] = self.board[given_move.end_rank][7]
                                self.board[given_move.end_rank][5].set_rank(given_move.end_rank)
                                self.board[given_move.end_rank][5].set_file(5)
                                self.board[given_move.end_rank][5].update_move_history((given_move.end_rank, 5))
                                self.board[given_move.end_rank][7] = WhiteSpace.WhiteSpace(given_move.end_rank, 7)
                                given_move.set_special_pos((given_move.end_rank, 7))
                                given_move.set_extra_piece(self.board[given_move.end_rank][5])

                            elif given_move.start_file - given_move.end_file > 0:
                                self.board[given_move.end_rank][3] = self.board[given_move.end_rank][0]
                                self.board[given_move.end_rank][3].set_rank(given_move.end_rank)
                                self.board[given_move.end_rank][3].set_file(3)
                                self.board[given_move.end_rank][3].update_move_history((given_move.end_rank, 3))
                                self.board[given_move.end_rank][0] = WhiteSpace.WhiteSpace(given_move.end_rank, 0)
                                given_move.set_special_pos((given_move.end_rank, 0))
                                given_move.set_extra_piece(self.board[given_move.end_rank][3])

                            self.move_log.append(given_move)
                        case 'e':
                            given_move.set_move_type('e')

                            if piece.get_color().lower() == 'white':
                                given_move.set_extra_piece(self.board[given_move.end_rank + 1][given_move.end_file])
                                given_move.set_special_pos((given_move.start_rank, given_move.end_file))
                                self.board[given_move.end_rank + 1][given_move.end_file] = WhiteSpace.WhiteSpace(given_move.end_rank + 1, given_move.end_file)
                            elif piece.get_color().lower() == 'black':
                                given_move.set_extra_piece(self.board[given_move.end_rank - 1][given_move.end_file])
                                given_move.set_special_pos((given_move.start_rank, given_move.end_file))
                                self.board[given_move.end_rank - 1][given_move.end_file] = WhiteSpace.WhiteSpace(given_move.end_rank - 1, given_move.end_file)

                            self.move_log.append(given_move)
                        case 'p':
                            given_move.set_move_type('p')

                            given_move.set_extra_piece(self.board[given_move.end_rank][given_move.end_file])
                            given_move.set_special_pos((given_move.start_rank, given_move.start_file))
                            self.board[given_move.end_rank][given_move.end_file] = Queen.Queen(given_move.end_rank, given_move.end_file, piece.get_color())

                            self.move_log.append(given_move)
                        case 'n':
                            given_move.set_move_type('n')

                            self.move_log.append(given_move)
                        case _:
                            ChessErrors.InvalidMoveIdentifier(const.invalid_move_identifier_error)

                    if given_move.piece_captured.get_alpha() == 'wK' or given_move.piece_captured.get_alpha() == 'bK':
                        raise ChessErrors.KingCapturedError(const.king_captured_error)

                    # If any of the kings were moved, update their positions.
                    if given_move.piece_moved.get_alpha() == "wK":
                        self.white_king_position = (given_move.end_rank, given_move.end_file)
                    elif given_move.piece_moved.get_alpha() == "bK":
                        self.black_king_position = (given_move.end_rank, given_move.end_file)

                    self.white_to_move = not self.white_to_move

                    if sound:
                        if not self.is_stalemate(self.active_player()):
                            if self.in_check(self.active_player()):
                                if self.is_checkmate(self.active_player()):
                                    if given_move.piece_captured.get_alpha() != "--":  # If you captured a piece and delivered a checkmate, it will be a capture and checkmate sound.
                                        pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/capture_and_checkmate.mp3"))
                                    elif given_move.piece_captured.get_alpha() == "--":  # If you just delivered a checkmate, it will be executed with a checkmate sound.
                                        if given_move.get_move_type() == 'e':
                                            pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/capture_and_checkmate.mp3"))
                                        else:
                                            pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/move_and_checkmate.mp3"))
                                else:  # If you just delivered a check, it will be executed with a check sound.
                                    pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/check.wav"))
                            else:
                                if given_move.piece_captured.get_alpha() != "--":  # If you captured a piece, it will be executed with a capture sound.
                                    pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/capture.wav"))
                                elif given_move.piece_captured.get_alpha() == "--":  # If you made a normal move, it will be executed with a normal sound.
                                    if given_move.get_move_type() == 'e':
                                        pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/capture.wav"))
                                    elif given_move.get_move_type() == 'c':
                                        pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/castle.mp3"))
                                    else:
                                        pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/normal.wav"))
                        elif self.is_stalemate(self.active_player()):  # If the opponent was stalemated, it will be executed with a stalemate sound.
                            pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/stalemate.mp3"))
                return True
            elif testing:
                if const.get_move_id([(given_move.start_rank, given_move.start_file), (given_move.end_rank, given_move.end_file)]) in moves.legal_moves(self.board[given_move.start_rank][given_move.start_file], self.board):  # If the move is legal, it will be executed.
                    self.board[given_move.end_rank][given_move.end_file] = self.board[given_move.start_rank][given_move.start_file]
                    self.board[given_move.end_rank][given_move.end_file].set_rank(given_move.end_rank)
                    self.board[given_move.end_rank][given_move.end_file].set_file(given_move.end_file)
                    self.board[given_move.start_rank][given_move.start_file] = WhiteSpace.WhiteSpace(given_move.start_file, given_move.start_rank)
                    self.move_log.append(given_move)

                    # If any of the kings were moved, update their positions.
                    if given_move.piece_moved.get_alpha() == "wK":
                        self.white_king_position = (given_move.end_rank, given_move.end_file)
                    elif given_move.piece_moved.get_alpha() == "bK":
                        self.black_king_position = (given_move.end_rank, given_move.end_file)
                    self.white_to_move = not self.white_to_move
                return True
            else:
                return False

    def in_check(self, color: str) -> bool:
        if color == "white":
            king_position = self.white_king_position
        else:
            king_position = self.black_king_position
        if self.is_square_under_attack(king_position[0], king_position[1]):
            return True
        else:
            return False

    def active_player(self) -> str:
        if self.white_to_move:
            return "white"
        else:
            return "black"

    def opponent(self) -> str:
        if self.white_to_move:
            return "black"
        else:
            return "white"

    def is_square_under_attack(self, rank: int, file: int) -> bool:
        for row in self.board:
            for piece in row:
                if piece.get_alpha() != "--" and piece.get_color() != self.board[rank][file].get_color():
                    temp = str(rank) + str(file)
                    for k in moves.legal_moves(piece, self.board):
                        if temp == k[2:4]:
                            return True
        return False

    def undo_move(self, testing: bool = False) -> bool:
        if len(self.move_log) > 0:
            last_move = self.move_log.pop()
            self.board[last_move.start_rank][last_move.start_file] = last_move.piece_moved
            self.board[last_move.start_rank][last_move.start_file].set_rank(last_move.start_rank)
            self.board[last_move.start_rank][last_move.start_file].set_file(last_move.start_file)
            if last_move.get_move_type() == 'c':
                special_rank = last_move.get_special_pos()[0]
                special_file = last_move.get_special_pos()[1]
                special_piece = last_move.get_extra_piece()

                self.board[special_piece.get_rank()][special_piece.get_file()] = WhiteSpace.WhiteSpace(special_piece.get_rank(), special_piece.get_file())
                self.board[special_rank][special_file] = special_piece

                self.board[special_rank][special_file].set_rank(special_rank)
                self.board[special_rank][special_file].set_file(special_file)
                self.board[special_rank][special_file].undo_last_move()
            if last_move.get_move_type() == 'e':
                special_piece = last_move.get_extra_piece()

                self.board[special_piece.get_rank()][special_piece.get_file()] = special_piece
            if not testing:
                self.board[last_move.start_rank][last_move.start_file].undo_last_move()
            self.board[last_move.end_rank][last_move.end_file] = last_move.piece_captured
            if last_move.piece_moved.get_alpha() == "wK":
                self.white_king_position = (last_move.start_rank, last_move.start_file)
            elif last_move.piece_moved.get_alpha() == "bK":
                self.black_king_position = (last_move.start_rank, last_move.start_file)
            self.white_to_move = not self.white_to_move
            return True
        else:
            return False

    def legal_moves(self, pseudo_legal: list) -> list:
        legal_moves_list = pseudo_legal
        for i in range(len(legal_moves_list) - 1, -1, -1):
            false_move = move.Move(const.get_move_from_id(legal_moves_list[i])[0], const.get_move_from_id(legal_moves_list[i])[1], self.board)
            active = self.active_player()
            self.make_move(false_move, True)

            if self.in_check(active):
                legal_moves_list.pop(i)
            self.undo_move(True)
        return legal_moves_list

    def is_checkmate(self, color: str) -> bool:
        available_moves = []
        if self.in_check(color):
            for rank in self.board:
                for piece in rank:
                    if piece.get_color() == color:
                        pseudo_legal_moves = moves.legal_moves(piece, self.board)
                        legal_moves = self.legal_moves(pseudo_legal_moves)
                        available_moves += legal_moves

                        if available_moves:
                            return False
            return True
        else:
            return False

    def is_stalemate(self, color: str) -> bool:
        available_moves = []
        if not self.in_check(color):
            for rank in self.board:
                for piece in rank:
                    if piece.get_color() == color:
                        pseudo_legal_moves = moves.legal_moves(piece, self.board)
                        legal_moves = self.legal_moves(pseudo_legal_moves)
                        available_moves += legal_moves

                        if available_moves:
                            return False
            return True
        else:
            return False

    def is_pos_under_attack(self, opponent_color: str, pos: tuple) -> bool:
        for rank in self.board:
            for piece in rank:
                if piece.get_color() == opponent_color:
                    legal_moves = moves.legal_moves(piece, self.board)
                    for legal_move in legal_moves:
                        if legal_move[-3:-1] == (str(pos[0]) + str(pos[1])):
                            return True
        return False

    def special_moves(self, piece: Piece) -> list:
        special_move_list = []
        # Castling
        rank = piece.get_rank()
        file = piece.get_file()
        if not self.in_check(self.active_player()):
            if isinstance(piece, King.King) and not piece.get_move_history():
                if piece.get_color().lower() == 'white' and (piece.get_rank(), piece.get_file()) == (7, 4):
                    if self.castle_rights['white'][1]:
                        if isinstance(self.board[rank][file - 3], WhiteSpace.WhiteSpace) and isinstance(self.board[rank][file - 2], WhiteSpace.WhiteSpace) and isinstance(self.board[rank][file - 1], WhiteSpace.WhiteSpace):
                            if not isinstance(self.board[rank][file - 4], WhiteSpace.WhiteSpace):
                                if not self.board[rank][file - 4].get_move_history():
                                    if not self.is_pos_under_attack(self.opponent(), (rank, file - 2)) and not self.is_pos_under_attack(self.opponent(), (rank, file - 1)):
                                        special_move = [(rank, file), (rank, file - 2)]
                                        special_move_list += [const.get_move_id(special_move, 'c')]
                    if self.castle_rights['white'][0]:
                        if isinstance(self.board[rank][file + 1], WhiteSpace.WhiteSpace) and isinstance(self.board[rank][file + 2], WhiteSpace.WhiteSpace):
                            if not isinstance(self.board[rank][file + 3], WhiteSpace.WhiteSpace):
                                if not self.board[rank][file + 3].get_move_history():
                                    if not self.is_pos_under_attack(self.opponent(), (rank, file + 1)) and not self.is_pos_under_attack(self.opponent(), (rank, file + 2)):
                                        special_move = [(rank, file), (rank, file + 2)]
                                        special_move_list += [const.get_move_id(special_move, 'c')]
                elif piece.get_color().lower() == 'black' and (piece.get_rank(), piece.get_file()) == (0, 4):
                    if self.castle_rights['black'][1]:
                        if isinstance(self.board[rank][file - 3], WhiteSpace.WhiteSpace) and isinstance(self.board[rank][file - 2], WhiteSpace.WhiteSpace) and isinstance(self.board[rank][file - 1], WhiteSpace.WhiteSpace):
                            if not isinstance(self.board[rank][file - 4], WhiteSpace.WhiteSpace):
                                if not self.board[rank][file - 4].get_move_history():
                                    if not self.is_pos_under_attack(self.opponent(), (rank, file - 2)) and not self.is_pos_under_attack(self.opponent(), (rank, file - 1)):
                                        special_move = [(rank, file), (rank, file - 2)]
                                        special_move_list += [const.get_move_id(special_move, 'c')]
                    if self.castle_rights['black'][0]:
                        if isinstance(self.board[rank][file + 1], WhiteSpace.WhiteSpace) and isinstance(self.board[rank][file + 2], WhiteSpace.WhiteSpace):
                            if not isinstance(self.board[rank][file + 3], WhiteSpace.WhiteSpace):
                                if not self.board[rank][file + 3].get_move_history():
                                    if not self.is_pos_under_attack(self.opponent(), (rank, file + 1)) and not self.is_pos_under_attack(self.opponent(), (rank, file + 2)):
                                        special_move = [(rank, file), (rank, file + 2)]
                                        special_move_list += [const.get_move_id(special_move, 'c')]

            if isinstance(piece, Pawn.Pawn):
                # En-passant
                if piece.get_color().lower() == 'white' and piece.get_rank() == 3:
                    if file > 0:
                        if isinstance(self.board[rank][file - 1], Pawn.Pawn) and len(self.board[rank][file - 1].get_move_history()) == 1:
                            if len(self.move_log) > 0 and self.move_log[-1].piece_moved == self.board[rank][file - 1]:
                                special_move = [(rank, file), (rank - 1, file - 1)]
                                special_move_list += [const.get_move_id(special_move, 'e')]
                    if file < 7:
                        if isinstance(self.board[rank][file + 1], Pawn.Pawn) and len(self.board[rank][file + 1].get_move_history()) == 1:
                            if len(self.move_log) > 0 and self.move_log[-1].piece_moved == self.board[rank][file + 1]:
                                special_move = [(rank, file), (rank - 1, file + 1)]
                                special_move_list += [const.get_move_id(special_move, 'e')]
                elif piece.get_color().lower() == 'black' and piece.get_rank() == 4:
                    if file > 0:
                        if isinstance(self.board[rank][file - 1], Pawn.Pawn) and len(self.board[rank][file - 1].get_move_history()) == 1:
                            if len(self.move_log) > 0 and self.move_log[-1].piece_moved == self.board[rank][file - 1]:
                                special_move = [(rank, file), (rank + 1, file - 1)]
                                special_move_list += [const.get_move_id(special_move, 'e')]
                    if file < 7:
                        if isinstance(self.board[rank][file + 1], Pawn.Pawn) and len(self.board[rank][file + 1].get_move_history()) == 1:
                            if len(self.move_log) > 0 and self.move_log[-1].piece_moved == self.board[rank][file + 1]:
                                special_move = [(rank, file), (rank + 1, file + 1)]
                                special_move_list += [const.get_move_id(special_move, 'e')]
        return special_move_list
