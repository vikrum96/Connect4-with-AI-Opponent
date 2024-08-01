import numpy as np
import random
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
AI = 1

EMPTY = 0
PLAYER_COIN = 1
AI_COIN = 2

WINDOW_LENGTH = 4

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
             if board[r][c] == PLAYER_COIN:
                pygame.draw.circle(screen, RED, (int(c*SQ_SIZE+SQ_SIZE/2), int(r*SQ_SIZE+SQ_SIZE+SQ_SIZE/2)), RADIUS)
             elif board[r][c] == AI_COIN: 
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

def win(board, coin):
    # Check horizontal locations for win
	for c in range(COL_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == coin and board[r][c+1] == coin and board[r][c+2] == coin and board[r][c+3] == coin:
				return True

	# Check vertical locations for win
	for c in range(COL_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == coin and board[r+1][c] == coin and board[r+2][c] == coin and board[r+3][c] == coin:
				return True

	# Check positively sloped diaganols
	for c in range(COL_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == coin and board[r+1][c+1] == coin and board[r+2][c+2] == coin and board[r+3][c+3] == coin:
				return True

	# Check negatively sloped diaganols
	for c in range(COL_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == coin and board[r-1][c+1] == coin and board[r-2][c+2] == coin and board[r-3][c+3] == coin:
				return True


## AI Methods ##

def get_valid_locations(board):
	valid_locations = []
	for col in range(COL_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, coin):
	valid_locations = get_valid_locations(board)
	best_score = 0
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_coin(temp_board, row, col, coin)
		score = score_position(temp_board, coin)
		if best_score < score:
			best_score = score
			best_col = col

	return best_col

def evaluate_window(window, coin):
	score = 0
	opp_coin = PLAYER_COIN if coin == PLAYER_COIN else AI_COIN

	if window.count(coin) == 4:
		score += 100
	elif window.count(coin) == 3 and window.count(EMPTY) == 1:
		score += 10 # maybe 5
	elif window.count(coin) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_coin) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score


def score_position(board, coin):
    score = 0

	## Score center column
    center_array = [int(i) for i in list(board[:, COL_COUNT//2])]
    center_count = center_array.count(coin)
    score += center_count * 3

	## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COL_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, coin)

	## Score Vertical
    for c in range(COL_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, coin)

	## Score posiive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COL_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, coin)

    for r in range(ROW_COUNT-3):
        for c in range(COL_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, coin)
    
    return score

def is_terminal_node(board):
	return win(board, PLAYER_COIN) or win(board, AI_COIN) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if win(board, AI_COIN):
				return (None, 100000000000000)
			elif win(board, PLAYER_COIN):
				return (None, -10000000000000)
			else:
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_COIN))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_coin(b_copy, row, col, AI_COIN)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_coin(b_copy, row, col, PLAYER_COIN)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value


board = create_board()
print(board)
game_over = False

pygame.init()

width = COL_COUNT * SQ_SIZE
height = (ROW_COUNT+1) * SQ_SIZE

screen = pygame.display.set_mode((width, height))
draw_board(board)

pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQ_SIZE))
            pos_x = event.pos[0]
            if turn % 2 == 0:
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
                    drop_coin(board, row, col, PLAYER_COIN)
                    if win(board, PLAYER_COIN):
                        label = myfont.render("Player 1 Wins!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True
                    turn += 1
                    print(board)
                    draw_board(board)

    if turn % 2 == AI and not game_over:
        
        #col = pick_best_move(board, AI_COIN)
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)   

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_coin(board, row, col, AI_COIN)
            if win(board, AI_COIN):
                label = myfont.render("Player 2 Wins!", 1, YELLOW)
                screen.blit(label, (40,10))
                game_over = True

            print(board)
            draw_board(board)
            turn += 1

    if game_over:
        pygame.time.wait(3000)

