#region ###### import #######
from Quixo import Quixo
from State import State
import wandb
from DQN_Agent import DQN_Agent
from Replay_Buffer import Replay_Buffer
from Random_Agent import Random_Agent
from Fix_Agent import Fix_Agent
import torch
from Tester import Tester
#endregion

#region ##### params and paths #####
epochs = 2000000
start_epoch = 0
C = 100
learning_rate = 0.0001
batch_size = 64
env = Quixo()
MIN_Buffer = 4000

### X ###
File_Num1 = 305
path_load1 = None
path_Save1 = f'Data/params_{File_Num1}.pth'
path_best1 = f'Data/best_params_{File_Num1}.pth'

buffer_path1 = f'Data/buffer_{File_Num1}.pth'
results_path1 = f'Data/results_{File_Num1}.pth'
random_results_path1 = f'Data/random_results_{File_Num1}.pth'
path_best_random1 = f'Data/best_random_params_{File_Num1}.pth'

### O ###
File_Num2 = 306
path_load2 = None
path_Save2 = f'Data/params_{File_Num2}.pth'
path_best2 = f'Data/best_params_{File_Num2}.pth'

buffer_path2 = f'Data/buffer_{File_Num2}.pth'
results_path2 = f'Data/results_{File_Num2}.pth'
random_results_path2 = f'Data/random_results_{File_Num2}.pth'
path_best_random2 = f'Data/best_random_params_{File_Num2}.pth'

#endregion

#region ###### wandb init #####
wandb.init(

    project = "Quixo",
    resume = False,
    id = f"Quixo {File_Num1}, {File_Num2}",
    config = {
        "name": f"Quixo {File_Num1}, {File_Num2}",
        "learning_rate:": learning_rate,
        "epochs": epochs,
        "start_epoch": start_epoch,
        "decay": 400,
        "gamma": 0.99,
        "batch_size": batch_size,
        "C": C
    }
)
#endregion

def main ():
    
    #region ###### init objects and variables ######
    player1 = DQN_Agent(player = 1, env = env,parametes_path = None)
    player1_hat = DQN_Agent(player = 1, env = env, train = False)
    Q1 = player1.DQN
    Q1_hat = Q1.copy()
    player1_hat.DQN = Q1_hat
    
    player2 = DQN_Agent(player = 2, env = env,parametes_path = None)
    player2_hat = DQN_Agent(player = 2, env = env, train = False)
    Q2 = player2.DQN
    Q2_hat = Q2.copy()
    player2_hat.DQN = Q2_hat

    buffer1 = Replay_Buffer(path = None)
    buffer2 = Replay_Buffer(path = None)
    
    results_file = [] #torch.load(results_path)
    results1, results2 = [], [] #results_file['results'] # []
    avgLosses1, avgLosses2 = [], [] #results_file['avglosses']     #[]
    avgLoss1, avgLoss2 = 0, 0 #avgLosses[-1] #0
    loss = 0
    res = 0
    best_res = -200
    loss_count1, loss_count2 = 0, 0

    tester1 = Tester(player1 = player1, player2 = Random_Agent(player = 2, env = env), env = env)
    tester2 = Tester(player1 = Random_Agent(player = 1, env = env), player2 = player2, env = env)

    random_results1, random_results2 = [], [] #torch.load(random_results_path)   # []
    best_random1, best_random2 = 0, 0 #max(random_results)
    
    
    # init optimizer
    optim1 = torch.optim.Adam(Q1.parameters(), lr = learning_rate)
    scheduler1 = torch.optim.lr_scheduler.StepLR(optim1, 100000*30, gamma = 0.90)

    optim2 = torch.optim.Adam(Q2.parameters(), lr = learning_rate)
    scheduler2 = torch.optim.lr_scheduler.StepLR(optim2, 100000*30, gamma = 0.90)
    #endregion

    for epoch in range(start_epoch, epochs):
        state_1 = State()
        end_of_game_2 = False
        step = 0
        while not end_of_game_2:
            step +=1
            #region ###### Sample Environement #####
            action_1 = player1.get_Action(state=state_1, epoch=epoch)
            after_state_1 = env.get_next_state(state=state_1, action=action_1)
            reward_1, end_of_game_1 = env.reward(after_state_1)
            if step > 1:            
                buffer2.push(state_2, action_2, -1 * reward_1, after_state_1, end_of_game_1)
            if end_of_game_1:
                res += reward_1
                buffer1.push(state_1, action_1, reward_1, after_state_1, True)
                break
            state_2 = after_state_1
            action_2 = player2.get_Action(state=state_2, epoch=epoch)
            after_state_2 = env.get_next_state(state=state_2, action=action_2)
            reward_2, end_of_game_2 = env.reward(state=after_state_2)
            if end_of_game_2:
                res += reward_2
                buffer2.push(state_2, action_2, -1 * reward_2, after_state_2, True)
            buffer1.push(state_1, action_1, reward_2, after_state_2, end_of_game_2)
            state_1 = after_state_2

            if len(buffer1) < MIN_Buffer:
                continue
            #endregion

            #region  ###### Train X NN #####
            states, actions, rewards, next_states, dones = buffer1.sample(batch_size)
            Q_values = Q1(states, actions)
            next_actions = player1.get_Actions(next_states, dones) # DDQN; DQN player1_het.get_Actions(next_states, dones)
            with torch.no_grad():
                Q_hat_Values = Q1_hat(next_states, next_actions) 

            loss = Q1.loss(Q_values, rewards, Q_hat_Values, dones)
            loss.backward()
            optim1.step()
            optim1.zero_grad()
            scheduler1.step()
            
            if loss_count1 <= 1000:
                avgLoss1 = (avgLoss1 * loss_count1 + loss.item()) / (loss_count1 + 1)
                loss_count1 += 1
            else:
                avgLoss1 += (loss.item()-avgLoss1)* 0.0001 
            #endregion

            #region  ###### Train O NN #####
            states, actions, rewards, next_states, dones = buffer2.sample(batch_size)
            Q_values = Q2(states, actions)
            next_actions = player2.get_Actions(next_states, dones) # DDQN
            with torch.no_grad():
                Q_hat_Values = Q2_hat(next_states, next_actions) 

            loss = Q2.loss(Q_values, rewards, Q_hat_Values, dones)
            loss.backward()
            optim2.step()
            optim2.zero_grad()
            scheduler2.step()

            if loss_count2 <= 1000:
                avgLoss2 = (avgLoss2 * loss_count2 + loss.item()) / (loss_count2 + 1)
                loss_count2 += 1
            else:
                avgLoss2 += (loss.item()-avgLoss2)* 0.0001 
            #endregion

        if epoch % C == 0:
                Q1_hat.load_state_dict(Q1.state_dict())
                Q2_hat.load_state_dict(Q2.state_dict())

        #region ##### prints and save #######
        if (epoch+1) % 100 == 0:
            print(f'\nres= {res}')
            avgLosses1.append(avgLoss1)
            results1.append(res)

            avgLosses2.append(avgLoss2)
            results2.append(res)

            wandb.log({
                "loss1": avgLoss1,
                "loss2": avgLoss2,
                "result": res
            })

            if best_res < res:
                best_res = res
            res = 0

        if (epoch+1) % 1000 == 0:
            test1 = tester1(100)
            test_score1 = test1[0]-test1[1]
            if best_random1 < test_score1:
                best_random1 = test_score1
                player1.save_param(path_best_random1)
            random_results1.append(test_score1)
            
            test2 = tester2(100)
            test_score2 = test2[1]-test2[0]
            if best_random2 < test_score2:
                best_random2 = test_score2
                player2.save_param(path_best_random2)
            random_results2.append(test_score2)
            print(test1, test2)
            

        if (epoch+1) % 1000 == 0:
            torch.save({'epoch': epoch, 'results': results1, 'avglosses':avgLosses1}, results_path1)
            torch.save(buffer1, buffer_path1)
            player1.save_param(path_Save1)
            torch.save(random_results1, random_results_path1)

            torch.save({'epoch': epoch, 'results': results2, 'avglosses':avgLosses2}, results_path2)
            torch.save(buffer2, buffer_path2)
            player2.save_param(path_Save2)
            torch.save(random_results2, random_results_path2)
        
        print (f'epoch={epoch} step={step} loss1={loss:.5f} avgloss1={avgLoss1:.5f}', end=" ")
        print (f'learning rate1={scheduler1.get_last_lr()[0]} path1={path_Save1} res= {res} best_res = {best_res}')

        print (f'epoch={epoch} step={step} loss2={loss:.5f} avgloss2={avgLoss2:.5f}', end=" ")
        print (f'learning rate2={scheduler2.get_last_lr()[0]} path2={path_Save2} res= {res} best_res = {best_res}')
        #endregion

    torch.save({'epoch': epoch, 'results': results1, 'avglosses':avgLosses1}, results_path1)
    torch.save(buffer1, buffer_path1)
    torch.save(random_results1, random_results_path1)

    torch.save({'epoch': epoch, 'results': results2, 'avglosses':avgLosses2}, results_path2)
    torch.save(buffer2, buffer_path2)
    torch.save(random_results2, random_results_path2)

if __name__ == '__main__':
    main()





    