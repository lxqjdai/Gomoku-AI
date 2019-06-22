import random
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG
import copy

pp.infotext = 'name="pbrain-pyrandom", author="Jan Stransky", version="1.0", country="Czech Republic", www="https://github.com/stranskyjan/pbrain-pyrandom"'

MAX_BOARD = 20
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
max_sim_time = 40
move_left = []
my_move = []
opponent_move = []
for i in range(MAX_BOARD):
    for j in range(MAX_BOARD):
        move_left.append((i, j))

def updata_board_info(board):
    move_left = []
    my_move = []
    opponent_move = []
    for i in range(MAX_BOARD):
        for j in range(MAX_BOARD):
            if board[i][j] == 0:
                move_left.append((i, j))
            elif board[i][j] == 1:
                my_move.append((i, j))
            elif board[i][j] == 2:
                opponent_move.append((i, j))
    return move_left, my_move, opponent_move

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


def Check_x_in_line(new_board, move, side, num):  # move 表示检查那个点附近 side表示检查哪一边的，num表示检查连续几个
    num = num - 1
    x, y = move
    min_x = max(0, x - num-1)
    max_x = min(MAX_BOARD - 1, x + num+1)
    min_y = max(0, y - num-1)
    max_y = min(MAX_BOARD - 1, y + num+1)
    force_move_all = []
    count = 1
    force_move = []
    for i in range(min_x + 1, max_x + 1):  # 竖着num个
        if new_board[i][y] == side and new_board[i - 1][y] == side:
            count += 1
            end_pos = (i, y)  # 记录最后的位置
        else:
            count = 1
        if count == num + 1: # 检查xxx的情况 num = 2 count = 3
            x1, y1 = end_pos
            if x1 + 1 <= MAX_BOARD - 1 and new_board[x1 + 1][y1] == 0:  # 往后一格看看行不行
                force_move.append((x1 + 1, y1))
            if x1 - num - 1 >= 0 and new_board[x1 - num - 1][y1] == 0:
                force_move.append((x1 - num - 1, y1))
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break
        if count == num: # 检查 ** * 或者* **的情况 num = 2 count = 2
            x1,y1 = end_pos
            if x1 + 2 <= MAX_BOARD - 1 and new_board[x1 + 1][y1] == 0 and new_board[x1+2][y1] == side:
                force_move.append((x1+1,y1))
            if x1 - num - 1 >= 0 and new_board[x1-num][y1] == 0 and new_board[x1-num-1][y1] == side:
                force_move.append((x1-num,y1))
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
        if count == num + 1: # 检查正常 xxx 情况 num = 2 count = 3
            x1, y1 = end_pos
            if y1 + 1 <= MAX_BOARD - 1 and new_board[x1][y1 + 1] == 0:  # 往后一格看看行不行
                force_move.append((x1, y1 + 1))
            if y1 - num - 1 >= 0 and new_board[x1][y1 - num - 1] == 0: # 往前看一格行不行
                force_move.append((x1, y1 - num - 1))
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break
        if count == num: # 检查xx x 或者x xx的情况 num = 2 count = 2
            x1,y1 = end_pos
            if y1 + 2 <= MAX_BOARD - 1 and new_board[x1][y1+1] == 0 and new_board[x1][y1+2] == side:
                force_move.append((x1,y1+1))
            if y1 - num - 1 >= 0 and new_board[x1][y1-num] == 0 and new_board[x1][y1-num-1] == side:
                force_move.append((x1,y1-num))
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
            if x1 - num - 1 >= 0  and y1 - num - 1 >= 0 and new_board[x1-num][y1-num] == 0 and new_board[x1-num-1][y1-num-1] == side:
                force_move.append((x1-num,y1-num))
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
            if x1 - num - 1 >= 0  and y1 + num + 1 <= MAX_BOARD-1 and new_board[x1-num][y1+num] == 0 and new_board[x1-num-1][y1+num+1] == side:
                force_move.append((x1-num,y1+num))
            if len(force_move) != 0:
                force_move_all.append(force_move)
                break
    longest_force = 0
    best_force = []
    for force_move in force_move_all:
        if len(force_move) > longest_force:
            best_force = force_move
    return best_force


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
        force_move = Check_x_in_line(new_board, self.sim_move_b2, turn, 4)
        if force_move:
            return force_move
        # four in a row in opponent side
        force_move = Check_x_in_line(new_board, self.sim_move_b1, 3 - turn, 4)
        if force_move:
            return force_move
        # three in a row in my side
        force_move = Check_x_in_line(new_board, self.sim_move_b2, turn, 3)
        if force_move:
            return force_move
        # three in a row in opponent side
        force_move = Check_x_in_line(new_board, self.sim_move_b1, 3 - turn, 3)
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


def brain_init():
    if pp.width < 5 or pp.height < 5:
        pp.pipeOut("ERROR size of the board")
        return
    if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
        pp.pipeOut("ERROR Maximal board size is {}".format(MAX_BOARD))
        return
    pp.pipeOut("OK")




def brain_restart():
    for x in range(pp.width):
        for y in range(pp.height):
            board[x][y] = 0
    global move_left
    global my_move
    global opponent_move
    move_left, my_move, opponent_move = updata_board_info(board)
    #logDebug('restart')
    #logDebug('mymove',str(my_move))
    #logDebug('opponent',str(opponent_move))
    pp.pipeOut("OK")


def isFree(x, y):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0


def brain_my(x, y):
    if isFree(x, y):
        board[x][y] = 1
        my_move.append((x, y))
        move_left.remove((x, y))
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    if isFree(x, y):
        board[x][y] = 2
        opponent_move.append((x, y))
        move_left.remove((x, y))
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))


def brain_block(x, y):
    if isFree(x, y):
        board[x][y] = 3
    else:
        pp.pipeOut("ERROR winning move [{},{}]".format(x, y))


def brain_takeback(x, y):
    if x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] != 0:
        board[x][y] = 0
        return 0
    return 2


def brain_turn():
    if pp.terminateAI:
        return
    #move_left, my_move, opponent_move = updata_board_info(board)
    mcts = MTCS(board, move_left, my_move, opponent_move)
    (x, y) = mcts.main()
    pp.do_mymove(x, y)
    #logDebug(str((x,y)))
    #with open('D:/学习资料/大三下/人工智能/final pj/code/log.txt', "a") as f:
    #    f.write('my move' + str(my_move) + "\n")
    #    f.write('opponent move' + str(opponent_move) + '\n')
    #    f.flush()
    """
    i = 0
    while True:
        x = random.randint(0, pp.width)
        y = random.randint(0, pp.height)
        i += 1
        if pp.terminateAI:
            return
        if isFree(x, y):
            break
    if i > 1:
        pp.pipeOut("DEBUG {} coordinates didn't hit an empty field".format(i))
    """


def brain_end():
    pass


def brain_about():
    pp.pipeOut(pp.infotext)


if DEBUG_EVAL:
    import win32gui


    def brain_eval(x, y):
        # TODO check if it works as expected
        wnd = win32gui.GetForegroundWindow()
        dc = win32gui.GetDC(wnd)
        rc = win32gui.GetClientRect(wnd)
        c = str(board[x][y])
        win32gui.ExtTextOut(dc, rc[2] - 15, 3, 0, None, c, ())
        win32gui.ReleaseDC(wnd, dc)

######################################################################
# A possible way how to debug brains.
# To test it, just "uncomment" it (delete enclosing """)
######################################################################
"""
# define a file for logging ...
DEBUG_LOGFILE = "D:/学习资料/大三下/人工智能/final pj/code/tmp/pbrain-pyrandom.log"
# ...and clear it initially
with open(DEBUG_LOGFILE,"w") as f:
    pass

# define a function for writing messages to the file
def logDebug(msg):
    with open(DEBUG_LOGFILE,"a") as f:
        f.write(msg+"\n")
        f.flush()

# define a function to get exception traceback
def logTraceBack():
    import traceback
    with open(DEBUG_LOGFILE,"a") as f:
        traceback.print_exc(file=f)
        f.flush()
    raise Exception()

# use logDebug wherever
# use try-except (with logTraceBack in except branch) to get exception info
# an example of problematic function
def brain_turn():
    logDebug("some message 1")
    try:
        logDebug("some message 2")
        1. / 0. # some code raising an exception
        logDebug("some message 3") # not logged, as it is after error
    except:
        logTraceBack()

######################################################################
"""
# "overwrites" functions in pisqpipe module
pp.brain_init = brain_init
pp.brain_restart = brain_restart
pp.brain_my = brain_my
pp.brain_opponents = brain_opponents
pp.brain_block = brain_block
pp.brain_takeback = brain_takeback
pp.brain_turn = brain_turn
pp.brain_end = brain_end
pp.brain_about = brain_about
if DEBUG_EVAL:
    pp.brain_eval = brain_eval


def main():
    pp.main()

if __name__ == "__main__":
    main()
