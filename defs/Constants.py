from defs.enums.GameModes import GameModes
from defs.enums.Colors import Color

initial_board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# initial_board = "k7/6p1/8/q4P1K/8/8/8/8 b KQkq - 0 1"

# Pre-defined game constraints
WIDTH = HEIGHT = 720
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60
IMAGES = {}
PIECE_VALUES = {'K': 20000, 'Q': 900, 'R': 500, 'B': 330, 'N': 320, 'P': 100}
CHECKMATE = 100000
STALEMATE = -100000
DEPTH = 2
GAME_MODE = GameModes.AI_VS_AI

# Special move tuples
CASTLES = {
    ((7, 4), (7, 6)),
    ((7, 4), (7, 2)),

    ((0, 4), (0, 6)),
    ((0, 4), (0, 2))
}

EN_PASSANTS = {
    ((3, 0), (2, 1)),
    ((3, 1), (2, 0)),
    ((3, 1), (2, 2)),
    ((3, 2), (2, 1)),
    ((3, 2), (2, 3)),
    ((3, 3), (2, 2)),
    ((3, 3), (2, 4)),
    ((3, 4), (2, 3)),
    ((3, 4), (2, 5)),
    ((3, 5), (2, 4)),
    ((3, 5), (2, 6)),
    ((3, 6), (2, 5)),
    ((3, 6), (2, 7)),
    ((3, 7), (2, 6)),

    ((4, 0), (5, 1)),
    ((4, 1), (5, 0)),
    ((4, 1), (5, 2)),
    ((4, 2), (5, 1)),
    ((4, 2), (5, 3)),
    ((4, 3), (5, 2)),
    ((4, 3), (5, 4)),
    ((4, 4), (5, 3)),
    ((4, 4), (5, 5)),
    ((4, 5), (5, 4)),
    ((4, 5), (5, 6)),
    ((4, 6), (5, 5)),
    ((4, 6), (5, 7)),
    ((4, 7), (5, 6))
}

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
color_error = "Invalid color value. Must be (case-sensitive) 'white' or 'black' only." \
              "To fix - Check all 'color' arguments of pieces in board.py.fen_to_board() method, or if you've defined the board.py by yourself, check the 'color' argument entered."
no_king_error = "No King was found in the FEN string. If not done by you, report to me at - oreus@duck.com"
king_captured_error = "The King was captured. There must be a bug, please report to me at - oreus@duck.com with full explanation of the moves you made."
invalid_move_identifier_error = "An invalid move identifier was provided."
invalid_game_mode_error = "An invalid game mode was provided."


# Returns a 2D Board array from a 1D continuous Board array
def to_matrix(lst: list, number: int) -> list:
    return [lst[i:i + number] for i in range(0, len(lst), number)]


# Returns an alphabet for every color, used in accessing piece icons
def get_color_alpha(color: Color) -> str:
    return "w" if color == Color.WHITE else "b"
