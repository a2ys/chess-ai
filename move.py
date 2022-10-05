import piece.Piece


# This class defines a 'Move' object responsible for identification, validation and execution of a move.
class Move:
    def __init__(self, start_pos: tuple, end_pos: tuple, board: list) -> None:
        self.start_rank = start_pos[0]
        self.start_file = start_pos[1]
        self.end_rank = end_pos[0]
        self.end_file = end_pos[1]
        self.move_type = None
        self.special_pos = ()
        self.move_id = self.start_rank * 1000 + self.start_file * 100 + self.end_rank * 10 + self.end_file

        self.piece_moved = board[self.start_rank][self.start_file]
        self.piece_captured = board[self.end_rank][self.end_file]

        self.extra_piece = None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_move_type(self) -> str:
        return self.move_type

    def set_move_type(self, move_type: str) -> None:
        self.move_type = move_type

    def get_special_pos(self) -> tuple:
        return self.special_pos

    def set_special_pos(self, pos: tuple) -> None:
        self.special_pos = pos

    def get_extra_piece(self) -> piece.Piece:
        return self.extra_piece

    def set_extra_piece(self, extra_piece_object: piece.Piece) -> None:
        self.extra_piece = extra_piece_object

    def print_info(self) -> None:
        print(f"The piece {self.piece_moved.get_alpha()} moved from ({self.start_rank},{self.start_file}) to ({self.end_rank},{self.end_file}).")
