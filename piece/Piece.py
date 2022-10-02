# This is a piece class. Every piece inherits from this class.
# Every piece is initialized with a Rank, File and Color. There are getters and setters for every defined value, and a defined method to print all information in a structural manner.

class Piece:
    def __init__(self, rank: int, file: int, color: str) -> None:
        self.rank = rank
        self.file = file
        self.color = color
        self.move_history = []
        self.moved = False

    def get_rank(self) -> int:
        return self.rank

    def set_rank(self, rank: int) -> None:
        self.rank = rank

    def get_file(self) -> int:
        return self.file

    def set_file(self, file: int) -> None:
        self.file = file

    def get_color(self) -> str:
        return self.color

    def set_color(self, color: str) -> None:
        self.color = color

    def get_moved(self) -> bool:
        return self.moved

    def set_moved(self, moved: bool) -> None:
        self.moved = moved

    def get_move_history(self) -> list:
        return self.move_history

    def update_move_history(self, move: tuple) -> None:
        self.move_history.append(move)

    def undo_last_move(self):
        return self.move_history.pop()

    def print_info(self) -> None:
        print("Rank of the piece is: " + str(self.rank))
        print("File of the piece is: " + str(self.file))
        print("Color of the piece is: " + str(self.color))
        print(f"Has the piece moved? {'Yes' if self.moved else 'No'}")
