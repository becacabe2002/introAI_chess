"""
Main driver file.
Handling user input.
Displaying current GameStatus object.
"""

import pygame as p
import engine, ai_moves
import sys

WIDTH = HEIGHT = 512
DIMENSION = 8

SQUARE_SIZE = HEIGHT // DIMENSION

MAX_FPS = 15
    
IMAGES = {}


def load_images():
    """
    Initialize a global directory of images.
    This will be called exactly once in the main.
    """
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))
        
        
def main():
    """
    The main driver for our code.
    This will handle user input and updating the graphics.
    """
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = engine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False  # flag variable for when a move is made
    animate = False  # flag variable for when we should animate a move
    load_images()  # do this only once before while loop
    
    running = True
    # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    square_selected = ()
    player_clicks = []  # this will keep track of player clicks (two tuples)
    game_over = False

    player_one = True # if a human is playing white, then True, else False
    player_two = False # same as above but for black

    while running:
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)

        for e in p.event.get():  
            if e.type == p.QUIT:
                running = False
                p.quit()
                sys.exit()
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    location = p.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE
                    if square_selected == (row, col):  # user clicked the same square twice
                        square_selected = ()  # deselect
                        player_clicks = []  # clear clicks
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)  # append for both 1st and 2nd click
                    if len(player_clicks) == 2:  # after 2nd click
                        move = engine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                print(move.get_chess_notation())
                                game_state.make_move(valid_moves[i])
                                move_made = True
                                animate = True
                                square_selected = ()  # reset user clicks
                                player_clicks = [] 
                        if not move_made:
                            player_clicks = [square_selected]
            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when 'z' is pressed
                    game_state.undo_move()
                    move_made = True
                    animate = False
                    game_over = False
                if e.key == p.K_r:  # reset the board when 'r' is pressed
                    game_state = engine.GameState()
                    valid_moves = game_state.get_valid_moves()
                    move_made = False
                    animate = False
                    game_over = False
                    square_selected = ()
                    player_clicks = []
                
        # AI move finder
        if not game_over and not human_turn:
            ai_move = ai_moves.find_best_move_minmax(game_state, valid_moves)
            if ai_move is None:
                ai_move = ai_moves.find_random_move(valid_moves)
            game_state.make_move(ai_move)
            move_made = True
            animate = True

        if move_made:
            if animate:
                animate_move(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.get_valid_moves()
            move_made = False
            animate = False

        draw_game_state(screen, game_state, valid_moves, square_selected)

        if game_state.check_mate:
            game_over = True
            if game_state.white_to_move:
                draw_text(screen, 'Black wins by checkmate')
            else:
                draw_text(screen, 'White wins by checkmate')
        elif game_state.stale_mate:
            game_over = True
            draw_text(screen, 'Stalemate')

        clock.tick(MAX_FPS)
        p.display.flip()


def high_light_square(screen, game_state, valid_moves, square_selected):
    """
    Draw a highlighted square on the screen.
    """
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == ('w' if game_state.white_to_move else 'b'):
            # highlight selected square
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)  # transparency value -> 0 transparent; 255 opaque
            s.fill(p.Color("blue"))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            # highlight moves from that square
            s.fill(p.Color("yellow"))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col*SQUARE_SIZE, move.end_row*SQUARE_SIZE))


def draw_game_state(screen, game_state, valid_moves, square_selected):
    """
    Responsible for all the graphics within current game state.
    """
    draw_board(screen)  # draw squares on the board
    # add in piece highlighting or move suggestions (later)
    high_light_square(screen, game_state, valid_moves, square_selected)
    draw_pieces(screen, game_state.board)  # draw pieces on top of those squares


def draw_board(screen):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row+column) % 2)]
            p.draw.rect(screen, color, p.Rect(column*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    

def draw_pieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
         

def animate_move(move, screen, board, clock):
    """
    Animating a piece
    """
    global colors
    d_r = move.end_row - move.start_row
    d_c = move.end_col - move.start_col
    frames_per_square = 10  # frames to move one square
    frame_count = (abs(d_r) + abs(d_c)) * frames_per_square
    for frame in range(frame_count + 1):
        r, c = (move.start_row + d_r*frame/frame_count, move.start_col + d_c*frame/frame_count)
        draw_board(screen)
        draw_pieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col*SQUARE_SIZE, move.end_row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)


def draw_text(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, 0, p.Color('Gray'))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT)\
        .move(WIDTH/2 - text_object.get_width()/2, HEIGHT/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, p.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))


if __name__ == "__main__":
    main()
