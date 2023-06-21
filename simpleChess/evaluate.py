
"""
TODO:
* [ ] middle game evaluation
* [ ] endgame evaluation
* [ ] phase
* [ ] scale factor
* [x] tempo
"""


class Square:
    def __init__(self, row, col):
        self.col = col
        self.row = row


def main_evaluation(game_state):
    mg = middle_game_eval(game_state)
    eg = end_game_eval(game_state)
    p = phase(game_state)
    t = tempo(game_state, None)
    eg = eg * scale_factor(game_state, eg) / 64
    return (mg * p + eg * (128 - p)) / 128 + t


def middle_game_eval(game_state):
    return 1


def end_game_eval(game_state):
    return 1


def phase(game_state):
    return 1


def tempo(game_state, square):
    """
    > **tempo** - turn/single move
    * when a player achieves desired result in one fewer move
    -> Gain a tempo
    * when a player takes more move than necessary
    -> Lose a tempo
    """
    if square is not None:
        return 0
    else:
        if game_state.white_to_move:
            return 28 * 1
        else:
            return 28 * -1

def scale_factor(game_state, eg):
    """
    Used to scale down the endgame evaluation score
    """
    if eg is None:
        eg = end_game_eval(game_state)


    return 1
