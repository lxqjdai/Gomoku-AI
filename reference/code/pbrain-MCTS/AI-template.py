# @Time    : 28/05/2018 2:37 PM
# @Author  : Shihan Ran
# @File    : AI-template.py
# @Software: PyCharm
# @license : Copyright(C), Fudan University
# @Contact : rshcaroline@gmail.com
# @Desc    : This is a template for Gomoku.


import random
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG

pp.infotext = 'name="AI-template", author="Shihan Ran", version="1.0", country="China"'

MAX_BOARD = 100
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]


def brain_init():
    """
    Initiate the board, the board size must be in set [5, MAX_BOARD].
    """
    if pp.width < 5 or pp.height < 5:
        pp.pipeOut("ERROR size of the board")
        return
    if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
        pp.pipeOut("ERROR Maximal board size is {}".format(MAX_BOARD))
        return
    pp.pipeOut("OK")


def brain_restart():
    """
    Restart the game, set all squares to zero.
    """
    for x in range(pp.width):
        for y in range(pp.height):
            board[x][y] = 0
    pp.pipeOut("OK")


def isFree(x, y):
    """
    Return a bool value indicating if (x, y) square is free.
    """
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0


def brain_my(x, y):
    """
    I take a move.
    """
    if isFree(x,y):
        board[x][y] = 1
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    """
    Opponents take a move.
    """
    if isFree(x,y):
        board[x][y] = 2
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))


def brain_block(x, y):
    """
    I don't know what is block...???
    It seems irrelevant with us. Since it means square [x,y] belongs to a winning line (when info_continuous is 1).
    """
    if isFree(x,y):
        board[x][y] = 3
    else:
        pp.pipeOut("ERROR winning move [{},{}]".format(x, y))


def brain_takeback(x, y):
    """
    Take back a move. You cheat!
    :return 0: success, 1: not supported, 2: error
    """
    if x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] != 0:
        board[x][y] = 0
        return 0
    return 2


def brain_turn():
    """
    Choose your move and call do_mymove(x,y), 0 <= x < width, 0 <= y < height.
    Write your strategies here. Randomly take a move.
    """
    if pp.terminateAI:
        return
    i = 0
    while True:
        x = random.randint(0, pp.width)
        y = random.randint(0, pp.height)
        i += 1
        if pp.terminateAI:
            return
        if isFree(x,y):
            break
    if i > 1:
        pp.pipeOut("DEBUG {} coordinates didn't hit an empty field".format(i))
    pp.do_mymove(x, y)


def brain_end():
    """
    Delete temporary files, free resources
    """
    pass


def brain_about():
    """
    Print copyright.
    """
    pp.pipeOut(pp.infotext)


if DEBUG_EVAL:
    # For debugging.
    import win32gui
    def brain_eval(x, y):
        # TODO check if it works as expected
        wnd = win32gui.GetForegroundWindow()
        dc = win32gui.GetDC(wnd)
        rc = win32gui.GetClientRect(wnd)
        c = str(board[x][y])
        win32gui.ExtTextOut(dc, rc[2]-15, 3, 0, None, c, ())
        win32gui.ReleaseDC(wnd, dc)


# overwrites information about a game
# The board has 20x20 squares
pp.width, pp.height = 20, 20
# 15 seconds per move, 90 seconds per match for maximum
# time for one turn in milliseconds
pp.info_timeout_turn = 15000
# total time for a game
pp.info_timeout_match = 90000
# 0: human opponent, 1: AI opponent, 2: tournament, 3: network tournament
pp.info_game_type = 1
# 0: five or more stones win, 1: exactly five stones win
pp.info_exact5 = 0
# 0: gomoku, 1: renju
pp.info_renju = 0

# overwrites functions in pisqpipe module
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
