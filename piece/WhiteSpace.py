import piece.Piece as Piece


class WhiteSpace(Piece.Piece):
    def __init__(self, rank: int, file: int) -> None:
        super().__init__(rank, file, None)

    @staticmethod
    def get_alpha() -> str:
        return "--"

    def print_info(self) -> None:
        super().print_info()
        print("Current square is a white space")
