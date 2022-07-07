import Piece.Piece as Piece


class Rook(Piece.Piece):
    def __init__(self, rank, file, color):
        super().__init__(rank, file, color)

    def get_alpha(self):
        if self.color == "white":
            return "wR"
        elif self.color == "black":
            return "bR"
        else:
            raise Exception("Invalid color")
