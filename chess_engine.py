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
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []