class Piece:
    def __init__(self, rank, file, color):
        self.rank = rank
        self.file = file
        self.color = color
        self.moved = False

    def get_rank(self):
        return self.rank

    def set_rank(self, rank):
        self.rank = rank

    def get_file(self):
        return self.file

    def set_file(self, file):
        self.file = file

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_moved(self):
        return self.moved

    def set_moved(self, moved):
        self.moved = moved
