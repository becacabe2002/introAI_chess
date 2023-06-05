'''
Main driver file.
Handling user input.
Displaying current GameStatus object.
'''

import pygame as p
import engine
import sys

WIDTH = HEIGHT = 512
DIMENSION = 8

SQUARE_SIZE = HEIGHT // DIMENSION

MAX_FPS = 15
    
IMAGES = {}


def load_images():
    '''
    Initialize a global directory of images.
    This will be called exactly once in the main.
    '''
    pieces = ['wp', 'wR', 'wN', 'wB' ,'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE,SQUARE_SIZE))
        
        
def main():
    '''
    The main driver for our code.
    This will handle user input and updating the graphics.
    '''
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = engine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False #flag variable for when a move is made
    
    load_images() #do this only once before while loop
    
    running = True
    square_selected = () #no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    player_clicks = [] #this will keep track of player clicks (two tuples)

    while running:
        for e in p.event.get():  
            if e.type == p.QUIT:
                running = False
                p.quit()
                sys.exit()
            #mouse handler            
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x, y) location of the mouse
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE
                if square_selected == (row, col): #user clicked the same square twice
                    square_selected = () #deselect
                    player_clicks = [] #clear clicks
                else:
                    square_selected = (row, col)
                    player_clicks.append(square_selected) #append for both 1st and 2nd click
                if len(player_clicks) == 2: #after 2nd click                                                                    
                    move = engine.Move(player_clicks[0], player_clicks[1], game_state.board)
                    for i in range(len(valid_moves)):
                        if move == valid_moves[i]:
                            print(move.getChessNotation()) 
                            game_state.make_move(valid_moves[i])
                            move_made = True
                            square_selected = () #reset user clicks
                            player_clicks = [] 
                    if not move_made:
                        player_clicks = [square_selected]
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    game_state.undo_move()
                    move_made = True
                    
        if move_made:
            valid_moves = game_state.get_valid_moves()
            move_made = False
                    
                            
        draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_game_state(screen, game_state):
    '''
    Responsible for all the graphics within current game state.
    '''
    draw_board(screen) #draw squares on the board
    #add in piece highlighting or move suggestions (later)
    draw_pieces(screen, game_state.board) #draw pieces on top of those squares


def draw_board(screen):
    '''
    Draw the squares on the board.
    The top left square is always light.
    '''
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row+column) % 2)]
            p.draw.rect(screen, color, p.Rect(column*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    

def draw_pieces(screen, board):
    '''
    Draw the pieces on the board using the current game_state.board
    '''
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
         
                
if __name__ == "__main__":
    main()
