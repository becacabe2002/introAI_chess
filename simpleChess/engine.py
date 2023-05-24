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
        self.move_log = []  # save made moves

        # variables to keep track of king pieces (for implementing checkmate)
        self.white_king_pos = (7, 4)  # similar to row 1, col e
        self.black_king_pos = (0, 4)  # similar to row 8, col e

        self.move_func = {'p': self.get_pawn_moves, 'R': self.get_rook_moves,
                          'N': self.get_knight_moves, 'B': self.get_bishop_moves,
                          'Q': self.get_queen_moves, 'K': self.get_king_moves}
        self.check_mate = False  # King is in check and doesnt have any valid move -> Win
        self.stale_mate = False  # King is not in check but doesnt have any valid move -> Draw
        self.in_check = False
        self.pins = []
        self.checks = []

    def make_a_move(self, move):
        self.board[move.start_row][move.start_col] = "__"
        self.board[move.end_row][move.end_col] = move.piece_moved
        # save move to log list to undo if necessary
        self.move_log.append(move)
        # swap player
        self.white_move = not self.white_move
        # update the King position if it is moved
        if move.piece_moved == "wK":
            self.white_king_pos = (move.end_row, move.end_col)
        if move.piece_moved == "bK":
            self.black_king_pos = (move.end_row, move.end_col)

    def undo_move(self):
        if len(self.move_log) != 0:  # check whether is a move performed
            last_move = self.move_log.pop()
            self.board[last_move.start_row][last_move.start_col] = last_move.piece_moved
            self.board[last_move.end_row][last_move.end_col] = last_move.piece_captured
            self.white_move = not self.white_move
            if last_move.piece_moved == "wK":
                self.white_king_pos = (last_move.start_row, last_move.start_col)
            if last_move.piece_moved == "bK":
                self.black_king_pos = (last_move.start_row, last_move.start_col)

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

        moves = []
        self.in_check, self.pins, self.checks = self.check_pins_and_checks()

        if self.white_move:
            king_row = self.white_king_pos[0]
            king_col = self.white_king_pos[1]
        else:
            king_row = self.black_king_pos[0]
            king_col = self.black_king_pos[1]

        if self.in_check:
            if len(self.checks) == 1:  # only 1 check, block the check or move the king
                moves = self.gen_possible_moves()
                # to block the check you must put a piece into one of the squares between the enemy piece and your king
                check = self.checks[0]  # check information
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []  # squares that pieces can move to
                # if knight, must capture the knight or move your king, other pieces can be blocked
                if piece_checking[1] == "N":
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)  # check[2] and check[3] are the check directions
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:  # once you get to piece and check
                            break
                # get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1):  # iterate through the list backwards when removing elements
                    if moves[i].piece_moved[1] != "K":  # move doesn't move king so it must block or capture
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:  # move doesn't block or capture piece
                            moves.remove(moves[i])
            else:  # double check, king has to move
                self.get_king_moves(king_row, king_col, moves)
        else:  # not in check - all moves are fine
            moves = self.gen_possible_moves()

        # Update game state: checkMate and staleMate
        if len(moves) == 0:
            if self.is_in_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False
        return moves

    def is_in_check(self):
        if self.white_move:
            return self.is_square_attacked(self.white_king_pos[0], self.white_king_pos[1])
        else:
            return self.is_square_attacked(self.black_king_pos[0], self.black_king_pos[1])

    def is_square_attacked(self, row, col):
        self.white_move = not self.white_move
        opponent_moves = self.gen_possible_moves()  # generate all possible move of opponent
        self.white_move = not self.white_move
        for m in opponent_moves:
            if m.end_row == row and m.end_col == col:
                return True
        return False

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

    def check_pins_and_checks(self):
        pins = []  # squares pinned and the direction its pinned from
        checks = []  # squares where enemy is applying a check
        in_check = False
        if self.white_move:
            enemy_color = "b"
            ally_color = "w"
            start_row = self.white_king_pos[0]
            start_col = self.white_king_pos[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            start_row = self.black_king_pos[0]
            start_col = self.black_king_pos[1]
        # check outwards from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            direction = directions[j]
            possible_pin = ()  # reset possible pins
            for i in range(1, 8):
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != "K":
                        if possible_pin == ():  # first allied piece could be pinned
                            possible_pin = (end_row, end_col, direction[0], direction[1])
                        else:  # 2nd allied piece - no check or pin from this direction
                            break
                    elif end_piece[0] == enemy_color:
                        enemy_type = end_piece[1]
                        # 5 possibilities in this complex conditional
                        # 1.) orthogonally away from king and piece is a rook
                        # 2.) diagonally away from king and piece is a bishop
                        # 3.) 1 square away diagonally from king and piece is a pawn
                        # 4.) any direction and piece is a queen
                        # 5.) any direction 1 square away and piece is a king
                        if (0 <= j <= 3 and enemy_type == "R") or \
                                (4 <= j <= 7 and enemy_type == "B") or \
                                (i == 1 and enemy_type == "p" and ((enemy_color == "w" and 6 <= j <= 7) or (enemy_color == "b" and 4 <= j <= 5))) or \
                                (enemy_type == "Q") or (i == 1 and enemy_type == "K"):
                            if possible_pin == ():  # no piece blocking, so check
                                in_check = True
                                checks.append((end_row, end_col, direction[0], direction[1]))
                                break
                            else:  # piece blocking so pin
                                pins.append(possible_pin)
                                break
                        else:  # enemy piece not applying checks
                            break
                else:
                    break  # off board
        # check for knight checks
        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == "N":  # enemy knight attacking a king
                    in_check = True
                    checks.append((end_row, end_col, move[0], move[1]))
        return in_check, pins, checks

    def get_pawn_moves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()

        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_move:  # moves for white pawn
            if self.board[row - 1][col] == "__":  # empty space
                moves.append(Move((row, col), (row - 1, col), self.board))  # one block forward
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
            if self.board[row + 1][col] == "__":  # empty space
                moves.append(Move((row, col), (row + 1, col), self.board))  # one block forward
                if row == 1 and self.board[row + 2][col] == "__":  # two block forward
                    moves.append(Move((row, col), (row + 2, col), self.board))
            # normal capture (left)
            if col - 1 >= 0 and self.board[row + 1][col - 1][0] == 'w':
                moves.append(Move((row, col), (row + 1, col - 1), self.board))
            # normal capture (right)
            if col + 1 <= 7 and self.board[row + 1][col + 1][0] == 'w':
                moves.append(Move((row, col), (row + 1, col + 1), self.board))

            # todo: implement pawn promotions

    def get_rook_moves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != "Q":  # can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break

        # rook's moving directions: forward, backward, right, lef
        directions = ((-1, 0), (1, 0), (0, 1), (0, -1))
        enemy_color = 'b' if self.white_move else 'w'
        for d in directions:
            for i in range(1, 8):  # 7 block is the maximum
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # make sure that it is still on board
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "__":  # empty space
                            new_move = Move((row, col), (end_row, end_col), self.board)
                            moves.append(new_move)
                        elif end_piece[0] == enemy_color:  # if there is enemy on the way, capture the first one
                            new_move = Move((row, col), (end_row, end_col), self.board)
                            moves.append(new_move)
                            break
                        else:
                            break
                else:
                    break

    def get_knight_moves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        positions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = 'w' if self.white_move else 'b'
        for p in positions:
            end_row = row + p[0]
            end_col = col + p[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color: # not an ally piece (empty or enemy piece)
                        moves.append(Move((row, col), (end_row, end_col), self.board))
            else:
                continue

    def get_bishop_moves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = 'b' if self.white_move else 'w'
        for d in directions:
            for i in range(1, 8):  # 7 block is the maximum
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # make sure that it is still on board
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "__":  # empty space
                            new_move = Move((row, col), (end_row, end_col), self.board)
                            moves.append(new_move)
                        elif end_piece[0] == enemy_color:  # if there is enemy on the way, capture the first one
                            new_move = Move((row, col), (end_row, end_col), self.board)
                            moves.append(new_move)
                            break
                        else:
                            break
                else: # off board
                    break

    def get_queen_moves(self, row, col, moves):
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

    def get_king_moves(self, row, col, moves):
        positions = ((-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1), (0, -1), (0, 1))
        ally_color = 'w' if self.white_move else 'b'
        for p in positions:
            end_row = row + p[0]
            end_col = col + p[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] is not ally_color:
                    moves.append(Move((row, col), (end_row, end_col), self.board))
            else:
                continue


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
