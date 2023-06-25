from evaluate import *
from engine import *

class Pawn:

    @staticmethod
    def isolated(game_state, square=None, param=None):
        if square is None:
            return Global.sum(game_state, Pawn.isolated)
        if game_state.board[square.row][square.col] != "wp":
            return 0
        for i in range(8):
            if game_state.board[i][square.col - 1] == "wp":
                return 0
            if game_state.board[i][square.col + 1] == "wp":
                return 0

        return 1

    @staticmethod
    def opposed(game_state, square=None, param=None):
        if square is None:
            return Global.sum(game_state, Pawn.opposed)
        if game_state.board[square.row][square.col] != "wp":
            return 0
        for i in range(square.row):
            if game_state.board[i][square.col] == "bp":
                return 1
        return 0

    @staticmethod
    def phalanx(game_state, square=None, param=None):
        if square is None:
            return Global.sum(game_state, Pawn.phalanx)
        if game_state.board[square.row][square.col] != "wp":
            return 0
        if game_state.board[square.row][square.col - 1] == "wp":
            return 1
        if game_state.board[square.row][square.col + 1] == "wp":
            return 1
        return 0

    @staticmethod
    def backward(game_state, square=None, param=None):
        if square is None:
            return Global.sum(game_state, Pawn.backward)
        if game_state.board[square.row][square.col] != "wp":
            return 0
        for j in range(square.row,8):
            if game_state.board[j][square.col - 1] == "wp" or game_state.board[j][square.col + 1] == "wp":
                return 0
        if Pawn.isolated(game_state, square):
            return 0
        if game_state.board[square.row - 2][square.col - 1] == "bp" \
            or game_state.board[square.row - 2][square.col + 1] == "bp" \
            or game_state.board[square.row - 1][square.col] == "bp":
            return 1
        return 0

    @staticmethod
    def doubled(game_state, square=None, param=None):
        if square is None:
            return Global.sum(game_state, Pawn.doubled)
        if game_state.board[square.row][square.col] != "wp":
            return 0
        if game_state.board[square.row + 1][square.col] != "wp":
            return 0
        if game_state.board[square.row + 1][square.col - 1] == "wp":
            return 0
        if game_state.board[square.row + 1][square.col + 1] == "wp":
            return 0
        return 1

    @staticmethod
    def connected(game_state, square=None, param=None):
        if square is None:
            return Global.sum(game_state, Pawn.connected)
        if Pawn.supported(game_state, square) or Pawn.phalanx(game_state, square):
            return 1
        return 0

    @staticmethod
    def supported(game_state, square, param=None):
        """
        check if there are any pawn that support a specific pawn
        """
        if square is None:
            return Global.sum(game_state, Pawn.supported)
        if game_state.board[square.row][square.col] != "wp":
            return 0
        val = 0
        val += 1 if game_state.board[square.row + 1][square.col - 1] == "wp" else 0
        val += 1 if game_state.board[square.row + 1][square.col + 1] == "wp" else 0
        return val

    @staticmethod
    def connected_bonus(game_state, square=None, param=None):
        if square is None:
            return Global.sum(game_state, Pawn.connected_bonus)
        if not Pawn.connected(game_state, square):
            return 0
        seed = [0, 7, 8, 12, 29, 48, 86]
        op = Pawn.opposed(game_state, square)
        ph = Pawn.phalanx(game_state, square)
        su = Pawn.supported(game_state, square)
        bl = 1 if game_state.board[square.row - 1][square.col] == "bp" else 0
        r = square.row
        if r < 2 or r > 7:
            return 0
        return seed[r - 1] * (2 + ph - op) + 21 * su

    @staticmethod
    def pawns_midgame(game_state, square=None, param=None):
        if square is None:
            return Global.sum(game_state, Pawn.pawns_midgame)
        v = 0.0
        v -= 5 if Pawn.isolated(game_state, square) else 0
        v -= 9 if Pawn.backward(game_state, square) else 0
        v -= 11 if Pawn.doubled(game_state, square) else 0
        v += Pawn.connected_bonus(game_state, square) if Pawn.connected(game_state, square) else 0
        return v

    @staticmethod
    def pawns_endgame(game_state, square=None, param=None):
        if square is None:
            return Global.sum(game_state, Pawn.pawns_endgame)
        v = 0.0
        v -= 15 if Pawn.isolated(game_state, square) else 0
        v -= 24 if Pawn.backward(game_state, square) else 0
        v -= 56 if Pawn.doubled(game_state, square) else 0
        v += Pawn.connected_bonus(game_state, square) if (Pawn.connected(game_state, square) * (square.row - 3)/4) else 0
        return v
