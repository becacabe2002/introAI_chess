from global_func import Global
from evaluate import *

class Material:

    @staticmethod
    def non_pawn_material(game_state, square=None, param=None):
        """
        Midgame value of non-pawn material.
        """
        if square is None:
            return Global.sum(game_state, Material.non_pawn_material)
        string = ("wN", "wB", "wR", "wQ")
        i = Global.index_of(string, Global.get_piece(game_state, square.row, square.col))
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
        i = Global.index_of(string, Global.get_piece(game_state, square.row, square.col))
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
            [[0, 0, 0, 0], [-11, 7, 7, 17], [-16, -3, 23, 23], [-14, -7, 20, 24], [-5, -2, -1, 12], [-11, -12, -2, 4],
             [-2, 20, -10, -2], [0, 0, 0, 0]],
            [[-161, -96, -80, -73], [-83, -43, -21, -10], [-71, -22, 0, 9], [-25, 18, 43, 47], [-26, 16, 38, 50],
             [-11, 37, 56, 65], [-63, -19, 5, 14], [-195, -67, -42, -29]],
            [[-49, -7, -10, -34], [-24, 9, 15, 1], [-9, 22, -3, 12], [4, 9, 18, 40], [-8, 27, 13, 30], [-17, 14, -6, 6],
             [-19, -13, 7, -11], [-47, -7, -17, -29]],
            [[-25, -16, -16, -9], [-21, -8, -3, 0], [-21, -9, -4, 2], [-22, -6, -1, 2], [-22, -7, 0, 1],
             [-21, -7, 0, 2], [-12, 4, 8, 12], [-23, -15, -11, -5]],
            [[0, -4, -3, -1], [-4, 6, 9, 8], [-2, 6, 9, 9], [-1, 8, 10, 7], [-3, 9, 8, 7], [-2, 6, 8, 10],
             [-2, 7, 7, 6], [-1, -4, -1, 0]],
            [[272, 325, 273, 190], [277, 305, 241, 183], [198, 253, 168, 120], [169, 191, 136, 108],
             [145, 176, 112, 69], [122, 159, 85, 36], [87, 120, 64, 25], [64, 87, 49, 0]]]

        bonus2 = [
            [[0, 0, 0, 0], [-3, -1, 7, 2], [-2, 2, 6, -1], [7, -4, -8, 2], [13, 10, -1, -8], [16, 6, 1, 16],
             [1, -12, 6, 25], [0, 0, 0, 0]],
            [[-105, -82, -46, -14], [-69, -54, -17, 9], [-50, -39, -7, 28], [-41, -25, 6, 38], [-46, -25, 3, 40],
             [-54, -38, -7, 27], [-65, -50, -24, 13], [-109, -89, -50, -13]],
            [[-58, -31, -37, -19], [-34, -9, -14, 4], [-23, 0, -3, 16], [-26, -3, -5, 16], [-26, -4, -7, 14],
             [-24, -2, 0, 13], [-34, -10, -12, 6], [-55, -32, -36, -17]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
             [0, 0, 0, 0]],
            [[-71, -56, -42, -29], [-56, -30, -21, -5], [-39, -17, -8, 5], [-29, -5, 9, 19], [-27, -5, 10, 21],
             [-40, -16, -10, 3], [-55, -30, -21, -6], [-74, -55, -43, -30]],
            [[0, 41, 80, 93], [57, 98, 138, 131], [86, 138, 165, 173], [103, 152, 168, 169], [98, 166, 197, 194],
             [87, 164, 174, 189], [40, 99, 128, 141], [5, 60, 75, 75]]]

        string = ("wp", "wN", "wB", "wR", "wQ", "wK")
        i = Global.index_of(string, Global.get_piece(game_state, square.row, square.col))
        if i < 0:
            return 0
        if param:  # middle game
            return bonus1[i][7 - square.row][min(square.col, 7 - square.col)]
        else:  # end game
            return bonus2[i][7 - square.row][min(square.col, 7 - square.col)]

