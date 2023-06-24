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
    