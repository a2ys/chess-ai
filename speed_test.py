import numpy
import time

import moves
from piece import Pawn

board = [[Pawn.Pawn(rank, file, "white") for file in range(8)] for rank in range(8)]
numpy_board = numpy.array(board)

start = time.time()
for parent in range(1000):
    for i in range(len(board)):
        for j in range(len(board[i])):
            moves.legal_moves(board[i][j], board)

print(f"It took {time.time() - start} seconds to access every element of normal array.")

start = time.time()
for parent in range(1000):
    for i in range(len(board)):
        for j in range(len(board[i])):
            moves.legal_moves(numpy_board[i][j], numpy_board)

print(f"It took {time.time() - start} seconds to access every element of numpy array.")

print(numpy_board.shape)
