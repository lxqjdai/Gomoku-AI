import random
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG
import copy
import numpy as np
pp.infotext = 'name="pbrain-pyrandom", author="Jan Stransky", version="1.0", country="Czech Republic", www="https://github.com/stranskyjan/pbrain-pyrandom"'

MAX_BOARD = 20
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
my_move =[(9, 9), (8, 8)]
opponent_move = [(10, 9), (10, 8), (10, 6)]
move_left = [(i, j) for i in range(MAX_BOARD) for j in range(MAX_BOARD)]
for move in my_move:
    board[move[0]][move[1]]=1
    move_left.remove(move)
for move in opponent_move:
    board[move[0]][move[1]]=2
    move_left.remove(move)

max_sim_time = 20


def Exe_move(board, move, side):
    new_board = [[board[i][j] for j in range(MAX_BOARD)] for i in range(MAX_BOARD)]
    new_board[move[0]][move[1]] = side
    return new_board


def Check_win(new_board, side, move):
    count = 1
    x, y = move
    min_x = max(0, x - 4)
    max_x = min(MAX_BOARD-1, x + 4)
    min_y = max(0, y - 4)
    max_y = min(MAX_BOARD-1, y + 4)
    for i in range(min_x + 1, max_x + 1):
        if new_board[i][y] == side and new_board[i - 1][y] == side:
            count += 1
        else:
            count = 1
        if count >= 5:
            return True
    count = 1
    for i in range(min_y + 1, max_y + 1):
        if new_board[x][i] == side and new_board[x][i - 1] == side:
            count += 1
        else:
            count = 1
        if count >= 5:
            return True
    count = 1
    down = min(x-min_x, y-min_y)
    up = min(max_x-x,max_y-y)
    for m in range(-down, up):
        i = x + m + 1
        j = y + m + 1
        if new_board[i][j] == side and new_board[i - 1][j - 1] == side:
            count += 1
        else:
            count = 1
        if count >= 5:
            return True
    count = 1
    down = min(max_y-y,x-min_x)
    up = min(max_x - x, y - min_y)
    for m in range(-down, up):
        i = x + m + 1
        j = y - m - 1
        if new_board[i][j] == side and new_board[i - 1][j + 1] == side:
            count += 1
        else:
            count = 1
        if count >= 5:
            return True
    return False


def Check_terminal(move_left_sim):
    if not move_left_sim:
        return True
    return False


def Check_4_in_line(new_board, move, side):  # move 表示检查那个点附近 side表示检查哪一边的，num表示检查连续几个
    num = 3
    x, y = move
    min_x = max(0, x - num-1)
    max_x = min(MAX_BOARD - 1, x + num+1)
    min_y = max(0, y - num-1)
    max_y = min(MAX_BOARD - 1, y + num+1)
    force_move_all = []
    count = 1
    force_move = []
    for i in range(min_x + 1, max_x + 1):  # 竖着4个
        if new_board[i][y] == side and new_board[i - 1][y] == side:
            count += 1
        else:
            count = 1
        end_pos = (i, y)  # 记录最后的位置
        if count == 4: # 检查xxxx的情况 
            x1, y1 = end_pos
            if x1 + 1 <= MAX_BOARD - 1 and new_board[x1 + 1][y1] == 0:  # 往后一格看看行不行
                force_move.append((x1 + 1, y1))
            if x1 - num - 1 >= 0 and new_board[x1 - num - 1][y1] == 0:
                force_move.append((x1 - num - 1, y1))
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break
        if count == 3: # 检查 xxx x 或者x xxx的情况 
            x1,y1 = end_pos
            if x1 + 2 <= MAX_BOARD - 1 and new_board[x1 + 1][y1] == 0 and new_board[x1+2][y1] == side:
                force_move.append((x1+1,y1))
            if x1 - num - 1 >= 0 and new_board[x1-num][y1] == 0 and new_board[x1-num-1][y1] == side:
                force_move.append((x1-num,y1))
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break
        if count == 2: # 检查 xx xx 的情况 
            x1,y1 = end_pos
            if x1 + 3 <= MAX_BOARD-1 and new_board[x1+1][y1]==0 and new_board[x1+2][y1]==side and new_board[x1+3][y1]==side:
                force_move.append((x1+1,y1))
            if x1 - 4 >= 0 and new_board[x1-2][y1]==0 and new_board[x1-3][y1]==side and new_board[x1-4][y1]==side:
                force_move.append((x1-2,y1))
            if len(force_move)!=0:
                force_move_all.append(force_move)


    count = 1
    force_move = []
    for i in range(min_y + 1, max_y + 1):  # 横着的4个
        if new_board[x][i] == side and new_board[x][i - 1] == side:
            count += 1
        else:
            count = 1
        end_pos = (x, i)  # 记录最后的位置
        if count == 4: # 检查正常 xxx 情况 num = 2 count = 3
            x1, y1 = end_pos
            if y1 + 1 <= MAX_BOARD - 1 and new_board[x1][y1 + 1] == 0:  # 往后一格看看行不行
                force_move.append((x1, y1 + 1))
            if y1 - num - 1 >= 0 and new_board[x1][y1 - num - 1] == 0: # 往前看一格行不行
                force_move.append((x1, y1 - num - 1))
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break
        if count == 3: # 检查xx x 或者x xx的情况 num = 2 count = 2
            x1,y1 = end_pos
            if y1 + 2 <= MAX_BOARD - 1 and new_board[x1][y1+1] == 0 and new_board[x1][y1+2] == side:
                force_move.append((x1,y1+1))
            if y1 - num - 1 >= 0 and new_board[x1][y1-num] == 0 and new_board[x1][y1-num-1] == side:
                force_move.append((x1,y1-num))
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break
        if count == 2: # 检查 xx xx 的情况 
            x1,y1 = end_pos
            if y1 + 3 <= MAX_BOARD-1 and new_board[x1][y1+1]==0 and new_board[x1][y1+2]==side and new_board[x1][y1+3]==side:
                force_move.append((x1,y1+1))
            if y1 - 4 >= 0 and new_board[x1][y1-2]==0 and new_board[x1][y1-3]==side and new_board[x1][y1-4]==side:
                force_move.append((x1,y1-2))
            if len(force_move)!=0:
                force_move_all.append(force_move)

    count = 1
    force_move = []
    down = min(x-min_x, y-min_y)
    up = min(max_x-x,max_y-y)
    for m in range(-down, up): # 正斜的时候
        i = x + m + 1
        j = y + m + 1
        if new_board[i][j] == side and new_board[i - 1][j - 1] == side:
            count += 1
        else:
            count = 1
        end_pos = (i, j)  # 记录最后的位置
        if count == 4: # 检查xxx的情况 num = 2 count = 3
            x1, y1 = end_pos
            if x1 + 1 <= MAX_BOARD - 1 and y1 + 1 <= MAX_BOARD - 1 and new_board[x1 + 1][y1 + 1] == 0:  # 往后一格看看行不行
                force_move.append((x1 + 1, y1 + 1))
            if x1 - num - 1 >= 0 and y1 - num - 1 >= 0 and new_board[x1 - num - 1][y1 - num - 1] == 0: # 往前看一格行不行
                force_move.append((x1 - num - 1, y1 - num - 1))
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break
        if count == 3:  # 检查xxx x 或者x xxx的情况
            x1,y1 = end_pos
            if x1 + 2 <= MAX_BOARD - 1 and y1 + 2 <= MAX_BOARD - 1 and new_board[x1+1][y1+1] == 0 and new_board[x1+2][y1+2] == side:
                force_move.append((x1+1,y1+1))
            if x1 - num - 1 >= 0  and y1 - num - 1 >= 0 and new_board[x1-num][y1-num] == 0 and new_board[x1-num-1][y1-num-1] == side:
                force_move.append((x1-num,y1-num))
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break
        if count == 2: # 检查 xx xx 的情况 
            x1,y1 = end_pos
            if x1+3<=MAX_BOARD-1 and y1 + 3 <= MAX_BOARD-1 and new_board[x1+1][y1+1]==0 and new_board[x1+2][y1+2]==side and new_board[x1+3][y1+3]==side:
                force_move.append((x1+1,y1+1))
            if x1-4>=0 and y1 - 4 >= 0 and new_board[x1-2][y1-2]==0 and new_board[x1-3][y1-3]==side and new_board[x1-4][y1-4]==side:
                force_move.append((x1-2,y1-2))
            if len(force_move)!=0:
                force_move_all.append(force_move)

    
    count = 1
    force_move = []
    down = min(max_y-y,x-min_x)
    up = min(max_x - x, y - min_y)
    for m in range(-down, up): # 检查侧斜的情况
        i = x + m + 1
        j = y - m - 1
        if new_board[i][j] == side and new_board[i - 1][j + 1] == side:
            count += 1
            end_pos = (i, j) # 记录终点位置
        else:
            count = 1
        if count == num + 1: # 检查xxx的情况 num = 2 count = 3
            x1, y1 = end_pos
            if x1 + 1 <= MAX_BOARD - 1 and y1 - 1 >= 0 and new_board[x1 + 1][y1 - 1] == 0:  # 往后一格看看行不行
                force_move.append((x1 + 1, y1 - 1))
            if x1 - num - 1 >= 0 and y1 + num + 1 <= MAX_BOARD - 1 and new_board[x1 - num - 1][y1 + num + 1] == 0: # 往前看一步行不行
                force_move.append((x1 - num - 1, y1 + num + 1))
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break
        if count == num:  # 检查xxx x 或者x xxx的情况 num = 2 count = 2
            x1,y1 = end_pos
            if x1 + 2 <= MAX_BOARD - 1 and y1 - 2 >= 0 and new_board[x1+1][y1-1] == 0 and new_board[x1+2][y1-2] == side:
                force_move.append((x1+1,y1-1))
            if x1 - num - 1 >= 0  and y1 + num + 1 <= MAX_BOARD-1 and new_board[x1-num][y1+num] == 0 and new_board[x1-num-1][y1+num+1] == side:
                force_move.append((x1-num,y1+num))
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break
        if count == 2: # 检查 xx xx 的情况 
            x1,y1 = end_pos
            if x1+3<=MAX_BOARD-1 and y1 - 3 >= 0  and new_board[x1+1][y1-1]==0 and new_board[x1+2][y1-2]==side and new_board[x1+3][y1-3]==side:
                force_move.append((x1+1,y1-1))
            if x1-4>=0 and y1 + 4 <= MAX_BOARD -1 and new_board[x1-2][y1+2]==0 and new_board[x1-3][y1+3]==side and new_board[x1-4][y1+4]==side:
                force_move.append((x1-2,y1+2))
            if len(force_move)!=0:
                force_move_all.append(force_move)


    longest_force = 0
    best_force = []
    for force_move in force_move_all:
        if len(force_move) > longest_force:
            best_force = force_move
    return best_force

def Check_3_in_line(new_board, move, side):  # move 表示检查那个点附近 side表示检查哪一边的，num表示检查连续几个
    num = 2
    x, y = move
    min_x = max(0, x - num-1)
    max_x = min(MAX_BOARD - 1, x + num+1)
    min_y = max(0, y - num-1)
    max_y = min(MAX_BOARD - 1, y + num+1)
    force_move_all = []
    count = 1
    force_move = []
    for i in range(min_x + 1, max_x + 1):  # 竖着3个
        if new_board[i][y] == side and new_board[i - 1][y] == side:
            count += 1
        else:
            count = 1
        end_pos = (i, y)  # 记录最后的位置
        if count == 3: # 检查xxx的情况
            x1, y1 = end_pos
            if x1 + 1 <= MAX_BOARD - 1 and new_board[x1 + 1][y1] == 0:  # 往后一格看看行不行
                force_move.append((x1 + 1, y1))
            if x1 - num - 1 >= 0 and new_board[x1 - num - 1][y1] == 0:
                force_move.append((x1 - num - 1, y1))
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break
        if count == 2: # 检查 ** * 或者* **的情况 num = 2 count = 2
            x1,y1 = end_pos
            if x1 + 2 <= MAX_BOARD - 1 and new_board[x1 + 1][y1] == 0 and new_board[x1+2][y1] == side:
                force_move.append((x1+1,y1))
                if x1+3 <= MAX_BOARD - 1 and new_board[x1+3][y1]==0:#检查xx xo
                    force_move.append((x1+3,y1))
                if x1-2 >= 0 and new_board[x1-2][y1]==0:#检查oxx x
                    force_move.append((x1-2,y1))
                if len(force_move) == 3:
                    return [(x1+1,y1)]
            if x1 - num - 1 >= 0 and new_board[x1-num][y1] == 0 and new_board[x1-num-1][y1] == side:
                force_move.append((x1-num,y1))
                if x1+1 <= MAX_BOARD-1 and new_board[x1+1][y1]==0:#检查x xxo
                    force_move.append((x1+1,y1))
                if x1-4>=0 and new_board[x1-4][y1]==0:#检查ox xx
                    force_move.append((x1-4,y1))
                if len(force_move) == 3:
                    return [(x1-num,y1)]
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break


    count = 1
    force_move = []
    for i in range(min_y + 1, max_y + 1):  # 横着的num个
        if new_board[x][i] == side and new_board[x][i - 1] == side:
            count += 1
            end_pos = (x, i)  # 记录最后的位置
        else:
            count = 1
        if count == 3: # 检查正常 xxx 情况 num = 2 count = 3
            x1, y1 = end_pos
            if y1 + 1 <= MAX_BOARD - 1 and new_board[x1][y1 + 1] == 0:  # 往后一格看看行不行
                force_move.append((x1, y1 + 1))
            if y1 - num - 1 >= 0 and new_board[x1][y1 - num - 1] == 0: # 往前看一格行不行
                force_move.append((x1, y1 - num - 1))
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break
        if count == 2: # 检查xx x 或者x xx的情况 num = 2 count = 2
            x1,y1 = end_pos
            if y1 + 2 <= MAX_BOARD - 1 and new_board[x1][y1+1] == 0 and new_board[x1][y1+2] == side:
                force_move.append((x1,y1+1))
                if y1+3 <= MAX_BOARD - 1 and new_board[x1][y1+3]==0:#检查xx xo
                    force_move.append((x1,y1+3))
                if y1-2 >= 0 and new_board[x1][y1-2]==0:#检查oxx x
                    force_move.append((x1,y1-2))
                if len(force_move) == 3:
                    return [(x1,y1+1)]
            if y1 - num - 1 >= 0 and new_board[x1][y1-num] == 0 and new_board[x1][y1-num-1] == side:
                force_move.append((x1,y1-num))
                if y1+1 <= MAX_BOARD-1 and new_board[x1][y1+1]==0:#检查x xxo
                    force_move.append((x1,y1+1))
                if y1-4>=0 and new_board[x1][y1-4]==0:#检查ox xx
                    force_move.append((x1,y1-4))
                if len(force_move) == 3:
                    return [(x1,y1-num)]
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break

    count = 1
    force_move = []
    down = min(x-min_x, y-min_y)
    up = min(max_x-x,max_y-y)
    for m in range(-down, up): # 正斜的时候
        i = x + m + 1
        j = y + m + 1
        if new_board[i][j] == side and new_board[i - 1][j - 1] == side:
            count += 1
            end_pos = (i, j)  # 记录最后的位置
        else:
            count = 1
        if count == num + 1: # 检查xxx的情况 num = 2 count = 3
            x1, y1 = end_pos
            if x1 + 1 <= MAX_BOARD - 1 and y1 + 1 <= MAX_BOARD - 1 and new_board[x1 + 1][y1 + 1] == 0:  # 往后一格看看行不行
                force_move.append((x1 + 1, y1 + 1))
            if x1 - num - 1 >= 0 and y1 - num - 1 >= 0 and new_board[x1 - num - 1][y1 - num - 1] == 0: # 往前看一格行不行
                force_move.append((x1 - num - 1, y1 - num - 1))
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break
        if count == num:  # 检查xx x 或者x xx的情况 num = 2 count = 3
            x1,y1 = end_pos
            if x1 + 2 <= MAX_BOARD - 1 and y1 + 2 <= MAX_BOARD - 1 and new_board[x1+1][y1+1] == 0 and new_board[x1+2][y1+2] == side:
                force_move.append((x1+1,y1+1))
                if x1+3<=MAX_BOARD-1 and y1+3 <= MAX_BOARD - 1 and new_board[x1+3][y1+3]==0:#检查xx xo
                    force_move.append((x1+3,y1+3))
                if x1-2>=0 and y1-2 >= 0 and new_board[x1-2][y1-2]==0:#检查oxx x
                    force_move.append((x1-2,y1-2))
                if len(force_move) == 3:
                    return [(x1+1,y1+1)]
            if x1 - num - 1 >= 0  and y1 - num - 1 >= 0 and new_board[x1-num][y1-num] == 0 and new_board[x1-num-1][y1-num-1] == side:
                force_move.append((x1-num,y1-num))
                if x1+1 <= MAX_BOARD-1 and y1+1 <= MAX_BOARD-1 and new_board[x1+1][y1+1]==0:#检查x xxo
                    force_move.append((x1+1,y1+1))
                if x1-4>=0 and y1-4>=0 and new_board[x1-4][y1-4]==0:#检查ox xx
                    force_move.append((x1-4,y1-4))
                if len(force_move) == 3:
                    return [(x1-num,y1-num)]
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break

    count = 1
    force_move = []
    down = min(max_y-y,x-min_x)
    up = min(max_x - x, y - min_y)
    for m in range(-down, up): # 检查侧斜的情况
        i = x + m + 1
        j = y - m - 1
        if new_board[i][j] == side and new_board[i - 1][j + 1] == side:
            count += 1
            end_pos = (i, j) # 记录终点位置
        else:
            count = 1
        if count == num + 1: # 检查xxx的情况 num = 2 count = 3
            x1, y1 = end_pos
            if x1 + 1 <= MAX_BOARD - 1 and y1 - 1 >= 0 and new_board[x1 + 1][y1 - 1] == 0:  # 往后一格看看行不行
                force_move.append((x1 + 1, y1 - 1))
            if x1 - num - 1 >= 0 and y1 + num + 1 <= MAX_BOARD - 1 and new_board[x1 - num - 1][y1 + num + 1] == 0: # 往前看一步行不行
                force_move.append((x1 - num - 1, y1 + num + 1))
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break
        if count == num:  # 检查xx x 或者x xx的情况 num = 2 count = 2
            x1,y1 = end_pos
            if x1 + 2 <= MAX_BOARD - 1 and y1 - 2 >= 0 and new_board[x1+1][y1-1] == 0 and new_board[x1+2][y1-2] == side:
                force_move.append((x1+1,y1-1))
                if x1+3<=MAX_BOARD-1 and y1-3 >= 0 and new_board[x1+3][y1-3]==0:#检查xx xo
                    force_move.append((x1+3,y1-3))
                if x1-2>=0 and y1+2 <= MAX_BOARD-1 and new_board[x1-2][y1+2]==0:#检查oxx x
                    force_move.append((x1-2,y1+2))
                if len(force_move)==3:
                    return [(x1+1,y1-1)]
            if x1 - num - 1 >= 0  and y1 + num + 1 <= MAX_BOARD-1 and new_board[x1-num][y1+num] == 0 and new_board[x1-num-1][y1+num+1] == side:
                force_move.append((x1-num,y1+num))
                if x1+1<=MAX_BOARD-1 and y1-1 >= 0 and new_board[x1+1][y1-1]==0:#检查xx xo
                    force_move.append((x1+1,y1-1))
                if x1-4>=0 and y1+4 <= MAX_BOARD-1 and new_board[x1-4][y1+4]==0:#检查oxx x
                    force_move.append((x1-4,y1+4))
                if len(force_move)==3:
                    return [(x1-num,y1+num)]
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break

    longest_force = 0
    best_force = []
    for force_move in force_move_all:
        if len(force_move) > longest_force:
            best_force = force_move
    return best_force

def Check_2_in_line(new_board, move, side):  # move 表示检查那个点附近 side表示检查哪一边的，num表示检查连续几个
    x,y = move
    force_move = []
    if x-2>=0 and new_board[x-2][y]==side and new_board[x-1][y]==0:
        force_move.append((x-1,y))
        if x-3>=0 and new_board[x-3][y]==0:
            force_move.append((x-3,y))
        if x+1<=MAX_BOARD-1 and new_board[x+1][y]==0:
            force_move.append((x+1,y))
    if x+2<=MAX_BOARD-1 and new_board[x+2][y]==side and new_board[x+1][y]==0:
        force_move.append((x+1,y))
        if x+3 <= MAX_BOARD-1 and new_board[x+3][y]==0:
            force_move.append((x+3,y))
        if x-1>=0 and new_board[x-1][y]==0:
            force_move.append((x-1,y))

    if y-2>=0 and new_board[x][y-2]==side and new_board[x][y-1]==0:
        force_move.append((x,y-1))
        if y-3>=0 and new_board[x][y-3]==0:
            force_move.append((x,y-3))
        if y+1<=MAX_BOARD-1 and new_board[x][y+1]==0:
            force_move.append((x,y+1))
    if y+2<=MAX_BOARD-1 and new_board[x][y+2]==side and new_board[x][y+1]==0:
        force_move.append((x,y+1))
        if y+3 <= MAX_BOARD-1 and new_board[x][y+3]==0:
            force_move.append((x,y+3))
        if y-1>=0 and new_board[x][y-1]==0:
            force_move.append((x,y-1))

    if x-2>=0 and y-2>=0 and new_board[x-2][y-2]==side and new_board[x-1][y-1]==0:
        force_move.append((x-1,y-1))
        if x-3>=0 and y-3>=0 and new_board[x-3][y-3]==0:
            force_move.append((x-3,y-3))
        if x+1<=MAX_BOARD-1 and y+1<=MAX_BOARD-1 and new_board[x+1][y+1]==0:
            force_move.append((x+1,y+1))
    if x+2<=MAX_BOARD-1 and y+2<=MAX_BOARD-1 and new_board[x+2][y+2]==side and new_board[x+1][y+1]==0:
        force_move.append((x+1,y+1))
        if x+3 <= MAX_BOARD-1 and y+3<=MAX_BOARD-1 and new_board[x+3][y+3]==0:
            force_move.append((x+3,y+3))
        if x-1>=0 and y-1>=0 and new_board[x-1][y-1]==0:
            force_move.append((x-1,y-1))

    if x-2>=0 and y+2<=MAX_BOARD-1 and new_board[x-2][y+2]==side and new_board[x-1][y+1]==0:
        force_move.append((x-1,y+1))
        if x-3>=0 and y+3<=MAX_BOARD-1 and new_board[x-3][y+3]==0:
            force_move.append((x-3,y+3))
        if x+1<=MAX_BOARD-1 and y-1>=0 and new_board[x+1][y-1]==0:
            force_move.append((x+1,y-1))
    if x+2<=MAX_BOARD-1 and y-2>=0 and new_board[x+2][y-2]==side and new_board[x+1][y-1]==0:
        force_move.append((x+1,y-1))
        if x+3 <= MAX_BOARD-1 and y-3>=0 and new_board[x+3][y-3]==0:
            force_move.append((x+3,y-3))
        if x-1>=0 and y+1<=MAX_BOARD-1 and new_board[x-1][y+1]==0:
            force_move.append((x-1,y+1))
    
    return force_move


class MTCS():
    def __init__(self, board, move_left, my_move, opponent_move):
        self.board = board
        self.move_left = move_left
        self.my_move = my_move
        self.opponent_move = opponent_move
        if opponent_move:
            self.sim_move_b1 = opponent_move[-1]  # 前一步，也就是对手下的
        else:
            self.sim_move_b1 = None
        if my_move:
            self.sim_move_b2 = my_move[-1]  # 前两步，也就是自己下的
        else:
            self.sim_move_b2 = None

    def Heuristic_knowledge(self, new_board, turn):
        if self.sim_move_b1 is None or self.sim_move_b2 is None:
            return False
        # four in a row in my side
        force_move = Check_4_in_line(new_board, self.sim_move_b2, turn)
        if force_move:
            return force_move
        # four in a row in opponent side
        force_move = Check_4_in_line(new_board, self.sim_move_b1, 3 - turn)
        if force_move:
            return force_move
        # three in a row in my side
        force_move = Check_3_in_line(new_board, self.sim_move_b2, turn)
        if force_move:
            return force_move
        # three in a row in opponent side
        force_move = Check_3_in_line(new_board, self.sim_move_b1, 3 - turn)
        if force_move:
            return force_move
        # two in a row in my side
        force_move = Check_2_in_line(new_board,self.sim_move_b2,turn)
        if force_move:
            return force_move
        # two in a row in opponent side
        force_move = Check_2_in_line(new_board,self.sim_move_b1,3-turn)
        if force_move:
            return force_move
        return False

    def Simulation(self, new_board, move_left_sim, turn):
        if self.sim_move_b1 is not None and self.sim_move_b2 is not None:  # 保证前面有走了2步以上
            if turn == 1: # 得到各方上一次的move
                my_move_b, opponent_move_b = self.sim_move_b2, self.sim_move_b1
            else:
                my_move_b, opponent_move_b = self.sim_move_b1, self.sim_move_b2
            if Check_win(new_board, 1, my_move_b): # 判断是否终止
                return 1.0
            elif Check_win(new_board, 2, opponent_move_b):
                return -1.0
            elif Check_terminal(move_left_sim):
                return 0.0
        force_move = self.Heuristic_knowledge(new_board, turn)
        if force_move:
            move = random.choice(force_move)
        else:
            move = random.choice(move_left_sim)
        move_left_sim.remove(move)
        new_board = Exe_move(new_board, move, turn)
        self.sim_move_b2 = self.sim_move_b1
        self.sim_move_b1 = move
        return self.Simulation(new_board, move_left_sim, 3 - turn)

    def constrain_move(self):
        if not self.my_move:
            if self.opponent_move:
                my_move = self.opponent_move
                opponent_move = self.opponent_move
            else:
                return [(MAX_BOARD//2,MAX_BOARD//2)]
        else:
            my_move = self.my_move
            opponent_move = self.opponent_move
        min_x_m,_ = min(my_move,key=lambda x:x[0])
        max_x_m,_ = max(my_move,key=lambda x:x[0])
        _,min_y_m = min(my_move,key=lambda x:x[1])
        _,max_y_m = max(my_move,key=lambda x:x[1])
        min_x_o,_ = min(opponent_move, key=lambda x: x[0])
        max_x_o,_ = max(opponent_move, key=lambda x: x[0])
        _,min_y_o = min(opponent_move, key=lambda x: x[1])
        _,max_y_o = max(opponent_move, key=lambda x: x[1])
        min_x = max(min(min_x_m,min_x_o)-1,0)
        max_x = min(max(max_x_m,max_x_o)+1,MAX_BOARD-1)
        min_y = max(min(min_y_m,min_y_o)-1,0)
        max_y = min(max(max_y_m,max_y_o)+1,MAX_BOARD-1)
        cons_move = []
        for i in range(min_x,max_x+1):
            for j in range(min_y,max_y+1):
                if (i,j) in self.my_move or (i,j) in self.opponent_move:
                    continue
                cons_move.append((i,j))
        return cons_move

    def main(self):
        history = []
        sim_move_b1 = self.sim_move_b1  # 先保存下来，等下会反复使用
        cons_move = self.constrain_move()
        for move in cons_move:
            move_lef_sim = copy.deepcopy(self.move_left)
            move_lef_sim.remove(move)
            new_board = Exe_move(self.board, move, 1)
            r_total = 0
            sim_time = 0
            while sim_time < max_sim_time:
                self.sim_move_b2 = sim_move_b1
                self.sim_move_b1 = move
                move_lef_sim1 = copy.deepcopy(move_lef_sim)
                r_now = self.Simulation(new_board, move_lef_sim1, 2)
                r_total += r_now
                sim_time += 1
            history.append((move, r_total))
        max_move, _ = max(history, key=lambda x: x[1])
        #print(sorted(history,key=lambda x:-x[1]))
        return max_move


mcts = MTCS(board, move_left,my_move,opponent_move)
(x, y) = mcts.main()
print(x,y)
#pp.do_mymove(x, y)

