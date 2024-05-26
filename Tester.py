from Random_Agent import Random_Agent
from DQN_Agent import DQN_Agent
from Min_Max_Agent import Min_Max_Agent
from Quixo import Quixo
from State import State

class Tester:
    def __init__(self, env, player1, player2) -> None:
        self.env : Quixo = env
        self.player1 = player1
        self.player2 = player2

    def test (self, games_num):
        env = self.env
        player = self.player1
        player1_win = 0
        player2_win = 0
        games = 0
        while games < games_num:
            action = player.get_Action(state = env.state, events = None, train = None)
            env.move(action=action, state=env.state)
            player = self.switchPlayers(player)
            winner = env.check_winner(env.state)
            if winner != -1:
                if winner == 1:
                    player1_win += 1
                elif winner == 2:
                    player2_win += 1
                env.state = State()
                games += 1
                player = self.player1
        return player1_win, player2_win

    def switchPlayers(self, player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1
        

    def __call__(self, games_num):
        return self.test(games_num)

if __name__ == '__main__':
    env = Quixo()
    #player1 = DQN_Agent(player = 1, train = True, env=env, parametes_path="Data/params_113.pth")
    #player1 = Random_Agent(player = 1, env = env)
    player1 = Min_Max_Agent(player = 1, env = env)

    player2 = Random_Agent(player = 2, env = env)
    #player2 = DQN_Agent(player = 2, train = True, env=env, parametes_path="Data/params_304.pth")
    
    test = Tester(env, player1, player2)
    print(test.test(100))
    