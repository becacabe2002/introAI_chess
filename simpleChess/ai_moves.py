import random

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1} # assign scrores for each piece

CHECKMATE = 1000
STALEMATE = 0

def find_best_move(game_state, valid_moves):
    """
    Find the best move based on material alone
    """
    return

def score_material(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]
    return score

def find_random_move(valid_moves):
    """
    Picks and returns a random valid move.
    """
    return random.choice(valid_moves)
