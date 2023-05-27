"""
Main file:
    * Handling input
    * Displaying Game State obj
"""

import pygame as pg
import engine

WIDTH = HEIGHT = 512  # of the board
DIMENSION = 8  # is a 8x8 board
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animation

IMAGES = {

}

'''
Just load images one time 
(since loading for every frame will make the game lag)
'''


def load_image():
    pieces = ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']
    for p in pieces:
        # load images and scale them
        IMAGES[p] = pg.transform.scale(pg.image.load("./images/" + p + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


# draw squares on the board
def draw_board(screen):
    clrs = [pg.Color("White"), pg.Color("Gray")]
    for row in range(DIMENSION):  # 1 -> 8 for better view
        for col in range(DIMENSION):
            color = clrs[((row + col) % 2)]
            pg.draw.rect(screen, color, pg.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


# draw chess pieces on the board based on game state
def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != '__':  # blank square
                screen.blit(IMAGES[piece], pg.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clk = pg.time.Clock()
    screen.fill(pg.Color("White"))

    # init game state
    gs = engine.GameState()

    # load images
    load_image()
    square_selected = ()  # keep track of last click of user (row, col)
    clicks = []  # keep track of player clicks, contains two tuples
    running = True

    valid_moves = gs.gen_valid_moves()
    move_made = False  # flag to determine whether it is necessary to gen_valid_moves() or not

    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

            # Handler for mouse event
            elif e.type == pg.MOUSEBUTTONDOWN:

                # to determine which block that mouse clicked, need to get grounded result when calculating location

                location = pg.mouse.get_pos()  # get mouse position
                col = location[0] // SQUARE_SIZE  # grounded division
                row = location[1] // SQUARE_SIZE

                # check if player click on the same piece again
                if square_selected == (row, col):
                    # if true, reset all
                    square_selected = ()
                    clicks = []
                else:
                    square_selected = (row, col)
                    clicks.append(square_selected)
                if len(clicks) == 2:
                    new_move = engine.Move(clicks[0], clicks[1], gs.board)
                    for i in range(len(valid_moves)):
                        if new_move == valid_moves[i]:
                            gs.make_a_move(valid_moves[i])
                            print(new_move.get_chess_notation())
                            move_made = True
                            # reset
                            square_selected = ()
                            clicks = []
                    if not move_made:
                        # in case player click on one piece first, then click on other piece
                        clicks = [square_selected]
                # check if there is a second click saved in clicks -> move the piece
                # need to check if the first click is a piece

            # Handler for keyboard event
            elif e.type == pg.KEYDOWN:
                # press z -> undo move
                if e.key == pg.K_z:
                    gs.undo_move()
                    move_made = True

        if move_made:
            valid_moves = gs.gen_valid_moves()
            move_made = False

        draw_game_state(screen, gs)
        clk.tick(MAX_FPS)
        pg.display.flip()
        if gs.check_mate:
            if gs.white_move:
                player_color = "black"
            else:
                player_color = "white"
            print("Player " + player_color + " win")
        elif gs.stale_mate:
            print("Stale mate. Game drawn.")


if __name__ == "__main__":
    main()
