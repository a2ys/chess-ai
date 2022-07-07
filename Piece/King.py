import Piece.Piece as Piece


class King(Piece.Piece):
    def __init__(self, rank, file, color):
        super().__init__(rank, file, color)

    def get_alpha(self):
        if self.color == "white":
            return "wK"
        elif self.color == "black":
            return "bK"
        else:
            raise Exception("Invalid color")
