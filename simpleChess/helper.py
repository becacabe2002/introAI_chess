from evaluate import GameState, Global, Material, Eval, Square, CastleRights
from engine import GameState, CastleRights, Move


class Helper:
    @staticmethod
    def bishop_count(game_state, square=None, param=None):
        if square is None:
            return Global.sum(game_state, Helper.bishop_count)
        if game_state.board[square.row][square.col] == "wB":
            return 1
        return 0

    @staticmethod
    def queen_count(game_state, square=None, param=None):
        if square is None:
            return Global.sum(game_state, Helper.queen_count)
        if game_state.board[square.row][square.col] == "wQ":
            return 1
        return

    @staticmethod
    def knight_count(game_state, square=None, param=None):
        if square is None:
            return Global.sum(game_state, Helper.knight_count)
        if game_state.board[square.row][square.col] == "wN":
            return 1
        return 0

    @staticmethod
    def rook_count(game_state, square=None, param=None):
        if square is None:
            return Global.sum(game_state, Helper.rook_count)
        if game_state.board[square.row][square.col] == "wR":
            return 1
        return 0

    @staticmethod
    def pawn_count(game_state, square=None, param=None):
        if square is None:
            return Global.sum(game_state, Helper.pawn_count)
        if game_state.board[square.row][square.col] == "wp":
            return 1
        return 0

    @staticmethod
    def opposite_bishops(game_state, square=None):
        """
        when each player has only one bishop remaining, and they are of opposite colors
        (one player has a light-squared bishop, and the other player has a dark-squared bishop).
        """
        if Helper.bishop_count(game_state) != 1:
            return False
        flip_gs = GameState()
        Global.flip_color(game_state, flip_gs)
        if Helper.bishop_count(flip_gs) != 1:
            return False

        color = [0, 0]
        for i in range(8):
            for j in range(8):
                if game_state.board[i][j] == 'wB':
                    color[0] = (i + j) % 2
                if game_state.board[i][j] == 'bB':
                    color[1] = (i + j) % 2
        # if color[0] == color[1] -> bishop in the same color
        return False if color[0] == color[1] else True
