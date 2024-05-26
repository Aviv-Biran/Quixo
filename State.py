import numpy as np
import torch

class State:
    def __init__(self, board = None, player = 1) -> None:
        if board is not None:
            self.board = board
        else:
            self.board = np.array([
                [3,3,3,3,3,3,3],
                [3,0,0,0,0,0,3],
                [3,0,0,0,0,0,3],
                [3,0,0,0,0,0,3],
                [3,0,0,0,0,0,3],
                [3,0,0,0,0,0,3],
                [3,3,3,3,3,3,3]])
        self.player = player

    def switchPlayers(self):
        if self.player == 1:
           self.player = 2
        else:
            self.player = 1

    def copy(self):
        newBoard = np.copy(self.board)
        return State(board = newBoard, player = self.player)

    def toTensor(self, device = torch.device('cpu')):
        board_np = self.board[1:6, 1:6].reshape(-1)
        board_tensor = torch.tensor(board_np, dtype = torch.float32, device = device)
        return board_tensor
    
    @staticmethod
    def tensorToState(tensor, player = 1):
        np_board = tensor.detach().cpu().numpy().astype(int)
        np_board = np_board.reshape(5,5)
        board = np.array([
                [3,3,3,3,3,3,3],
                [3,0,0,0,0,0,3],
                [3,0,0,0,0,0,3],
                [3,0,0,0,0,0,3],
                [3,0,0,0,0,0,3],
                [3,0,0,0,0,0,3],
                [3,3,3,3,3,3,3]])
        board[1:6, 1:6] = np_board
        state = State(board, player = player)
        return state
