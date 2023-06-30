from global_func import Global
from evaluate import Square
from engine import *
import math


class Attack:

    @staticmethod
    def pinned_direction(game_state, square=None, param=None):
        """
        Help detecting blockers for King.
        * Total Val = White Pinned Direction - Black Pinned Direction
        4 type of blockers:
            + 1 points for horizontal block
            + 2 points for top-left to bottom-right
            + 3 points for vertical block
            + 4 points for top-right to bottom-left
        """
        if square is None:
            return Global.sum(game_state, Attack.pinned_direction)

        all_pieces = ("wp", "wN", "wB", "wR", "wQ", "wK", "bp", "bN", "bB", "bR", "bQ", "bK")
        if Global.index_of(all_pieces, Global.get_piece(game_state, square.row, square.col)) < 0:
            return 0
        color = 1
        if Global.index_of(all_pieces, Global.get_piece(game_state, square.row, square.col)) >= 6:
            color = -1

        for i in range(8):
            # direction vector
            ix = ((i + (i > 3)) % 3) - 1
            iy = math.floor(((i + (i > 3)) / 3) - 1)
            king = False  # if king is in the current direction
            for d in range(1, 8):
                piece = Global.get_piece(game_state, square.row + d * iy, square.col + d * ix)
                if piece == "wK":
                    king = True
                if piece != "--":
                    break  # blocked

            if king:  # if king is in the direction, examine pieces in the opposite direction
                for d in range(1, 8):
                    piece = Global.get_piece(game_state, square.row - d * iy, square.col - d * ix)
                    if piece == "bQ" \
                            or piece == "bB" and ix * iy != 0 \
                            or piece == "bR" and ix * iy == 0:
                        # just take vertical/horizontal attack from rook,
                        # xray attack from bishop, and take both from queen
                        return math.fabs(ix + iy * 3) * color
                    if piece is not "--":
                        break
        return 0

    @staticmethod
    def knight_attack(game_state, square=None, param=None):
        """
        Count the number of knight-attacked squares on board
        (can be stacked)
        """
        if square is None:
            return Global.sum(game_state, Attack.knight_attack)
        square2 = param
        temp_square = Square(0,0)
        v = 0.0
        for i in range(8):
            ix = ((i > 3) + 1) * (((i % 4) > 1) * 2 - 1)
            iy = (2 - (i > 3)) * ((i % 2 == 0) * 2 - 1)
            piece = Global.get_piece(game_state,square.row + iy, square.col + ix)
            temp_square.row = square.row + iy
            temp_square.col = square.col + ix
            if piece == "wN" and \
                    (square2 is None or square2.row == square.row + iy and square2.col == square.col + ix) \
                    and not Attack.pinned(game_state, temp_square):
                v += 1
        return v

    @staticmethod
    def total_attack(game_state, square=None, param=None):
        if square is None:
            return Global.sum(game_state, Attack.total_attack)
        v = 0.0
        v += Attack.pawn_attack(game_state, square)
        v += Attack.king_attack(game_state, square)
        v += Attack.knight_attack(game_state, square)
        v += Attack.bishop_xray_attack(game_state, square)
        v += Attack.rook_xray_attack(game_state, square)
        v += Attack.queen_attack(game_state, square)

        return v

    @staticmethod
    def pinned(game_state, square, param=None):
        """
        abs pin is when a piece can not move,
        since doing that can expose king to be attacked
        """
        if square is None:
            return Global.sum(game_state, Attack.pinned)
        white_pieces = ("wp", "wN", "wB", "wR", "wQ", "wK")
        p = Global.get_piece(game_state, square.row, square.col)
        if Global.index_of(white_pieces, p) < 0:
            return 0
        return 1 if Attack.pinned_direction(game_state, square) > 0 else 0

    @staticmethod
    def pawn_attack(game_state, square=None, param=None):
        """
        count the number of pawn-attacked squares
        (not include en passant attack and pinned)
        """
        if square is None:
            return Global.sum(game_state, Attack.pawn_attack)
        if Global.get_piece(game_state, square.row + 1, square.col - 1) == "wp":
            return 1
        if Global.get_piece(game_state, square.row + 1, square.col + 1) == "wp":
            return 1
        return 0

    @staticmethod
    def king_attack(game_state, square=None, param=None):
        """
        count the number of king-attacked squares
        """
        if square is None:
            return Global.sum(game_state, Attack.king_attack)
        for i in range(8):
            ix = ((i + (i > 3)) % 3) - 1
            iy = math.floor(((i + (i > 3)) / 3) - 1)
            if Global.get_piece(game_state, square.row + ix, square.row + iy) == "wK":
                return 1
        return 0

    @staticmethod
    def bishop_xray_attack(game_state, square, param=None):
        """
        count the number of bishop-attacked squares
        (include xray attack through opponent queen)
        """
        if square is None:
            return Global.sum(game_state, Attack.bishop_xray_attack)
        square2 = param
        temp_square = Square(0, 0)
        v = 0.0
        for i in range(4):
            ix = ((i > 1) * 2 - 1)
            iy = ((i % 2 == 0) * 2 - 1)
            for d in range(1,8):
                piece = Global.get_piece(game_state, square.row + d * ix, square.col + d * iy)
                if piece == "wB" and \
                        square2 is None \
                        or square2.row == square.row + d * ix and square2.col == square.col + d * iy:
                    temp_square.row = square.row + d * ix
                    temp_square.col = square.col + d * iy
                    direction = Attack.pinned_direction(game_state, temp_square)
                    if direction == 0 or math.fabs(ix + iy * 3) == direction:
                        v += 1
                if piece != "--" and piece != "wQ" and piece != "bQ":
                    break
        return v


    @staticmethod
    def rook_xray_attack(game_state, square=None, param=None):
        """
        count the number of rook-attacked squares
        (include xray attack through opponent queen and allie rook)
        """
        pass

    @staticmethod
    def queen_attack(game_state, square=None, param=None):
        """
        count the number of queen-attacked squares
        """
        pass
