import numpy as np
import pygame
import sys
import math

# Global Variables
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COL_COUNT = 7

SQ_SIZE = 100
RADIUS = int(SQ_SIZE/2 - 5)

PLAYER = 0

def create_board():
    board = np.zeros((ROW_COUNT, COL_COUNT))
    return board

def draw_board(board):
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQ_SIZE, r*SQ_SIZE+SQ_SIZE, SQ_SIZE, SQ_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQ_SIZE+SQ_SIZE/2), int(r*SQ_SIZE+SQ_SIZE+SQ_SIZE/2)), RADIUS)
	
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):		
             if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQ_SIZE+SQ_SIZE/2), int(r*SQ_SIZE+SQ_SIZE+SQ_SIZE/2)), RADIUS)
             elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQ_SIZE+SQ_SIZE/2), int(r*SQ_SIZE+SQ_SIZE+SQ_SIZE/2)), RADIUS)
    pygame.display.update()

def drop_coin(board, row, col, coin):
    board[row][col] = coin

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for row in range(ROW_COUNT-1, -1, -1):
        if board[row][col] == 0:
            return row

def vertical_check(board, row, col, coin):
    if row <= ROW_COUNT-4:
        for r in range(row, row+4, 1):
            if board[r][col] != coin:
                return False
        return True
    else:
        return False

def horizontal_check(board, row, col, coin):
    num_coins = 1
    # Check backwards
    if col >= 0:
        for c in range(col-1, -1, -1):
            if board[row][c] == coin:
                num_coins += 1
            else:
                break

    # Check forwards
    if col < COL_COUNT-1:
        for c in range(col+1, COL_COUNT, 1):
            if num_coins == 4:
                return True
            elif board[row][c] == coin:
                num_coins += 1
            else:
                break
    
    return num_coins == 4

def diagonal_check(board, row, col, coin):
    num_coins = 1
    # Check up-left
    if row > 0 and col > 0:
        r = row-1
        c = col-1
        while r >= 0 and c >= 0:
            if board[r][c] == coin:
                num_coins += 1
            else:
                break
            if num_coins == 4:
                return True
            r -= 1
            c -= 1
        
    # Check down-right
    if row < ROW_COUNT-1 and col < COL_COUNT-1:
        r = row+1
        c = col+1
        while r < ROW_COUNT and c < COL_COUNT:
            if board[r][c] == coin:
                num_coins += 1
            else: 
                break
            if num_coins == 4:
                return True
            r += 1
            c += 1
    
    num_coins = 1
    # Check up-right
    if row > 0 and col < COL_COUNT-1:
        r = row-1
        c = col+1
        while r >= 0 and c < COL_COUNT:
            if board[r][c] == coin:
                num_coins += 1
            else: 
                break
            if num_coins == 4:
                return True
            r -= 1
            c += 1
    
    # Check down-left
    if row < ROW_COUNT-1 and col > 0:
        r = row+1
        c = col-1
        while r < ROW_COUNT and c >= 0:
            if board[r][c] == coin:
                num_coins += 1
            else: 
                break
            if num_coins == 4:
                return True
            
            r += 1
            c -= 1
    
    return False

def win(board, row, col, coin):
    # Going from last played move
    return True if vertical_check(board, row, col, coin) or horizontal_check(board, row, col, coin) or diagonal_check(board, row, col, coin) else False

board = create_board()
print(board)
game_over = False
turn = 0

pygame.init()

width = COL_COUNT * SQ_SIZE
height = (ROW_COUNT+1) * SQ_SIZE

screen = pygame.display.set_mode((width, height))
draw_board(board)

pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQ_SIZE))
            pos_x = event.pos[0]
            if turn % 2 == PLAYER:
                pygame.draw.circle(screen, RED, (pos_x, int(SQ_SIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (pos_x, int(SQ_SIZE/2)), RADIUS)
        
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQ_SIZE))
            if turn % 2 == PLAYER:
                pos_x = event.pos[0]
                col = int(math.floor(pos_x/SQ_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_coin(board, row, col, 1)
                    if win(board, row, col, 1):
                        label = myfont.render("Player 1 Wins!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True
            else:
                pos_x = event.pos[0]
                col = int(math.floor(pos_x/SQ_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_coin(board, row, col, 2)
                    if win(board, row, col, 2):
                        label = myfont.render("Player 2 Wins!", 1, YELLOW)
                        screen.blit(label, (40,10))
                        game_over = True
            turn += 1
            print(board)
            draw_board(board)
            if game_over:
                pygame.time.wait(3000)

