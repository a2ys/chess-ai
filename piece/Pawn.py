import piece.Piece as Piece
from defs import ChessErrors, const


class Pawn(Piece.Piece):
    def __init__(self, rank: int, file: int, color: str) -> None:
        super().__init__(rank, file, color)

    def get_alpha(self) -> str:
        if self.color == "white":
            return "wp"
        elif self.color == "black":
            return "bp"
        else:
            raise ChessErrors.InvalidColorError(const.color_error)

    def print_info(self) -> None:
        super().print_info()
        print("Type of the piece is: Pawn")
