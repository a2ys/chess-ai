import Piece.Piece as Piece


class Knight(Piece.Piece):
    def __init__(self, rank, file, color):
        super().__init__(rank, file, color)

    def get_alpha(self):
        if self.color == "white":
            return "wN"
        elif self.color == "black":
            return "bN"
        else:
            raise Exception("Invalid color")
