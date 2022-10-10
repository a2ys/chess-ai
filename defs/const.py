# Standard FEN Notation of initial board layout
import defs.ChessErrors

initial_board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# initial_board = "4k3/8/8/8/8/8/8/4K2Q w KQkq - 0 1"


# Pre-defined game constraints
WIDTH = HEIGHT = 720
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60
IMAGES = {}
PIECE_VALUES = {'K': 10000, 'Q': 900, 'R': 450, 'B': 350, 'N': 150, 'P': 100}
CHECKMATE = 100000
STALEMATE = 0

# Colors format - [LIGHT, DARK]
colors = [(238, 216, 192), (171, 122, 101)]
highlight_colors = [(207, 172, 106), (197, 173, 96)]
legal_move_colors = [(221, 89, 89), (197, 68, 79)]

# Original board colors
board_colors = [
    [colors[0], colors[1], colors[0], colors[1], colors[0], colors[1], colors[0], colors[1]],
    [colors[1], colors[0], colors[1], colors[0], colors[1], colors[0], colors[1], colors[0]],
    [colors[0], colors[1], colors[0], colors[1], colors[0], colors[1], colors[0], colors[1]],
    [colors[1], colors[0], colors[1], colors[0], colors[1], colors[0], colors[1], colors[0]],
    [colors[0], colors[1], colors[0], colors[1], colors[0], colors[1], colors[0], colors[1]],
    [colors[1], colors[0], colors[1], colors[0], colors[1], colors[0], colors[1], colors[0]],
    [colors[0], colors[1], colors[0], colors[1], colors[0], colors[1], colors[0], colors[1]],
    [colors[1], colors[0], colors[1], colors[0], colors[1], colors[0], colors[1], colors[0]]
]

# Backup of original board colors
original_colors = [
    [colors[0], colors[1], colors[0], colors[1], colors[0], colors[1], colors[0], colors[1]],
    [colors[1], colors[0], colors[1], colors[0], colors[1], colors[0], colors[1], colors[0]],
    [colors[0], colors[1], colors[0], colors[1], colors[0], colors[1], colors[0], colors[1]],
    [colors[1], colors[0], colors[1], colors[0], colors[1], colors[0], colors[1], colors[0]],
    [colors[0], colors[1], colors[0], colors[1], colors[0], colors[1], colors[0], colors[1]],
    [colors[1], colors[0], colors[1], colors[0], colors[1], colors[0], colors[1], colors[0]],
    [colors[0], colors[1], colors[0], colors[1], colors[0], colors[1], colors[0], colors[1]],
    [colors[1], colors[0], colors[1], colors[0], colors[1], colors[0], colors[1], colors[0]]
]

# Pre-defined error messages
fen_error = "Invalid character in FEN string."
invalid_fen_error = "Invalid FEN string."
color_error = "Invalid color value. Must be 'white' or 'black' (case-sensitive) only." \
              "To fix - Check all 'color' arguments of pieces in board.py.fen_to_board() method, or if you've defined the board.py by yourself, check the 'color' argument entered."
no_king_error = "No King was found in the FEN string. If not done by you, report to me at - oreus@duck.com"
king_captured_error = "The King was captured. There must be a bug, please report to me at - oreus@duck.com with full explanation of the moves you made."
invalid_move_identifier_error = "You provided an invalid move identifier."


# Method that returns a 2-D list from a 1-D list
def to_matrix(lst: list, number: int) -> list:
    return [lst[i:i + number] for i in range(0, len(lst), number)]


# Method that converts the position of a list to a single integer
def pos_to_index(pos: tuple) -> int:
    return pos[0] * 8 + pos[1]


# Method that converts the integer value of the position to a tuple
def index_to_pos(index: int) -> tuple:
    return index // 8, index % 8


# Method that returns the move ID of a move
def get_move_id(arg_move: list, spl_move_identifier: str = 'n') -> str:
    m_id = ""

    for i in arg_move:
        m_id += str(i[0]) + str(i[1])

    if spl_move_identifier.lower() in ['c', 'e', 'p', 'n']:
        m_id += spl_move_identifier.lower()
    else:
        raise defs.ChessErrors.InvalidMoveIdentifier(invalid_move_identifier_error)

    return m_id


# Method to compare two move IDs
def is_move_id_equal(move_id: str, all_move_id: list) -> bool:
    for m_id in all_move_id:
        if m_id[:-1] == move_id:
            return True
    return False


# Method to get the move type in various cases.
def get_move_type(move_id: str, all_move_id: list) -> str:
    for m_id in all_move_id:
        if m_id[:-1] == move_id:
            return m_id[-1]


# Method that returns the move from a move ID
def get_move_from_id(move_id: str) -> list:
    return [(int(move_id[0]), int(move_id[1])), (int(move_id[2]), int(move_id[3]))]


# Method that slices an integer value like a string does when sliced, upper limit is excluded
def slice_int(integer: int, start: int, end: int) -> int:
    return int(str(integer)[start:end])


# Method that filters out illegal moves from the pseudo-legal moves
def legal_moves(pseudo_legal_moves: list, illegal_moves: list) -> list:
    lgl_moves = pseudo_legal_moves
    for move in illegal_moves:
        if move in pseudo_legal_moves:
            lgl_moves.remove(move)
    return lgl_moves
