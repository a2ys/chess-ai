import piece.Piece as Piece
from defs import ChessErrors, Constants
from defs.enums.Colors import Color


class Pawn(Piece.Piece):
    def __init__(self, rank: int, file: int, color: Color) -> None:
        super().__init__(rank, file, color)

    def get_alpha(self) -> str:
        if self.color == Color.WHITE:
            return "P"
        elif self.color == Color.BLACK:
            return "p"
        else:
            raise ChessErrors.InvalidColorError(Constants.color_error)

    def print_info(self) -> None:
        super().print_info()
        print("Type of the piece is: Pawn")
