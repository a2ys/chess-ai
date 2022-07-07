import Piece.Piece as Piece


class Bishop(Piece.Piece):
    def __init__(self, rank, file, color):
        super().__init__(rank, file, color)

    def get_alpha(self):
        if self.color == "white":
            return "wB"
        elif self.color == "black":
            return "bB"
        else:
            raise Exception("Invalid color")
