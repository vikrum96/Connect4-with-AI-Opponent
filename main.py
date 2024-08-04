import pygame, sys
from button import Button
from connect4 import *
from connect4_against_ai import *

pygame.init()

width = COL_COUNT * SQ_SIZE
height = (ROW_COUNT+1) * SQ_SIZE

SCREEN = pygame.display.set_mode((width, height))
pygame.display.set_caption("Connect 4")

BG = pygame.image.load("assets/space_bg.png")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def play():
    SCREEN.fill("black")

    board = create_board()
    print(board)
    game_over = False

    draw_board(board, SCREEN)

    pygame.display.update()
    myfont = pygame.font.SysFont("monospace", 75)

    turn = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(SCREEN, BLACK, (0,0, width, SQ_SIZE))
                pos_x = event.pos[0]
                if turn % 2 == PLAYER:
                    pygame.draw.circle(SCREEN, RED, (pos_x, int(SQ_SIZE/2)), RADIUS)
                else:
                    pygame.draw.circle(SCREEN, YELLOW, (pos_x, int(SQ_SIZE/2)), RADIUS)
            
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(SCREEN, BLACK, (0,0, width, SQ_SIZE))
                if turn % 2 == PLAYER:
                    pos_x = event.pos[0]
                    col = int(math.floor(pos_x/SQ_SIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_coin(board, row, col, 1)
                        if win_play(board, row, col, 1):
                            label = myfont.render("Player 1 Wins!", 1, RED)
                            SCREEN.blit(label, (40,10))
                            game_over = True
                else:
                    pos_x = event.pos[0]
                    col = int(math.floor(pos_x/SQ_SIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_coin(board, row, col, 2)
                        if win_play(board, row, col, 2):
                            label = myfont.render("Player 2 Wins!", 1, YELLOW)
                            SCREEN.blit(label, (40,10))
                            game_over = True
                turn += 1
                print(board)
                draw_board(board, SCREEN)
                if game_over:
                    pygame.time.wait(3000)
                    main_menu()

def play_ai():
    SCREEN.fill("black")

    board = create_board()
    print(board)
    game_over = False

    draw_board(board, SCREEN)

    pygame.display.update()
    myfont = pygame.font.SysFont("monospace", 75)

    turn = random.randint(PLAYER, AI)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(SCREEN, BLACK, (0,0, width, SQ_SIZE))
                pos_x = event.pos[0]
                if turn % 2 == 0:
                    pygame.draw.circle(SCREEN, RED, (pos_x, int(SQ_SIZE/2)), RADIUS)
                else:
                    pygame.draw.circle(SCREEN, YELLOW, (pos_x, int(SQ_SIZE/2)), RADIUS)
            
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(SCREEN, BLACK, (0,0, width, SQ_SIZE))
                if turn % 2 == PLAYER:
                    pos_x = event.pos[0]
                    col = int(math.floor(pos_x/SQ_SIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_coin(board, row, col, PLAYER_COIN)
                        if win(board, PLAYER_COIN):
                            label = myfont.render("Player Wins!", 1, RED)
                            SCREEN.blit(label, (100,10))
                            game_over = True
                        turn += 1
                        print(board)
                        draw_board(board, SCREEN)

        if turn % 2 == AI and not game_over:
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)   

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_coin(board, row, col, AI_COIN)
                if win(board, AI_COIN):
                    label = myfont.render("AI Wins!", 1, YELLOW)
                    SCREEN.blit(label, (180,10))
                    game_over = True

                print(board)
                draw_board(board, SCREEN)
                turn += 1

        if game_over:
            pygame.time.wait(3000)
            main_menu()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("Connect 4", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(355, 100))

        PLAY = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(355, 250), 
                            text_input="PLAYER V. PLAYER", font=get_font(20), base_color="White", hovering_color="#a6ff9f")
        PLAY_AI = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(355, 375), 
                            text_input="PLAYER V. AI", font=get_font(20), base_color="White", hovering_color="#a6ff9f")
        QUIT = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(355, 508), 
                            text_input="QUIT", font=get_font(50), base_color="White", hovering_color="#ff756a")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY, PLAY_AI, QUIT]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY.checkForInput(MENU_MOUSE_POS):
                    play()
                elif PLAY_AI.checkForInput(MENU_MOUSE_POS):
                    play_ai()
                elif QUIT.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()