from engine import *
from evaluate import *
from helper import *
from pawn import Pawn
from global_func import Global


class PassedPawns:
    @staticmethod
    def candidate_passed(game_state, square=None, param=None):
        """
        check if pawn is passed or candidate passer.
        A passed pawn is when one of the three following condition is True:
            1. There is no stoppers except some levers
            2. The only stoppers are the leverPush, but we can outnumber them
            3. There is only one front stopper which can be levered
        If there is pawn of our color in the same file in front of current pawn it's no longer counts as passed.
        """
        if square is None:
            return Global.sum(game_state, PassedPawns.candidate_passed)
        if Global.get_piece(game_state, square.row, square.col) != "wp":
            return 0
        ty1 = 8
        ty2 = 8
        oy = 8
        for i in reversed(range(square.row)):
            if Global.get_piece(game_state, i, square.col) == "bp":
                ty1 = i
            if Global.get_piece(game_state, i, square.col - 1) == "bp" or \
                    Global.get_piece(game_state, i, square.col + 1) == "bp":
                ty2 = i
        if ty2 < (square.row - 2) or ty1 < (square.row - 1):
            return 0
        if ty2 >= square.row and ty1 == (square.row - 1) and square.row < 4:
            if Global.get_piece(game_state, square.row + 1, square.col - 1) == "wp" \
                    and Global.get_piece(game_state, square.row, square.col - 1) != "bp" \
                    and Global.get_piece(game_state, square.row - 1, square.col - 2) != "bp":
                return 1
            if Global.get_piece(game_state, square.row + 1, square.col + 1) == "wp" \
                    and Global.get_piece(game_state, square.row, square.col + 1) != "bp" \
                    and Global.get_piece(game_state, square.row - 1, square.col + 2) != "bp":
                return 1
        if Global.get_piece(game_state, square.row - 1, square.col) == "bp":
            return 0
        count1 = (1 if Global.get_piece(game_state, square.row - 1, square.col - 1) == "bp" else 0) + \
                 (1 if Global.get_piece(game_state, square.row - 1, square.col + 1) == "bp" else 0) - \
                 Pawn.supported(game_state, square) - 1
        count2 = (1 if Global.get_piece(game_state, square.row - 2, square.col - 1) == "bp" else 0) + \
                 (1 if Global.get_piece(game_state, square.row - 2, square.col + 1) == "bp" else 0) - \
                 (1 if Global.get_piece(game_state, square.row, square.col - 1) == "wp" else 0) - \
                 (1 if Global.get_piece(game_state, square.row, square.col + 1) == "wp" else 0)
        if count1 > 0 or count2 > 0:
            return 0
        return 1
