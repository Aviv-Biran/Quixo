import pygame
from Constants import *

class Human_Agent:

    def __init__(self, player: int, env = None, graphics = None) -> None:
        self.player = player
        self.mode = 0
        self.pos = None
        self.original_state = None
        self.env = env 
        self.graphics = graphics

    def get_player_number(self):
        return self.player
    
    def get_Action(self, events, state, train = False):        
        if self.mode == 0:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = self.graphics.get_Row_col(pygame.mouse.get_pos())
                    print("pos: ", pos)
                    if self.env.pos_legal(state, pos):
                        self.original_state = state.copy()
                        self.env.change_board(pos, state)
                        self.env.get_arrows(row_col = pos)
                        self.graphics.fill_bank(state.player)
                        self.graphics.draw(state)
                        self.pos = pos
                        self.mode = 1
                        return None
        elif self.mode == 1:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = self.graphics.get_Row_col(pygame.mouse.get_pos())
                    print("arrow: ", pos)
                    if self.env.arrow_legal(pos):
                        action = (self.pos, pos)
                        self.env.state = self.original_state
                        self.graphics.empty_bank()
                        self.env.arrows = []
                        self.mode = 0
                        return action
