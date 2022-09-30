# This class defines a 'Move' object responsible for identification, validation and execution of a move.
class Move:
    def __init__(self, start_pos, end_pos, board):
        self.start_rank = start_pos[0]
        self.start_file = start_pos[1]
        self.end_rank = end_pos[0]
        self.end_file = end_pos[1]
        self.move_type = None
        self.move_id = self.start_rank * 1000 + self.start_file * 100 + self.end_rank * 10 + self.end_file

        self.piece_moved = board[self.start_rank][self.start_file]
        self.piece_captured = board[self.end_rank][self.end_file]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_move_type(self):
        return self.move_type

    def set_move_type(self, move_type):
        self.move_type = move_type
