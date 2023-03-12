'''
This is responsible for storing all the info about the current state of a chess game. It will also be responsible
for determining the valid moves at the current state. It will also keep a move Log.
'''

class GameState():
    def __init__(self):
        #for ai - should change to use numpy array
        #board is 8x8 2d list, each element has 2 characters
        #first character represents color of piece(b or w)
        #second character represents the type of piece (K, Q, R, B, N or p)
        #"--" represents an empty space with no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.move_functions = {'p': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves, 
                               'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}

        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7,4)
        self.black_king_location = (0,4)
        self.check_mate = False
        self.stale_mate = False

    #executes move(will not work for castling, pawn promotion, en-passant)
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move) #log move so we can undo it later
        self.white_to_move = not self.white_to_move #swap players
        #update king's location if moved
        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)


    #undo last move
    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            #update king's position if needed
            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_col)

    #all moves considering checks
    def get_valid_moves(self):
        #generate all moves
        moves = self.get_all_possible_moves()
        #for each move, make the move
        for i in range(len(moves)-1, -1, -1): #when removing from a list, go backwards through the list so itterator doesn't miss values
            self.make_move(moves[i])
            #generate all opponents moves
            #for each of opponents moves, see if they attack your king
            self.white_to_move = not self.white_to_move 
            if self.in_check():
                moves.remove(moves[i]) #if they attack your king, not a valid move
            self.white_to_move = not self.white_to_move
            self.undo_move()
        if len(moves) == 0: #either checkmate or stalemate
            if self.in_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False
        return moves
    
    #determines if current player is in check
    def in_check(self):
        if self.white_to_move:
            #if square is under attack, player is in check
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    #determine if the enemy can attack the square r,c
    def square_under_attack(self, r, c):
        self.white_to_move = not self.white_to_move #deitch to opponent's turn
        opp_move = self.get_all_possible_moves() 
        self.white_to_move = not self.white_to_move #switch turns back
        for move in opp_move:
            if move.end_row == r and move.end_col == c: #square is under attack
                return True
        return False

    #all moves without considering checks
    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)): #num of rows
            for c in range(len(self.board[r])): #num of cols
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)
        return moves


    #get all pawn moves for pawn located at row, col and add these moves to list
    def get_pawn_moves(self, r, c, moves):
        if self.white_to_move: #white pawn moves
            if self.board[r-1][c] == "--": #moving forward by decreasing row
                moves.append(Move((r,c), (r-1,c),self.board)) #moves pawn 1 forward
                if r == 6 and self.board[r-2][c] == "--": #pawn can move 2 spaces on first move
                    moves.append(Move((r,c), (r-2,c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == "b": #emeny piece to capture left diagonal
                    moves.append(Move((r,c), (r-1,c-1),self.board))
            if c+1 < 7: #last col in board
                if self.board[r-1][c+1][0] == "b": #piece to capture right diagonal
                    moves.append(Move((r,c), (r-1,c+1),self.board))

        else: #black pawn moves
            if self.board[r+1][c] == "--": #moving forward by decreasing row
                moves.append(Move((r,c), (r+1,c),self.board)) #moves pawn 1 forward
                if r == 1 and self.board[r+2][c] == "--": #pawn can move 2 spaces on first move
                    moves.append(Move((r,c), (r+2,c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == "w": #emeny piece to capture left diagonal
                    moves.append(Move((r,c), (r+1,c-1),self.board))
            if c+1 < 7: #last col in board
                if self.board[r+1][c+1][0] == "w": #piece to capture right diagonal
                    moves.append(Move((r,c), (r+1,c+1),self.board))

        #add pawn promotions later


    #get all rook moves for pawn located at row, col and add these moves to list
    def get_rook_moves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #up, left, down, right (row, col)
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1,8):
                end_row = r + d[0] * i #take current r, add direction and mulitply by number of spots you can move (up tp 7)
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8: #on board
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((r,c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r,c), (end_row, end_col), self.board))
                        break
                    else: #friendly piece invalid
                        break
                else: #off board
                    break
    
    def get_knight_moves(self, r, c, moves):
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = "w" if self.white_to_move else "b"
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((r,c), (end_row, end_col), self.board))

    def get_bishop_moves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) 
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1,8):
                end_row = r + d[0] * i #take current r, add direction and mulitply by number of spots you can move (up tp 7)
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8: #on board
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((r,c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r,c), (end_row, end_col), self.board))
                        break
                    else: #friendly piece invalid
                        break
                else: #off board
                    break

    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)

    def get_king_moves(self, r, c, moves):
        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally_color = "w" if self.white_to_move else "b"
        for i in range(8):
            end_row = r + king_moves[i][0]
            end_col = c + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((r,c), (end_row, end_col), self.board))


class Move():
    #map key:value pairs for rows and cols
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v:k for k,v in ranks_to_rows.items()}
    files_to_col = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v:k for k,v in files_to_col.items()}


    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        #print(self.move_id)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False
    

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]