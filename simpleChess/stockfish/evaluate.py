# coding=utf-8
from engine import GameState, CastleRights, Move
from helper import Helper
from passed_pawns import PassedPawns
from imbalance import Imbalance
from global_func import Global
from pawn import Pawn
from material import Material

class Square:
    def __init__(self, row, col):
        self.col = col
        self.row = row

"""
TODO:
* [ ] middle game evaluation
* [ ] endgame evaluation
* [x] phase
* [x] scale factor
* [x] tempo
"""


class Eval:

    @staticmethod
    def main_evaluation(game_state):
        mg = Eval.middle_game_eval(game_state)
        eg = Eval.end_game_eval(game_state)
        p = Eval.phase(game_state)
        t = Eval.tempo(game_state, None)
        eg = eg * Eval.scale_factor(game_state, eg) / 64
        return (mg * p + eg * (128 - p)) / 128 + t

    @staticmethod
    def middle_game_eval(game_state):
        v = 0.0
        flip_gs = GameState()
        Global.flip_color(game_state, flip_gs)
        v += (Material.piece_value_middlegame(game_state) - Material.piece_value_middlegame(flip_gs))
        v += (Material.psqt_middlegame(game_state) - Material.psqt_middlegame(flip_gs))
        v += Imbalance.imbalance_total(game_state)
        v += (Pawn.pawns_midgame(game_state) - Pawn.pawns_midgame(flip_gs))
        # mobility
        # threats
        # passed pawn
        # space
        # king safety
        return v

    @staticmethod
    def end_game_eval(game_state, noinitiative=None):  # include initiative factor or not
        """
        Evaluates position for the endgame phase
        """
        v = 0.0
        flip_gs = GameState()
        Global.flip_color(game_state, flip_gs)
        v += (Material.piece_value_endgame(game_state) - Material.piece_value_endgame(flip_gs))
        v += (Material.psqt_endgame(game_state) - Material.psqt_endgame(flip_gs))
        v += Imbalance.imbalance_total(game_state)
        v += (Pawn.pawns_endgame(game_state) - Pawn.pawns_endgame(flip_gs))

        return v

    @staticmethod
    def phase(game_state):
        """
        Defined based on the amount of non pawn material on the board
        """
        midgame_limit = 15258
        endgame_limit = 3915
        flip_gs = GameState()
        Global.flip_color(game_state, flip_gs)
        npm = Material.non_pawn_material(game_state) + Material.non_pawn_material(flip_gs)
        npm = max(endgame_limit, min(npm, midgame_limit))
        return ((npm - endgame_limit) * 128) / (midgame_limit - endgame_limit)

    @staticmethod
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

    @staticmethod
    def scale_factor(game_state, eg):
        """
        Used to scale down the endgame evaluation score
        """
        v = 0.0
        if eg is None:
            eg = Eval.end_game_eval(game_state)

        flip_gs = GameState()
        Global.flip_color(game_state, flip_gs)
        gs_w = GameState()
        gs_b = GameState()

        if eg > 0:
            gs_w = game_state
            gs_b = flip_gs
        else:
            gs_w = flip_gs
            gs_b = game_state

        sf = 64.0  # scaling factor
        # Since having more pieces is an advantage 
        pawn_count_w = Helper.pawn_count(gs_w)
        pawn_count_b = Helper.pawn_count(gs_b)
        npm_w = Material.non_pawn_material(gs_w)
        npm_b = Material.non_pawn_material(gs_b)

        bishop_value_midgame = 825.0
        bishop_value_endgame = 915.0
        rook_value_midgame = 1276

        # if there is no white pawn and condition
        if pawn_count_w == 0 and npm_w - npm_b <= bishop_value_midgame :
            if npm_w < rook_value_midgame:
                sf = 0
            else:
                sf = 4 if npm_b <= bishop_value_midgame else 14

        if sf == 64:
            ob = Helper.opposite_bishops(game_state)
            # if there are one bishop each side and they are opposite bishop (exclude pawns)
            if ob and npm_w == bishop_value_midgame and npm_b == bishop_value_midgame:
                asymmetry = 0
                # check if there are any pawn are blocked by the opponent pawn
                # in the same col
                for col in range(8):
                    open = [0, 0]
                    for row in range(8):
                        if Global.get_piece(game_state, row, col) == "wp":
                            open[0] = 1
                        elif Global.get_piece(game_state, row, col) == "bp":
                            open[1] = 1
                    if open[0] + open[1] == 1:
                        asymmetry += 1

                asymmetry += PassedPawns.candidate_passed(game_state) + PassedPawns.candidate_passed(flip_gs)
                sf = 8 + 4 * asymmetry
            else:
                temp = 40 + (2 if ob else 7) * pawn_count_w
                sf = sf if sf < temp else temp
        return sf
