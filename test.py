import numpy as np
from State import State



board = np.array([
            [3,3,3,3,3,3,3],
            [3,1,0,0,1,0,3],
            [3,1,0,1,0,1,3],
            [3,0,0,0,2,2,3],
            [3,0,0,2,2,0,3],
            [3,0,1,2,0,0,3],
            [3,3,3,3,3,3,3]])


state = State(board)
state_tensor = state.toTensor()
print(state_tensor)

print(State.tensorToState(state_tensor).board)


# board = board[1:6, 1:6]
# count_rows_1 = (board == 1).sum(axis = 1) 
# count_cols_1 = (board == 1).sum(axis = 0) 

# print(count_rows_1, count_cols_1)

# count_rows_2 = (board == 2).sum(axis = 1) 
# count_cols_2 = (board == 2).sum(axis = 0) 
# print(count_rows_2, count_cols_2)
# print((count_rows_2==0).astype(int))
# print(count_rows_1*(count_rows_2==0))
# res = count_rows_1*(count_rows_2==0)
# res[res==1]=0
# print(res)

# value = res.sum()*2
# print(value)


