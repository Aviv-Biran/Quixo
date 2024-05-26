import numpy as np
from State import State
from Constants import *

class Quixo:
    def __init__(self, state:State = None) -> None:
        if state == None:
            self.state = State()
        else:
            self.state
        self.arrows = []
        self.winner = 0

    def check_winner(self, state):
        board = state.board

        #looping over all rows to identify row based winner
        for row in range(5):
            first_item = board[1][row + 1]
            if first_item == 0:
                continue
            for col in range(4):
                if board[col + 2][row + 1] != first_item:
                    break
                if col == 3:
                    self.winner = first_item
                    return first_item

        #looping over all columns to identify column based winner
        for col in range(5):
            first_item = board[col + 1][1]
            if first_item == 0:
                continue
            for row in range(4):
                if board[col + 1][row + 2] != first_item:
                    break
                if row == 3:
                    self.winner = first_item
                    return first_item
        
        #looping over the diagonals to identify diagonal based winner
        dia_first_item = board[1][1]
        if dia_first_item == 1 or dia_first_item == 2:
            for dia in range(4):
                if board[dia + 2][dia + 2] != dia_first_item:
                    break
                if dia == 3:
                    self.winner = first_item
                    return dia_first_item
        
        dia_first_item = board[5][1]
        if dia_first_item == 1 or dia_first_item == 2:
            for dia in range(4):
                if board[4 - dia][dia + 2] != dia_first_item:
                    break
                if dia == 3:
                    self.winner = first_item
                    return dia_first_item  
                    
        if self.check_draw(state):
            return 0
        return -1       # No end of game
    
    def is_end_of_game(self, state):
        winner = self.check_winner(state)
        if winner != -1:
            return True
        return False
    
    def reward(self, state):
        winner = self.check_winner(state)
        if winner == -1:
            return 0, False
        if winner == 0:
            return 0, True
        if winner == 1:
            return 1, True
        if winner == 2:
            return -1, True

    def check_draw(self, state):
        row1 = len(np.where(state.board[1] == 0)[0])
        row5 = len(np.where(state.board[5] == 0)[0])
        col1 = len(np.where(state.board[2:5, 1] ==0)[0] + 2)
        col5 = len(np.where(state.board[2:5, 5] == 0)[0] + 2)
        if row1 + row5 + col1 + col5 != 0:
            return False
        return True
    
    def pos_legal(self, state, row_col):
        if self.winner == 0:
            row, col = row_col
            if state.board[row, col] != 0:
                return False
            if (((col == 1 or col == 5) and (row < 6 and row > 0))) \
                or (((row == 1 or row == 5) and (col < 6 and col > 0))):
                return True
        return False

    def change_board(self, row_col, state):
        board = state.board
        board[row_col] = 3

    def get_arrows(self, row_col = None):
        self.arrows = []
        row, col = row_col
        if col == 1:
            self.arrows.append((1, row))
        elif col == 5:
            self.arrows.append((0, row))
        else:
            self.arrows.append((1, row))
            self.arrows.append((0, row))
            
        if row == 1:
            self.arrows.append((3, col))
        elif row == 5:
            self.arrows.append((2, col))
        else:
            self.arrows.append((2, col))
            self.arrows.append((3, col))
    
    def arrow_legal(self, row_col):
        row, col = row_col
        for arrow in self.arrows:
            if arrow[0] == 0:
                if col == 0 and row == arrow[1]:
                    return True
            if arrow[0] == 1:
                if col == 6 and row == arrow[1]:
                    return True
            if arrow[0] == 2:
                if row == 0 and col == arrow[1]:
                    return True
            if arrow[0] == 3:
                if row == 6 and col == arrow[1]:
                    return True
        return False
           
    def move (self, state, action):
        board = state.board
        player = state.player
        row, col = action[0]
        arrow_row, arrow_col = action[1]
        
        if arrow_col == 0:
            board[row, 1:col+1] = np.roll(board[row, 1:col+1], 1)
            board[row, 1] = player
        
        if arrow_col == 6:
            board[row, col: 6] = np.roll(board[row, col:6], -1)
            board[row, 5] = player

        if arrow_row == 0:
            board[1: row+1, col] = np.roll(board[1: row+1, col] , 1)
            board[1, col] = player

        if arrow_row == 6:
            board[row: 6, col] = np.roll(board[row: 6, col] , -1)
            board[5, col] = player

        state.switchPlayers()

    def get_arrow_row_col (self, row_col):
        arrows_row_col = []
        row, col = row_col
        if col == 1:
            arrows_row_col.append((row, 6))
        elif col == 5:
            arrows_row_col.append((row, 0))
        else:
            arrows_row_col.append((row, 0))
            arrows_row_col.append((row, 6))
            
        if row == 1:
            arrows_row_col.append((6, col))
        elif row == 5:
            arrows_row_col.append((0, col))
        else:
            arrows_row_col.append((0, col))
            arrows_row_col.append((6, col))
        return arrows_row_col

    def legal_actions (self, state):
        legal_actions = []
        empty_edges = np.where(state.board[1] == 0)[0]
        for edge in empty_edges:
            arrows_list = self.get_arrow_row_col((1,edge))
            for arrow in arrows_list:
                legal_actions.append(((1,edge), arrow))

        empty_edges = np.where(state.board[5] == 0)[0]
        for edge in empty_edges:
            arrows_list = self.get_arrow_row_col((5,edge))
            for arrow in arrows_list:
                legal_actions.append(((5,edge), arrow))
        
        empty_edges = np.where(state.board[2:5,1] ==0)[0] + 2
        for edge in empty_edges:
            arrows_list = self.get_arrow_row_col((edge,1))
            for arrow in arrows_list:
                legal_actions.append(((edge,1), arrow))

        empty_edges = np.where(state.board[2:5, 5] == 0)[0] + 2
        for edge in empty_edges:
            arrows_list = self.get_arrow_row_col((edge,5))
            for arrow in arrows_list:
                legal_actions.append(((edge,5), arrow))

        return legal_actions
    
    def get_next_state(self, action, state):
        next_state = state.copy()
        board = next_state.board
        player = next_state.player
        row, col = action[0]
        arrow_row, arrow_col = action[1]
        
        if arrow_col == 0:
            board[row, 1:col+1] = np.roll(board[row, 1:col+1], 1)
            board[row, 1] = player
        if arrow_col == 6:
            board[row, col: 6] = np.roll(board[row, col:6], -1)
            board[row, 5] = player
        if arrow_row == 0:
            board[1: row+1, col] = np.roll(board[1: row+1, col] , 1)
            board[1, col] = player
        if arrow_row == 6:
            board[row: 6, col] = np.roll(board[row: 6, col] , -1)
            board[5, col] = player

        next_state.switchPlayers()
        return next_state
