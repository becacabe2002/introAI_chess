from evaluate import *

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

    @staticmethod
    def index_of(input_tuple, substring):
        for i in range(len(input_tuple)):
            if input_tuple[i] == substring:
                return i
        return -1

    @staticmethod
    def get_piece(game_state, row, col):
        if 0 <= row <= 7 and 0 <= col <= 7:
            return game_state.board[row][col]
        return None

