from Quixo import Quixo
from State import State
MAXSCORE = 1000

class Alpha_Beta_Agent:

    def __init__(self, player, depth = 4, env = None):
        self.player = player
        if self.player == 1:
            self.opponent = 2
        else:
            self.opponent = 1
        self.depth = depth
        self.env = env

    def evaluate(self, state): # my evaluate
        # go on all rows and calculate
        # go on all columns and calculate
        
        board = state.board[1:6, 1:6]
        winner = self.env.check_winner(state)
        if winner != -1:
            if winner == 0:
                return 0
            elif self.player == winner:
                return 100
            else:
                return -100

        rows_1 = (board == 1).sum(axis = 1)
        cols_1 = (board == 1).sum(axis = 0)
        rows_2 = (board == 2).sum(axis = 1)
        cols_2 = (board == 2).sum(axis = 0)

        empty_rows_1 = rows_1*(rows_2 == 0)
        empty_rows_1[empty_rows_1==1]=0
        empty_cols_1 = cols_1*(cols_2 == 0)
        empty_cols_1[empty_cols_1==1]=0
        empty_rows_2 = rows_2*(rows_1 == 0)
        empty_rows_2[empty_rows_2==1]=0
        empty_cols_2 = cols_2*(cols_1 == 0)
        empty_cols_2[empty_cols_2==1]=0

        value1 = (empty_rows_1.sum() + empty_cols_1.sum()) * 2
        value2 = (empty_rows_2.sum() + empty_cols_2.sum()) * 2

        if self.player == 1:
          return value1 - value2
        else:
          return value2 - value1

    def get_Action(self, events = None, state = None, train = False):
        visited = set()
        value, bestAction = self.minMax(state, visited)
        return bestAction

    def minMax(self, state, visited):
        depth = 0
        alpha = -MAXSCORE
        beta = MAXSCORE
        return self.max_value(state, visited, depth, alpha, beta)

    def max_value (self, state, visited, depth, alpha, beta):
        
        value = -MAXSCORE

        # stop state
        if depth == self.depth or self.env.is_end_of_game(state):
            value = self.evaluate(state)
            return value, None
        
        # start recursion
        bestAction = None
        legal_actions = self.env.legal_actions(state)
        for action in legal_actions:
            newState = self.env.get_next_state(action, state)
            if newState not in visited:
                visited.add(newState)
                newValue, newAction = self.min_value(newState, visited,  depth + 1, alpha, beta)
                if newValue > value:
                    value = newValue
                    bestAction = action
                    alpha = max(alpha, value)
                if value >= beta:
                    return value, bestAction
                    

        if bestAction:    
            return value, bestAction 
        else:               # happend when all child states are in visited. return maxScore
            return MAXSCORE, bestAction

    def min_value (self, state, visited, depth, alpha, beta):
        
        value = MAXSCORE

        # stop state
        if depth == self.depth or self.env.is_end_of_game(state):
            value = self.evaluate(state)
            return value, None
        
        # start recursion
        bestAction = None
        legal_actions = self.env.legal_actions(state)
        for action in legal_actions:
            newState = self.env.get_next_state(action, state)
            if newState not in visited:
                visited.add(newState)
                newValue, newAction = self.max_value(newState, visited,  depth + 1, alpha, beta)
                if newValue < value:
                    value = newValue
                    bestAction = action
                    beta = min(beta, value)
                if value <= alpha:
                    return value, bestAction

        if bestAction:
            return value, bestAction 
        else:
            return -MAXSCORE, bestAction
 
    def get_state_action (self, events = None, state = None, epoch = 0, train = False):
        action = self.get_Action(state = state)
        if action == None:
            print (state)
        next_state = self.env.get_next_state(action, state)
        return next_state.toTensor(), action