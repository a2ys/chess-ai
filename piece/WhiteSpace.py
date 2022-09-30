import piece.Piece as Piece


class WhiteSpace(Piece.Piece):
    def __init__(self, rank, file):
        super().__init__(rank, file, None)

    @staticmethod
    def get_alpha():
        return "--"

    def print_info(self):
        super().print_info()
        print("Current square is a white space")
