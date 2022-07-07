import defs
from Piece import King, Queen, Bishop, Knight, Rook, Pawn, WhiteSpace


class GameState:
    def __init__(self):
        self.board = self.fen_to_board(defs.initial_board)
        self.white_to_move = True
        self.move_log = []

    def fen_to_board(self, fen):
        fen_list = fen.split(' ')
        board = []
        file, rank = 0, 7

        if fen_list[1] == 'w':
            self.white_to_move = True
        else:
            self.white_to_move = False

        for i in fen_list[0]:
            if i == "/":
                file = 0
                rank -= 1
            elif i.isdigit():
                for j in range(int(i)):
                    board.append(WhiteSpace.WhiteSpace(file, rank))
                    file += 1
            elif i.isalpha():
                if i == "K":
                    board.append(King.King(file, rank, "white"))
                elif i == "Q":
                    board.append(Queen.Queen(file, rank, "white"))
                elif i == "B":
                    board.append(Bishop.Bishop(file, rank, "white"))
                elif i == "N":
                    board.append(Knight.Knight(file, rank, "white"))
                elif i == "R":
                    board.append(Rook.Rook(file, rank, "white"))
                elif i == "P":
                    board.append(Pawn.Pawn(file, rank, "white"))
                elif i == "k":
                    board.append(King.King(file, rank, "black"))
                elif i == "q":
                    board.append(Queen.Queen(file, rank, "black"))
                elif i == "b":
                    board.append(Bishop.Bishop(file, rank, "black"))
                elif i == "n":
                    board.append(Knight.Knight(file, rank, "black"))
                elif i == "r":
                    board.append(Rook.Rook(file, rank, "black"))
                elif i == "p":
                    board.append(Pawn.Pawn(file, rank, "black"))
                file += 1

        return defs.to_matrix(board, 8)

    def make_move(self, move):
        if isinstance(self.board[move.start_row][move.start_col], WhiteSpace.WhiteSpace):
            return
        elif self.board[move.end_row][move.end_col].color == self.board[move.start_row][move.start_col].color:
            return
        else:
            self.board[move.start_row][move.start_col] = WhiteSpace.WhiteSpace(move.start_col, move.start_row)
            self.board[move.end_row][move.end_col] = move.piece_moved
            move.piece_moved.set_moved(True)
            self.move_log.append(move)
            self.white_to_move = not self.white_to_move


class Move:
    ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[1]
        self.start_col = start_square[0]
        self.end_row = end_square[1]
        self.end_col = end_square[0]

        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_taken = board[self.end_row][self.end_col]

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]
