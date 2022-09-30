import pygame

import move
import moves
from defs import const, ChessErrors
from piece import King, Queen, Bishop, Knight, Rook, Pawn, WhiteSpace


class GameState:
    def __init__(self):
        self.white_to_move = False
        self.move_check = False
        self.board = self.fen_to_board(const.initial_board)
        self.move_log = []
        self.white_king_position = (7, 4)
        self.black_king_position = (0, 4)
        pygame.init()

    # This method converts the FEN string to a board of list data type using the 'to_matrix()' method.
    def fen_to_board(self, fen):
        fen_list = fen.split(' ')
        board = []
        rank, file = 0, 0

        if fen_list[1] == 'w':
            self.white_to_move = True
        else:
            self.white_to_move = False

        if ('K' not in fen_list[0]) or ('k' not in fen_list[0]):
            raise ChessErrors.NoKingError(const.no_king_error)

        for char in fen_list[0]:
            if char == '/':
                rank += 1
                file = 0
            elif char.isdigit():
                for i in range(int(char)):
                    board.append(WhiteSpace.WhiteSpace(file, rank))
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

    def make_move(self, given_move, testing=False):
        if self.board[given_move.start_rank][given_move.start_file].color == self.board[given_move.end_rank][given_move.end_file].color:  # If you are trying to overlap pieces, it will not be allowed.
            return False
        elif (self.board[given_move.start_rank][given_move.start_file].color == "white" and not self.white_to_move) or (self.board[given_move.start_rank][given_move.start_file].color == "black" and self.white_to_move):  # If it's not your move, it will not be allowed.
            return False
        else:
            # When you're not checking for legal moves, this piece of code will run.
            if not testing:
                # This piece of code will filter out illegal moves from pseudo-legal moves and give out a legal-move list
                pseudo_legal_moves = moves.legal_moves(self.board[given_move.start_rank][given_move.start_file], self.board)
                piece = self.board[given_move.start_rank][given_move.start_file]
                legal_moves = const.legal_moves(pseudo_legal_moves, self.illegal_moves(piece))

                if const.get_move_id([(given_move.start_rank, given_move.start_file), (given_move.end_rank, given_move.end_file)]) in legal_moves:  # If the move is legal, it will be executed.
                    self.board[given_move.end_rank][given_move.end_file] = self.board[given_move.start_rank][given_move.start_file]
                    self.board[given_move.end_rank][given_move.end_file].set_rank(given_move.end_rank)
                    self.board[given_move.end_rank][given_move.end_file].set_file(given_move.end_file)
                    self.board[given_move.start_rank][given_move.start_file] = WhiteSpace.WhiteSpace(given_move.start_file, given_move.start_rank)
                    self.move_log.append(given_move)

                    if given_move.piece_captured.get_alpha() == 'wK' or given_move.piece_captured.get_alpha() == 'bK':
                        raise ChessErrors.KingCapturedError(const.king_captured_error)

                    # If any of the kings were moved, update their positions.
                    if given_move.piece_moved.get_alpha() == "wK":
                        self.white_king_position = (given_move.end_rank, given_move.end_file)
                    elif given_move.piece_moved.get_alpha() == "bK":
                        self.black_king_position = (given_move.end_rank, given_move.end_file)

                    if self.active_player() == "white":
                        if self.in_check("black"):
                            pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/check.wav"))
                        else:
                            if given_move.piece_captured.get_alpha() != "--":  # If you captured a piece, it will be executed with a capture sound.
                                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/capture.wav"))
                            elif given_move.piece_captured.get_alpha() == "--":  # If you made a normal move, it will be executed with a normal sound.
                                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/normal.wav"))
                    elif self.active_player() == "black":
                        if self.in_check("white"):
                            pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/check.wav"))
                        else:
                            if given_move.piece_captured.get_alpha() != "--":
                                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/capture.wav"))
                            elif given_move.piece_captured.get_alpha() == "--":
                                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/normal.wav"))
                    self.white_to_move = not self.white_to_move
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

    def in_check(self, color):
        if color == "white":
            king_position = self.white_king_position
        else:
            king_position = self.black_king_position
        if self.is_square_under_attack(king_position[0], king_position[1]):
            return True
        else:
            return False

    def active_player(self):
        if self.white_to_move:
            return "white"
        else:
            return "black"

    def is_square_under_attack(self, rank, file):
        for row in self.board:
            for piece in row:
                if piece.get_alpha() != "--":
                    if piece.get_color() != self.board[rank][file].get_color():
                        temp = str(rank) + str(file)
                        for k in moves.legal_moves(piece, self.board):
                            if temp == k[2:]:
                                return True
        return False

    def undo_move(self):
        if len(self.move_log) > 0:
            last_move = self.move_log.pop()
            self.board[last_move.start_rank][last_move.start_file] = last_move.piece_moved
            self.board[last_move.start_rank][last_move.start_file].set_rank(last_move.start_rank)
            self.board[last_move.start_rank][last_move.start_file].set_file(last_move.start_file)
            self.board[last_move.end_rank][last_move.end_file] = last_move.piece_captured
            if last_move.piece_moved.get_alpha() == "wK":
                self.white_king_position = (last_move.start_rank, last_move.start_file)
            elif last_move.piece_moved.get_alpha() == "bK":
                self.black_king_position = (last_move.start_rank, last_move.start_file)
            self.white_to_move = not self.white_to_move
            return True
        else:
            return False

    def illegal_moves(self, piece):
        wrong = []
        active = ""
        if piece.get_color() == self.active_player():
            for str_move in moves.legal_moves(piece, self.board):
                false_move = move.Move(const.get_move_from_id(str_move)[0], const.get_move_from_id(str_move)[1], self.board)
                active = self.active_player()
                self.make_move(false_move, True)
                if self.in_check(active):
                    wrong.append(str_move)
                self.undo_move()
        return wrong
