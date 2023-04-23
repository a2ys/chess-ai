import piece.Piece
from defs.enums.MoveType import MoveType


# This class defines a 'Move' object responsible for identification, validation and execution of a move.
class Move:
    def __init__(self, start_pos: tuple, end_pos: tuple, board: list) -> None:
        self.start_rank = start_pos[0]
        self.start_file = start_pos[1]
        self.end_rank = end_pos[0]
        self.end_file = end_pos[1]
        self.pos_tuple = ((self.start_rank, self.start_file), (self.end_rank, self.end_file))
        self.move_type = MoveType.NONE
        self.special_pos = ()

        self.piece_moved = board[self.start_rank][self.start_file]
        self.piece_captured = board[self.end_rank][self.end_file]

        self.extra_piece = None

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, self.__class__) and
                self.start_rank == other.start_rank and
                self.start_file == other.start_file and
                self.end_rank == other.end_rank and
                self.end_file == other.end_file)

        # If necessary, include below piece of code as well
        # self.move_type == other.move_type and
        # self.special_pos == other.special_pos and
        # self.piece_moved == other.piece_moved and
        # self.piece_captured == other.piece_captured and
        # self.extra_piece == other.extra_piece)

    def __hash__(self) -> int:
        # result = hash((self.start_rank, self.start_file, self.end_rank, self.end_file, self.piece_moved, self.piece_captured, self.extra_piece, self.move_type, self.special_pos))
        result = hash(
            (self.start_rank, self.start_file, self.end_rank, self.end_file, self.piece_moved, self.piece_captured))

        return result

    def get_move_type(self) -> MoveType:
        return self.move_type

    def set_move_type(self, move_type: MoveType) -> None:
        self.move_type = move_type

    def get_piece_moved(self) -> piece.Piece:
        return self.piece_moved

    def get_piece_captured(self) -> piece.Piece:
        return self.piece_captured

    def get_special_pos(self) -> tuple:
        return self.special_pos

    def set_special_pos(self, pos: tuple) -> None:
        self.special_pos = pos

    def get_extra_piece(self) -> piece.Piece:
        return self.extra_piece

    def set_extra_piece(self, extra_piece_object: piece.Piece) -> None:
        self.extra_piece = extra_piece_object

    def get_pos_tuple(self) -> tuple[tuple, tuple]:
        return self.pos_tuple

    def print_info(self) -> None:
        print(
            f"The piece {self.piece_moved.get_alpha()} moved from ({self.start_rank},{self.start_file}) to ({self.end_rank},{self.end_file}).")
