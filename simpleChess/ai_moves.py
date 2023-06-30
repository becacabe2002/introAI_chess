import random

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3,
               "N": 3, "p": 1}  # assign scrores for each piece

CHECKMATE = 1000
STALEMATE = 0
# DEPTH = 3


# def find_best_move_min_max_no_recursion(game_state, valid_moves):
#     """
#     Find the best move, min max without recursion
#     """
#     turn_multiplier = 1 if game_state.white_to_move else -1
#     opponent_minmax_score = CHECKMATE
#     best_player_move = None
#     random.shuffle(valid_moves)

#     for player_move in valid_moves:
#         game_state.make_move(player_move)
#         opponents_moves = game_state.get_valid_moves()
#         if game_state.stale_mate:
#             opponent_max_score = STALEMATE
#         elif game_state.check_mate:
#             opponent_max_score = -CHECKMATE
#         else:
#             opponent_max_score = -CHECKMATE
#             for opponents_move in opponents_moves:
#                 game_state.make_move(opponents_move)
#                 game_state.get_valid_moves()
#                 if game_state.check_mate:
#                     score = CHECKMATE
#                 elif game_state.stale_mate:
#                     score = STALEMATE
#                 else:
#                     score = -turn_multiplier * score_material(game_state.board)
#                 if score > opponent_max_score:
#                     opponent_max_score = score
#                 game_state.undo_move()
#         if opponent_max_score < opponent_minmax_score:
#             opponent_minmax_score = opponent_max_score
#             best_player_move = player_move
#         game_state.undo_move()
#     return best_player_move


def find_best_move(game_state, valid_moves, chosen_depth, chosen_algorithm):
    """
    Helper method to make first recursive call
    """
    global next_move, counter
    print(chosen_depth)
    next_move = None
    random.shuffle(valid_moves)
    counter = 0
    if chosen_algorithm == 'minmax':
        find_move_minmax(game_state, valid_moves, chosen_depth, game_state.white_to_move, max_depth = chosen_depth)
    elif chosen_algorithm == 'negamax':
        find_move_nega_max(game_state, valid_moves, chosen_depth, game_state.white_to_move, max_depth = chosen_depth)
    else:
        find_move_nega_max_alpha_beta(game_state, valid_moves, chosen_depth, -CHECKMATE, CHECKMATE, 1 if game_state.white_to_move else -1, max_depth = chosen_depth)
    print("counter" , counter)
    return next_move


def find_move_minmax(game_state, valid_moves, initial_depth, white_to_move, max_depth):
    global next_move
    if initial_depth == 0:
        return score_material(game_state.board)

    if white_to_move:
        max_score = -CHECKMATE
        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()
            score = find_move_minmax(game_state, next_moves, initial_depth - 1, False, max_depth)
            # search all possibilities down below the depth
            # to find the best score at that point
            if score > max_score:
                max_score = score
                if initial_depth == max_depth:
                    next_move =  move
            game_state.undo_move()
        return max_score # recursion back up
    else:
        min_score = CHECKMATE    
        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()
            score = find_move_minmax(game_state, next_moves, initial_depth - 1, True, max_depth)    
            if score < min_score:
                min_score = score
                if initial_depth == max_depth:
                    next_move = move
            game_state.undo_move()
        return min_score

def find_move_nega_max(game_state, valid_moves, initial_depth, turn_multiplier, max_depth):
    global next_move, counter
    counter += 1
    if initial_depth ==0:
        return turn_multiplier * score_board(game_state)
    
    max_score =-CHECKMATE
    for move in valid_moves:
        game_state.make_move(move)
        next_moves = game_state.get_valid_moves()
        score = -find_move_nega_max(game_state, next_moves, initial_depth -1, -turn_multiplier, max_depth)
        if score > max_score:
            max_score = score
            if initial_depth == max_depth:
                next_move = move
        game_state.undo_move()
    return max_score

def find_move_nega_max_alpha_beta(game_state, valid_moves, initial_depth, alpha, beta, turn_multiplier, max_depth):
    global next_move, counter
    counter += 1
    if initial_depth ==0:
        return turn_multiplier * score_board(game_state)
    
    max_score =-CHECKMATE
    for move in valid_moves:
        game_state.make_move(move)
        next_moves = game_state.get_valid_moves()
        score = -find_move_nega_max_alpha_beta(game_state, next_moves, initial_depth -1, -beta, -alpha, -turn_multiplier, max_depth)
        if score > max_score:
            max_score = score
            if initial_depth == max_depth:
                next_move = move
        game_state.undo_move()
        if max_score > alpha:  # pruning happens
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


def score_board(game_state):
    """
    A positive score is good for white, a negative score is good for black
    """
    if game_state.check_mate:
        if game_state.white_to_move:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif game_state.stale_mate:
        return STALEMATE  # neither side wins

    score = 0
    for row in game_state.board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]
    return score


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
