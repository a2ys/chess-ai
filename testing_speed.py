import time
import board
import moves
from defs import const
from piece import Pawn

gs = board.GameState()

start = time.time()

legal_moves = []
for i in gs.board:
    for j in i:
        lgl_moves = const.legal_moves(moves.legal_moves(j, gs.board), gs.legal_moves(j)) + gs.special_moves(j)
        legal_moves += lgl_moves
end = time.time()

print(f"It took {end-start} seconds to search normally.")

pieces = [(Pawn.Pawn(i, j, "white" if (i+j) % 2 == 0 else "black") for j in range(8)) for i in range(8)]
gs.board = pieces
start = time.time()
for i in pieces:
    for j in i:
        gs.legal_moves(j)
    print()
end = time.time()
