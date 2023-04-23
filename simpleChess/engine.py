
class GameState:
    """
    * Storing all information about the current state of the game.
    * Determining valid moves at the current state.
    * Keeping move logs.
    """
    def __init__(self):
        # b for black
        # w for white
        # __ for empty block
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.white_move = True  # decide what player to move
        self.move_log = []
        self.move_func = {'p': self.get_pawn_moves, 'R': self.get_rock_moves, 'N': self.get_knight_moves, 'B': self.get_bishop_moves,
                          'Q': self.get_queen_moves, 'K': self.get_king_moves}

    def make_a_move(self, move):
        self.board[move.start_row][move.start_col] = "__"
        self.board[move.end_row][move.end_col] = move.piece_moved
        # save move to log list to undo if necessary
        self.move_log.append(move)
        # swap player
        self.white_move = not self.white_move

    def undo_move(self):
        if len(self.move_log) != 0:  # check whether is a move performed
            last_move = self.move_log.pop()
            self.board[last_move.start_row][last_move.start_col] = last_move.piece_moved
            self.board[last_move.end_row][last_move.end_col] = last_move.piece_captured
            self.white_move = not self.white_move

    def gen_valid_moves(self):
        """
        Generate only valid moves based on generated possible moves
        * Get all possible move (move n):
        * Loop through all possible move:
            + Move piece
            + Generate all possible move for opponent(move n.*)
            + Check whether there are any moves that attack the king
            + If the king is not attacked -> add move n to a list
        * return the list that contains only valid move
        """
        return self.gen_possible_moves()

    def gen_possible_moves(self):
        """
        Generate all possible moves based on current game state board.
        """
        possible_moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]  # white(w) or black(b)
                if (turn == 'w' and self.white_move) or (turn == 'b' and not self.white_move):
                    piece = self.board[row][col][1]
                    self.move_func[piece](row, col, possible_moves)

        return possible_moves

    def get_pawn_moves(self, row, col, moves):
        if self.white_move:  # moves for white pawn
            if self.board[row-1][col] == "__":  # empty space
                moves.append(Move((row, col), (row-1, col), self.board))  # one block forward
                if row == 6 and self.board[row - 2][col] == "__":  # two block forward
                    moves.append(Move((row, col), (row - 2, col), self.board))
            # normal capture (left)
            if col - 1 >= 0 and self.board[row - 1][col - 1][0] == 'b':
                moves.append(Move((row, col), (row - 1, col - 1), self.board))
            # normal capture (right)
            if col + 1 <= 7 and self.board[row - 1][col + 1][0] == 'b':
                moves.append(Move((row, col), (row - 1, col + 1), self.board))
            # todo: implement en passent capture
            # check if the last move is eligible pawn move:
            # last_move = self.move_log[-1]
            # if last_move.piece_moved == "bp" \
            #     and last_move.start_row == 1 \
            #         and last_move.end_row == 3 and row == 3:
            #     if last_move.end_col == col - 1 and self.board[row - 1][col - 1] == "__":  # en passent capture left
            #         moves.append(Move((row, col), (row - 1, col - 1), self.board))
            #     elif last_move.end_col == col + 1 and self.board[row - 1][col + 1] == "__":  # en passent capture right
            #         moves.append(Move((row, col), (row + 1, col + 1), self.board))

        elif not self.white_move:  # moves for black pawn
            if self.board[row+1][col] == "__":  # empty space
                moves.append(Move((row, col), (row+1, col), self.board))  # one block forward
                if row == 1 and self.board[row + 2][col] == "__":  # two block forward
                    moves.append(Move((row, col), (row + 2, col), self.board))
            # normal capture (left)
            if col - 1 >= 0 and self.board[row + 1][col - 1][0] == 'w':
                moves.append(Move((row, col), (row + 1, col - 1), self.board))
            # normal capture (right)
            if col + 1 <= 7 and self.board[row + 1][col + 1][0] == 'w':
                moves.append(Move((row, col), (row + 1, col + 1), self.board))

    def get_rock_moves(self, row, col, moves):
        pass

    def get_knight_moves(self, row, col, moves):
        pass

    def get_bishop_moves(self, row, col, moves):
        pass

    def get_queen_moves(self, row, col, moves):
        pass

    def get_king_moves(self, row, col, moves):
        pass


class Move:

    # maps chess notation with matrix index
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def get_rank_file(self, col, row):
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    # Override equal method
    # Compare obj with other obj
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.piece_moved + ": " + self.get_rank_file(self.start_col, self.start_row) \
            + " go to " + self.get_rank_file(self.end_col, self.end_row)
