'''
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object
'''

import pygame as p
import chess_engine

WIDTH = HEIGHT = 512 #400 is another option
DIMENSION = 8 #dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #for animations later on
IMAGES = {}

'''
initialize a global dictionary of images. this is called exactly once in the main
'''
def load_images():
    pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wp', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

'''
The main driver for our code, this will handle user input and pdating the graphics
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chess_engine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False #flag variable for when a move is made

    load_images() #only do once before while loop
    running = True
    sq_selected = () #keep track of the last click of the user (row, col)
    player_clicks = [] #keeps track of player clicks (two tuples)
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sq_selected == (row, col): #if user clicked same sq twice
                    sq_selected = () #deselect
                    player_clicks = [] #clear player clicks
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)  #append for both clicks
                if len(player_clicks) == 2:
                    move = chess_engine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                        sq_selected = () #reset user clicks
                        player_clicks = []
                    else: # save first click
                        player_clicks = [sq_selected]
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when z is pressed
                    gs.undo_move()
                    move_made = True
        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


#responsible for all the graphics within a current game state
def draw_game_state(screen, gs):
    draw_board(screen) #draw squares on the board
    #can add piece highlighting or move suggestions here (later)
    draw_pieces(screen, gs.board) #draw pieces on top of squares

#top left square of board is always light
def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


#draw pieces on the board using the current game_state.board
def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not an empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()        

