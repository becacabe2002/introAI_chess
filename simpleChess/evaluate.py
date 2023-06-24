# coding=utf-8
from engine import GameState, CastleRights
from helper import Helper

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
            if param:  # True
                return a1[i]
            else:  # False
                return a2[i]
        return 0

    @staticmethod
    def piece_value_middlegame(game_state, square, param):
        if square is None:
            return Global.sum(game_state, Material.piece_value_middlegame)
        temp = True
        return Material.piece_value_bonus(game_state, square, temp)

    @staticmethod
    def piece_value_endgame(game_state, square, param):
        if square is None:
            return Global.sum(game_state, Material.piece_value_endgame)
        temp = True
        return Material.piece_value_bonus(game_state, square, temp)

"""
TODO:
* [ ] middle game evaluation
* [ ] endgame evaluation
* [x] phase
* [ ] scale factor
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
        return 1

    @staticmethod
    def end_game_eval(game_state, noinitiative=None):  # include initiative factor or not
        """
        Evaluates position for the endgame phase
        """
        v = 0.0

        return 1

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

        bishop_value_midgame = 828.0
        bishop_value_endgame = 916.0
        rook_value_midgame = 1286

        return 1
