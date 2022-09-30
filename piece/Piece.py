# This is a piece class. Every piece inherits from this class.
# Every piece is initialized with a Rank, File and Color. There are getters and setters for every defined value, and a defined method to print all information in a structural manner.

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

    def print_info(self):
        print("Rank of the piece is: " + str(self.rank))
        print("File of the piece is: " + str(self.file))
        print("Color of the piece is: " + str(self.color))
        print(f"Has the piece moved? {'Yes' if self.moved else 'No'}")
