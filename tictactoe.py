# this code is inspired by the video "Coding an Unbeatable Tic Tac Toe AI Using Python and the Minimax Algorithm" from the "Coding Spot" channel on Youtube

# You can press the button 'R' to restart the game, "0" to make the AI play randomly, "1" to make the unbeatable AI and "G" to PVP (Player vs Player)

import copy
import sys
import pygame
import numpy as np
import random

from constants import * 

# Creating the game interface using the library "pygame"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AI Tic Tac Toe')
screen.fill(BG_COLOR)

# Class responsible to create the board and check terminal states
class Board:

    # Creating the method init, then our class Board can be a constructor. The attributes are the field and some counters, to know if the space was marked or not
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    # Checking final states, it means we are checking if the game is over or not. If the game is finished, who wins? It's a draw? If the game not over, it means we don't have a result yet, so the program need to keep working.
    def final_state(self, show=False):
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                # Making the victory's vertical line
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]
            
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                # Making the victory's horizontal line
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]
            

        # In this two conditions, we are making the  victory's diagonal line
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]
        
        if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[0][2]
        
        # We are returning the final states to provide as a parameter for AI algorithm, so if the others conditions above don't work, it means we don't have the results yet, so the program need keep working
        return 0

    # This functions is responsible to make the player's round. We are assigning the player number in our numpy array
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    # Using this function to check if the position is empty
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0
    
    # We need this function to use in our AI algorithm, basically we are creating a array with empty positions to AI know what move it can play
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    # Checking if all the squares are filled, if yes, we have a draw
    def isfull(self):
        return self.marked_sqrs == 9
    
    # Just to check if the board just started, because we have 0 marked squares, i.e no ones played yet
    def isempty(self):
        return self.marked_sqrs == 0

class AI:
    # Making our contructor, giving the level and player as attributes. We used this to make the AI level and to attribute the type "cross or circle"
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # The 1st AI, just play random, so we in this function, we are making the AI's move randomly
    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx]

    # This is the most difficult part of this code, the Minimax algorithm. In a few words, we are giving the final state and making the move based on minimax algorithm.
    def minimax(self, board, maximizing):
        case = board.final_state()

        if case == 1:
            return 1, None
        
        if case == 2:
            return -1, None
        
        elif board.isfull():
            return 0, None
        

        # This is how the minimax works. Honestly, I still don't understand completely how it works. We are creating a temporary board to check all the possibilities, maximizing and minimizing, it means the algorithm is trying to make their best move while is thinking in the opponent's best move. Making this, the AI never lose, just draws or win
        if maximizing:
            max_eval = -2
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 2
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    # We use this function to predict the game, because AI check all the possibilities, so if you make a wrong decision, can return a defeat, even if the game don't over yet
    def eval(self, main_board):
        state = ''
        if self.level == 0:
            eval = 'random'
            state = 'random'
            move = self.rnd(main_board)
        else:
            eval, move = self.minimax(main_board, False)
            if eval == 0:
                state = "Empate!"
            elif eval == -1:
                state = "Derrota!"
            else:
                state = "Vitória!"

        
        print(f'O algoritmo escolheu a posição {move} e o jogo será {state}')

        return move
        

class Game:
    # Nothing special here, just dreawing the board and some functionalities
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai' 
        self.running = True
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def show_lines(self):
        screen.fill(BG_COLOR)
        
        # Vertical Lines
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # Horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            # des line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            # asc line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)


    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        if self.gamemode == 'pvp':
            self.gamemode = 'ai'
        else:
            self.gamemode = 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

# This function is our main program, we are just making functionalities to work the game. Hotkeys and checking some stuffs.
def main():

    game = Game()
    board = game.board
    ai = game.ai


    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    game.change_gamemode()

                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                if event.key == pygame.K_0:
                    ai.level = 0
                if event.key == pygame.K_1:
                    ai.level = 1

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()

            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                    game.running = False



        pygame.display.update()

main()