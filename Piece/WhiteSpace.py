import Piece.Piece as Piece


class WhiteSpace(Piece.Piece):
    def __init__(self, rank, file):
        super().__init__(rank, file, None)

    @staticmethod
    def get_alpha():
        return "--"
