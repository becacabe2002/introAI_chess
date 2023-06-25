# coding=utf-8
from engine import GameState, CastleRights
from helper import Helper
from passed_pawns import *
from imbalance import Imbalance

class Square:
    def __init__(self, row, col):
        self.col = col
        self.row = row


class Global:

    @staticmethod
    def flip_color(gs1, gs2):
        """
        đổi màu quân cờ từ trắng -> đen và ngược lại, cập nhật các chỉ số liên quan
        cac chi so can cap nhat:
        * Castle Rights
        * Enpassant Possible
        * White to move
        * Move count
        """
        for i in range(8):
            for j in range(8):
                piece = gs1.board[7 - i][j]
                gs2.board[i][j] = gs1.board[7-i][j]
                if piece == "w":
                    gs2.board[i][j] = "b" + gs2.board[i][j][1]
                else:
                    gs2.board[i][j] = "w" + gs2.board[i][j][1]

        gs2.current_castling_rights = CastleRights(wks=gs1.current_castling_rights.bks,
                                                   bks=gs1.current_castling_rights.wks,
                                                   wqs=gs1.current_castling_rights.bqs,
                                                   bqs=gs1.current_castling_rights.wqs)

        if gs1.enpassant_possible is not None:
            gs2.enpassant_possible = (7 - gs1.enpassant_possible[0], gs1.enpassant_possible[1])

        gs2.white_to_move = not gs1.white_to_move
        gs2.move_count = (gs1.move_count[0], gs1.move_count[1])

    @staticmethod
    def sum(game_state, func, param=None):
        d_sum = 0
        for i in range(8):
            for j in range(8):
                square = Square(i, j)
                d_sum += func(game_state, square, param)

        return d_sum


class Material:

    @staticmethod
    def non_pawn_material(game_state, square=None, param=None):
        """
        Midgame value of non-pawn material.
        """
        if square is None:
            return Global.sum(game_state, Material.non_pawn_material)
        string = ("wN", "wB", "wR", "wQ")
        i = string.index(game_state.board[square.row][square.col])
        if i >= 0:
            temp = True
            return Material.piece_value_bonus(game_state, square, temp)

    @staticmethod
    def piece_value_bonus(game_state, square, param):
        """
        Material values for middlegame and engame.
        Decided by param value (True/false)
        """
        if square is None:
            return Global.sum(game_state, Material.piece_value_bonus, param)
        a1 = [136, 782, 830, 1289, 2529]
        a2 = [208, 865, 918, 1378, 2687]

        string = ("wp", "wN", "wB", "wR", "wQ")
        i = string.index(game_state.board[square.row][square.col])
        if i >= 0:
            if param:  # True -> Midgame
                return a1[i]
            else:  # False -> Endgame
                return a2[i]
        return 0

    @staticmethod
    def piece_value_middlegame(game_state, square=None, param=None):
        if square is None:
            return Global.sum(game_state, Material.piece_value_middlegame)
        temp = True
        return Material.piece_value_bonus(game_state, square, temp)

    @staticmethod
    def piece_value_endgame(game_state, square=None, param=None):
        if square is None:
            return Global.sum(game_state, Material.piece_value_endgame)
        temp = True
        return Material.piece_value_bonus(game_state, square, temp)
    
    @staticmethod
    def psqt_middlegame(game_state, square=None, param=None):
        """
        Piece square table bonuses - middlegame.
        """
        if square is None:
            return Global.sum(game_state, Material.psqt_middlegame)
        temp = True
        return Material.psqt_bonus(game_state, square, temp)

    @staticmethod
    def psqt_endgame(game_state, square=None, param=None):
        """
         Piece square table bonuses - endgame.
        """
        if square is None:
            return Global.sum(game_state, Material.psqt_endgame)
        temp = False
        return Material.psqt_bonus(game_state, square, temp)

    @staticmethod
    def psqt_bonus(game_state, square, param):
        """
        Piece square table bonuses.
        For each piece type on a given square a (middlegame, endgame) score pair is assigned.
        """
        if square is None:
            return Global.sum(game_state, Material.psqt_bonus, param)
        bonus1 = [
            [[0, 0, 0, 0], [-11, 7, 7, 17], [-16, -3, 23, 23], [-14, -7, 20, 24], [-5, -2, -1, 12], [-11, -12, -2, 4], [-2, 20, -10, -2], [0, 0, 0, 0]],
            [[-161, -96, -80, -73], [-83, -43, -21, -10], [-71, -22, 0, 9], [-25, 18, 43, 47], [-26, 16, 38, 50], [-11, 37, 56, 65], [-63, -19, 5, 14], [-195, -67, -42, -29]],
            [[-49, -7, -10, -34], [-24, 9, 15, 1], [-9, 22, -3, 12], [4, 9, 18, 40], [-8, 27, 13, 30], [-17, 14, -6, 6], [-19, -13, 7, -11], [-47, -7, -17, -29]],
            [[-25, -16, -16, -9], [-21, -8, -3, 0], [-21, -9, -4, 2], [-22, -6, -1, 2], [-22, -7, 0, 1], [-21, -7, 0, 2], [-12, 4, 8, 12], [-23, -15, -11, -5]],
            [[0, -4, -3, -1], [-4, 6, 9, 8], [-2, 6, 9, 9], [-1, 8, 10, 7], [-3, 9, 8, 7], [-2, 6, 8, 10], [-2, 7, 7, 6], [-1, -4, -1, 0]],
            [[272, 325, 273, 190], [277, 305, 241, 183], [198, 253, 168, 120], [169, 191, 136, 108], [145, 176, 112, 69], [122, 159, 85, 36], [87, 120, 64, 25], [64, 87, 49, 0]]]

        bonus2 = [
            [[0, 0, 0, 0], [-3, -1, 7, 2], [-2, 2, 6, -1], [7, -4, -8, 2], [13, 10, -1, -8], [16, 6, 1, 16], [1, -12, 6, 25], [0, 0, 0, 0]],
            [[-105, -82, -46, -14], [-69, -54, -17, 9], [-50, -39, -7, 28], [-41, -25, 6, 38], [-46, -25, 3, 40], [-54, -38, -7, 27], [-65, -50, -24, 13], [-109, -89, -50, -13]],
            [[-58, -31, -37, -19], [-34, -9, -14, 4], [-23, 0, -3, 16], [-26, -3, -5, 16], [-26, -4, -7, 14], [-24, -2, 0, 13], [-34, -10, -12, 6], [-55, -32, -36, -17]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[-71, -56, -42, -29], [-56, -30, -21, -5], [-39, -17, -8, 5], [-29, -5, 9, 19], [-27, -5, 10, 21], [-40, -16, -10, 3], [-55, -30, -21, -6], [-74, -55, -43, -30]],
            [[0, 41, 80, 93], [57, 98, 138, 131], [86, 138, 165, 173], [103, 152, 168, 169], [98, 166, 197, 194], [87, 164, 174, 189], [40, 99, 128, 141], [5, 60, 75, 75]]]

        string = ("wp", "wN", "wB", "wR", "wQ", "wK")
        i = string.index(game_state.board[square.row][square.col])
        if i < 0:
            return 0
        if param:  # middle game
            return bonus1[i][7 - square.row][min(square.col, 7 - square.col)]
        else:  # end game
            return bonus2[i][7 - square.row][min(square.col, 7 - square.col)]


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
        """
        Since having more pieces 
        """
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
                        if game_state.board[row, col] == "wp":
                            open[0] = 1
                        elif game_state.board[row, col] == "bp":
                            open[1] = 1
                    if open[0] + open[1] == 1:
                        asymmetry += 1

                asymmetry += PassedPawns.candidate_passed(game_state) + PassedPawns.candidate_passed(flip_gs)
                sf = 8 + 4 * asymmetry
            else:
                temp = 40 + (2 if ob else 7) * pawn_count_w
                sf = sf if sf < temp else temp
        return sf
