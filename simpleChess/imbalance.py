from engine import *
from evaluate import *
from helper import *

class Imbalance:
    @staticmethod
    def imbalance(game_state, square=None, param=None):
        """
        calculates the imbalance by comparing the piece count of each piece type for both colors.
        Evaluate the material imbalance. We use a place-holder for the bishop pair "extended piece",
            which allows us to be more flexible in defining bishop pair bonuses.
            * This extended piece has a higher value than a regular bishop
                -> Help capture the adv of having both bishops in a pos
            * The actual value of the extended piece can be adjusted dynamically based on:
                - the position
                - game stage
                - ...
        """
        if square is None:
            return Global.sum(game_state, Imbalance.imbalance)

        qo = [
            [0],  # place holder
            [40, 38],  # wp
            [32, 255, -62],  # wN
            [0, 104, 4, 0],  # wB
            [-26, -2, 47, 105, -208],  # wR
            [-189, 24, 117, 133, -134, -6]  # wQ
        ]
        qt = [
            [0],
            [36, 0],
            [9, 63, 0],
            [59, 65, 42, 0],
            [46, 39, 24, -24, 0],
            [97, 100, -42, 137, 268, 0]
        ]
        # wx and wb for place-holder
        piece_types = ("wx", "wp", "wN", "wB", "wR", "wQ", "bx", "bp", "bN", "bB", "bR", "bQ")
        j = piece_types.index(game_state.board[square.row][square.col])
        if j < 0 or j > 5:
            return 0
        bishops = [0,0]
        v = 0.0
        for x in range(8):
            for y in range(8):
                i = piece_types.index(game_state.board[y][x])
                if i < 0: continue
                if i == 9:
                    bishops[0] += 1
                if i == 3:
                    bishops[1] += 1
                if i % 6 > j: continue
                if i > 5:
                    v += qt[j][i - 6]
                else:
                    v += qo[j][i]
        if bishops[0] > 1:
            v += qt[j][0]
        if bishops[1] > 1:
            v += qo[j][0]
        return v

    @staticmethod
    def bishop_pair(game_state):
        """
        player have two bishops
        """
        if Helper.bishop_count(game_state) > 1:
            return 1438
        return 0

    @staticmethod
    def imbalance_total(game_state, square=None):
        v = 0
        flip_gs = GameState()
        Global.flip_color(game_state, flip_gs)
        v += (Imbalance.imbalance(game_state) - Imbalance.imbalance(flip_gs))
        v += (Imbalance.bishop_pair(game_state) - Imbalance.bishop_pair(flip_gs))
        return v / 16
