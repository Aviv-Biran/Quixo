import numpy as np
import pygame
import time 
from Constants import *
from Quixo import Quixo
from State import State

pygame.init()

class Graphics:
    def __init__(self, win, env : Quixo):
        self.win = win
        self.env = env
        
    def paint_grid(self, board): 
        for i in range(7):
            for j in range(7):
                place = board[j][i]
                if place == 0:
                    pygame.draw.rect(self.win, SQR, (100 * i, 100 * j, 100, 100))
                elif place == 1:
                    pygame.draw.rect(self.win, SQR, (100 * i, 100 * j, 100, 100))
                    pygame.draw.line(self.win, BLACK, (100 * i + 15, 100 * j + 15), (100 * i + 85, 100 * j + 85), 7)
                    pygame.draw.line(self.win, BLACK, (100 * i + 15, 100 * j + 85), (100 * i + 85, 100 * j + 15), 7)
                elif place == 2:
                    pygame.draw.rect(self.win, SQR, (100 * i, 100 * j, 100, 100))
                    pygame.draw.circle(self.win, BLACK, (100 * i + 50, 100 * j + 50), 35, 5)
                if place == 3:
                    pygame.draw.rect(self.win, BOARD, (100 * i, 100 * j, 100, 100))

    def draw_lines(self):
        for i in range(6):
                pygame.draw.line(self.win, WHITE, (100, i * SQUARE_SIZE + 100), (WIDTH1, i * SQUARE_SIZE + 100), width=LINE_WIDTH)
                pygame.draw.line(self.win, WHITE, (i * SQUARE_SIZE + 100, 100), (i * SQUARE_SIZE + 100, HEIGHT2), width=LINE_WIDTH)
        pygame.draw.line(self.win, WHITE, (0, 7 * SQUARE_SIZE), (WIDTH, 7 * SQUARE_SIZE), width=LINE_WIDTH)

    def draw_bank_lines(self):
        pygame.draw.line(self.win, WHITE, (300,  7.5 * SQUARE_SIZE), (400, 7.5 * SQUARE_SIZE ), width=LINE_WIDTH)
        pygame.draw.line(self.win, WHITE, (300, 8.5 * SQUARE_SIZE), (400, 8.5 * SQUARE_SIZE ), width=LINE_WIDTH)
        pygame.draw.line(self.win, WHITE, (300, 7.5 * SQUARE_SIZE), (300 , 8.5 * SQUARE_SIZE), width=LINE_WIDTH)
        pygame.draw.line(self.win, WHITE, (400, 7.5 * SQUARE_SIZE), (400, 8.5 * SQUARE_SIZE), width=LINE_WIDTH)

    def draw_arrows(self, arrows):
        for arrow in arrows:
            if arrow[0] == 0:
                self.draw_arrow_right(arrow[1])
            if arrow[0] == 1:
                self.draw_arrow_left(arrow[1])
            if arrow[0] == 2:
                self.draw_arrow_down(arrow[1])
            if arrow[0] == 3:
                self.draw_arrow_up(arrow[1])
                
    def draw_arrow_down(self, pos = None):
        if pos:
            pygame.draw.line(self.win, WHITE, (pos * 100 + 50, 25), (pos * 100 + 50, 70), 3)
            pygame.draw.line(self.win, WHITE, (pos * 100 + 40, 55), (pos * 100 + 50, 70), 3)
            pygame.draw.line(self.win, WHITE, (pos * 100 + 60, 55), (pos * 100 + 50, 70), 3)

    def draw_arrow_up(self, pos = None):
        if pos:
            pygame.draw.line(self.win, WHITE, (pos * 100 + 50, 630), (pos * 100 + 50, 675), 3)
            pygame.draw.line(self.win, WHITE, (pos * 100 + 40, 645), (pos * 100 + 50, 630), 3)
            pygame.draw.line(self.win, WHITE, (pos * 100 + 60, 645), (pos * 100 + 50, 630), 3)

    def draw_arrow_right(self, pos = None):
        if pos:
            pygame.draw.line(self.win, WHITE, (25, pos * 100 + 50), (70, pos * 100 + 50), 3)
            pygame.draw.line(self.win, WHITE, (55, pos * 100 + 40), (70, pos * 100 + 50), 3)
            pygame.draw.line(self.win, WHITE, (55, pos * 100 + 60), (70, pos * 100 + 50), 3)

    def draw_arrow_left(self, pos = None):
        if pos:
            pygame.draw.line(self.win, WHITE, (630, pos * 100 + 50), (675, pos * 100 + 50), 3)
            pygame.draw.line(self.win, WHITE, (645, pos * 100 + 40), (630, pos * 100 + 50), 3)
            pygame.draw.line(self.win, WHITE, (645, pos * 100 + 60), (630, pos * 100 + 50), 3)
        
    def endofgame(self, winner):
        if winner == 1 or winner == 2:
            time.sleep(1.5)
            self.win.fill(GREEN)
            self.fill_bank(winner)
            self.draw_bank_lines()
            print("The winner is player number " , winner)
            self.handle_win(winner)
        elif winner == 0:
            print("It's a tie")
            self.handle_draw()

    def handle_win(self, winner):
        pygame.font.init()
        font = pygame.freetype.SysFont('Comic Sans MS', 100)       
        if winner == 1:
            text_surface, rect = font.render("X WON!", WHITE)
            self.win.blit(text_surface, (180, 250))
        if winner == 2:
            text_surface, rect = font.render("O WON!", WHITE)
            self.win.blit(text_surface, (180, 250))
        pygame.display.flip()

    def handle_draw(self):
        time.sleep(1)
        self.win.fill(RED)
        pygame.font.init()
        font = pygame.freetype.SysFont('Comic Sans MS', 100)            
        text_surface, rect = font.render("DRAW!", WHITE)
        self.win.blit(text_surface, (200, 250))
        pygame.display.flip()

    def get_Row_col (self, pos):
        col = int((pos)[0] // 100)
        row = int((pos)[1] // 100)
        return (row, col)
    
    def fill_bank(self, player = 0):
        if player and player != 0:
            pygame.draw.rect(self.win, SQR, (300, 750, 100, 100))
            if player == 1:
                pygame.draw.line(self.win, BLACK, (WIDTH2 - 35, 765), (WIDTH2 + 35, 835), 7)
                pygame.draw.line(self.win, BLACK, (WIDTH2 - 35, 835), (WIDTH2 + 35, 765), 7)
            elif player == 2:
                pygame.draw.circle(self.win, BLACK, (WIDTH2, 800), 35, 5)

    def empty_bank(self):
        pygame.draw.rect(self.win, BOARD, (300, 750, 100, 100))
        self.draw_bank_lines()

    def draw(self, state:State):
        board = state.board
        arrows = self.env.arrows
        self.paint_grid(board)
        self.draw_lines()
        self.draw_bank_lines()
        self.draw_arrows(arrows)