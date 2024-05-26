#region ###### import #######
import pygame
from Constants import *
import time
from Graphics import Graphics as Graphics
from Quixo import Quixo
from Human_Agent import Human_Agent
from Random_Agent import Random_Agent
from Min_Max_Agent import Min_Max_Agent
from Alpha_Beta_Agent import Alpha_Beta_Agent
from DQN_Agent import DQN_Agent
#endregion

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Quixo')
env = Quixo()
graphics = Graphics(win, env)
state = env.state

########################################################
####################-CHOOSE-PLAYERS-####################
########################################################

#player1 = Human_Agent(player = 1, env = env, graphics = graphics)
#player2 = Human_Agent(player = 2, env = env, graphics = graphics)

#player1 = Random_Agent(player = 1, env = env)
player2 = Random_Agent(player = 2, env = env)

#player1 = Min_Max_Agent(player = 1, env = env)
#player2 = Min_Max_Agent(player = 2, env = env)

#player1 = Alpha_Beta_Agent(player = 1, env = env)
#player2 = Alpha_Beta_Agent(player = 2, env = env)

player1 = DQN_Agent(player = 1, env = env, parametes_path="Data/params_305.pth", train = False)
#player2 = DQN_Agent(player = 2, env = env, parametes_path="Data/params_306.pth", train = False)

########################################################
########################################################
########################################################

pygame.init()

def main():

    run = True

    clock = pygame.time.Clock()
    win.fill(BOARD)
    graphics.draw(state = state)
    player = player1

    while(run):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        action = player.get_Action(events = events, state = state, train = False)

        if action:
            env.move(state, action)
            graphics.draw(state = state)
            player = Switch_Players(player)

        winner = env.check_winner(state)
        if winner != -1:
            pygame.display.update()
            graphics.endofgame(winner)
            run = False
        time.sleep(0.5)
        pygame.display.update()
        clock.tick(FPS)

    time.sleep(1)
    pygame.quit()
    print("End of Game")

def Switch_Players(player):
    if player == player1:
        return player2
    else:
        return player1

if __name__ == '__main__':
    main()
