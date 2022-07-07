import pygame
import board

WIDTH = HEIGHT = 400
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30
IMAGES = {}


def load_images():
    global IMAGES
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = pygame.image.load('Images/' + piece + '.png')
        IMAGES[piece] = pygame.transform.smoothscale(IMAGES[piece], (SQ_SIZE, SQ_SIZE))


def draw_squares(screen):
    colors = [(238, 238, 210), (118, 150, 86)]

    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[(i + j) % 2]
            pygame.draw.rect(screen, color, (j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, arg_board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = arg_board[i][j]
            if piece.get_alpha() != '--':
                screen.blit(IMAGES[piece.get_alpha()], pygame.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_game_state(screen, gs):
    draw_squares(screen)
    draw_pieces(screen, gs.board)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((255, 255, 255))
    clock = pygame.time.Clock()

    gs = board.GameState()
    load_images()

    square_selected = ()  # Stores the selected square (tuple: row, col)
    player_clicks = []  # Stores the last two squares clicked by the player [list: (from_row, from_col), (to_row, to_col)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # (x, y) location of mouse click
                x = pos[0] // SQ_SIZE
                y = pos[1] // SQ_SIZE

                if square_selected == (x, y):  # If the square is already selected, unselect it
                    square_selected = ()
                    player_clicks = []
                else:
                    square_selected = (x, y)
                    player_clicks.append(square_selected)

                if len(player_clicks) == 2:
                    move = board.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation(), end=' ')
                    gs.make_move(move)
                    player_clicks = []
                    square_selected = ()

        draw_game_state(screen, gs)
        pygame.display.update()
        clock.tick(MAX_FPS)


if __name__ == '__main__':
    main()
