import piece.Piece as Piece
from defs.enums.Colors import Color


class WhiteSpace(Piece.Piece):
    def __init__(self, rank: int, file: int) -> None:
        super().__init__(rank, file, Color.EMPTY)

    @staticmethod
    def get_alpha() -> str:
        return "--"

    def print_info(self) -> None:
        super().print_info()
        print("Current square is a WhiteSpace")
