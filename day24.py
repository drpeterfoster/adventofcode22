# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle
from queue import PriorityQueue

puz = Puzzle(year=2022, day=24)
print(puz.url)

# puz.input_data
# %%
TEST_DATA_A = "#.######\n#>>.<^<#\n#.<..<<#\n#>v.><>#\n#<^v^^>#\n######.#"
TEST_RESULT_A = 18
TEST_DATA_B = None
TEST_RESULT_B = 54


BOARDSTATES = {}


def format_data(data):
    vals = np.array([list(line) for line in data.split("\n")])
    # z : (right, left, down, up)
    mat = np.concatenate(
        [
            (vals == ">").astype(int)[:, :, np.newaxis],
            (vals == "<").astype(int)[:, :, np.newaxis],
            (vals == "v").astype(int)[:, :, np.newaxis],
            (vals == "^").astype(int)[:, :, np.newaxis],
        ],
        axis=2,
    )
    board = np.ones(mat.shape)
    board[0, 1, :] = [0] * 4  # add start
    board[-1, -2, :] = [0] * 4  # add end
    board[1:-1, 1:-1, :] = mat[1:-1, 1:-1, :]
    BOARDSTATES[0] = board.copy()
    return board


def print_board(turn, pos):
    flat = BOARDSTATES[turn].sum(axis=2).astype(str)
    flat[pos[0], pos[1]] = "X"
    string = "\n".join(["".join(line) for line in flat]).replace("0", " ")
    print(string)


def roll_board(turn):
    if turn in BOARDSTATES:
        return BOARDSTATES[turn]
    else:
        board = BOARDSTATES[turn - 1].copy()
        board[1:-1, 1:-1, 0] = np.roll(board[1:-1, 1:-1, 0], 1, axis=1)
        board[1:-1, 1:-1, 1] = np.roll(board[1:-1, 1:-1, 1], -1, axis=1)
        board[1:-1, 1:-1, 2] = np.roll(board[1:-1, 1:-1, 2], 1, axis=0)
        board[1:-1, 1:-1, 3] = np.roll(board[1:-1, 1:-1, 3], -1, axis=0)
        BOARDSTATES[turn] = board
        return board


def dist(a, b):
    return int(np.abs(a - b).sum())


def move_maker(pos, turn):
    turn += 1
    flat = roll_board(turn).sum(axis=2)
    newpos = []
    for mod in np.array([[0, -1], [-1, 0], [0, 0], [1, 0], [0, 1]]):
        try:
            opt = pos + mod
            if not np.all(opt >= 0):
                raise IndexError
            if flat[opt[0], opt[1]] == 0:
                newpos.append(opt)
        except IndexError:
            continue
    newstates = [
        (pos.copy() if isinstance(pos, np.ndarray) else pos, turn) for pos in newpos
    ]
    return newstates


def _solver(start, end, start_turn=0):
    visted = set()
    besttime = np.inf
    counter = 0
    stack = PriorityQueue()
    # distance, counter, position, turn
    stack.put((dist(start, end), counter, start, start_turn))
    while not stack.empty():
        dis, _, pos, turn = stack.get()
        if tuple([*pos, turn]) in visted:  # been there at that time? skip it.
            stack.task_done()
            continue
        visted.update([tuple([*pos, turn])])
        if (turn + dis) >= besttime:  # too far away to get besttime? skip it.
            stack.task_done()
            continue
        if np.all(pos == end) and turn < besttime:  # you the best time? record it.
            besttime = turn
            stack.task_done()
            continue
        newstates = move_maker(pos, turn)  # for everything else, step forward
        stack.task_done()
        for state in newstates:
            counter -= 1
            stack.put((dist(state[0], end), counter, *state))
    print(besttime)
    return besttime


def main1(data=None):
    board = format_data(data)
    start = np.array([0, 1])
    end = np.array([board.shape[0] - 1, board.shape[1] - 2])
    answer = _solver(start, end)
    print(answer)
    return answer


def main2(data=None):
    board = format_data(data)
    start = np.array([0, 1])
    end = np.array([board.shape[0] - 1, board.shape[1] - 2])
    routes = [(start, end), (end, start), (start, end)]
    answers = []
    besttime = 0
    for start_, end_ in routes:
        besttime = _solver(start_, end_, besttime)
        answers.append(besttime)
    print(answers)
    return answers[-1]


# assert main1(TEST_DATA_A) == TEST_RESULT_A
# resa = main1(puz.input_data)
# print(f"solution: {resa}")
# puz.answer_a = resa

# assert main2(TEST_DATA_A) == TEST_RESULT_B
resb = main2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb
# %%
