initial_board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# initial_board = "3qk3/8/8/8/8/8/8/3K4 w KQkq - 0 1"

WIDTH = HEIGHT = 720
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60
IMAGES = {}

# Colors format - [LIGHT, DARK]
colors = [(238, 216, 192), (171, 122, 101)]
highlight_colors = [(207, 172, 106), (197, 173, 96)]
legal_move_colors = [(221, 89, 89), (197, 68, 79)]

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

fen_error = "Invalid character in FEN string."
invalid_fen_error = "Invalid FEN string."
color_error = "Invalid color value. Must be 'white' or 'black' (case-sensitive) only." \
              "To fix - Check all 'color' arguments of pieces in board.py.fen_to_board() method, or if you've defined the board.py by yourself, check the 'color' argument entered."
no_king_error = "No King was found in the FEN string. If not done by you, report to me at - oreus@duck.com"
king_captured_error = "The King was captured. There must be a bug, please report to me at - oreus@duck.com with full explaination of the moves you made."


def to_matrix(lst, number):
    return [lst[i:i + number] for i in range(0, len(lst), number)]


def pos_to_index(pos):
    return pos[0] * 8 + pos[1]


def index_to_pos(index):
    return [index // 8, index % 8]


def get_move_id(arg_move):
    m_id = ""

    for i in arg_move:
        m_id += str(i[0]) + str(i[1])

    return m_id


def get_move_from_id(move_id):
    return [(int(move_id[0]), int(move_id[1])), (int(move_id[2]), int(move_id[3]))]


def slice_int(integer, start, end):
    return int(str(integer)[start:end])


def legal_moves(pseudo_legal_moves, illegal_moves):
    lgl_moves = pseudo_legal_moves
    for move in illegal_moves:
        if move in pseudo_legal_moves:
            lgl_moves.remove(move)

    return lgl_moves
