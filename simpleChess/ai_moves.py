import random

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3,
               "N": 3, "p": 1}  # assign scrores for each piece

CHECKMATE = 1000
STALEMATE = 0


def find_best_move(game_state, valid_moves):
    """
    Find the best move based on material alone
    """
    turn_multiplier = 1 if game_state.white_to_move else -1
    opponent_minmax_score = CHECKMATE
    best_player_move = None
    random.shuffle(valid_moves)

    for player_move in valid_moves:
        game_state.make_move(player_move)
        opponents_moves = game_state.get_valid_moves()
        if game_state.stale_mate:
            opponent_max_score = STALEMATE
        elif game_state.check_mate:
            opponent_max_score = -CHECKMATE
        else:
            opponent_max_score = -CHECKMATE
            for opponents_move in opponents_moves:
                game_state.make_move(opponents_move)
                game_state.get_valid_moves()
                if game_state.check_mate:
                    score = CHECKMATE
                elif game_state.stale_mate:
                    score = STALEMATE
                else:
                    score = -turn_multiplier * score_material(game_state.board)
                if score > opponent_max_score:
                    opponent_max_score = score
                game_state.undo_move()
        if opponent_max_score < opponent_minmax_score:
            opponent_minmax_score = opponent_max_score
            best_player_move = player_move
        game_state.undo_move()
    return best_player_move


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