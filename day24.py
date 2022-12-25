# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle
from queue import PriorityQueue
from collections import defaultdict

puz = Puzzle(year=2022, day=24)
print(puz.url)

# puz.input_data
# %%
TEST_DATA_A = "#.######\n#>>.<^<#\n#.<..<<#\n#>v.><>#\n#<^v^^>#\n######.#"
TEST_RESULT_A = 18
TEST_DATA_B = None
TEST_RESULT_B = None


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
    return mat[1:-1, 1:-1, :]


def roll_board(board):
    board[:, :, 0] = np.roll(board[:, :, 0], 1, axis=1)
    board[:, :, 1] = np.roll(board[:, :, 1], -1, axis=1)
    board[:, :, 2] = np.roll(board[:, :, 2], 1, axis=0)
    board[:, :, 3] = np.roll(board[:, :, 3], -1, axis=0)
    return board


def dist(a, board):
    b = np.array(board.shape[:-1]) - 1
    return int(np.abs(a - b).sum())


def move_maker(pos, board, round, permid):
    board = roll_board(board)
    round += 1
    permid = (permid + 1) % np.product(board.shape[:-1])
    flat = board.sum(axis=2)
    newpos = []
    if tuple(pos) == (-1, -1):
        if flat[0, 0] == 0:
            newpos += [np.array([0, 0])]
        newpos += [np.zeros(2) - 1]
    else:
        rng = np.random.default_rng(round)
        for mod in rng.choice([[0, -1], [-1, 0], [1, 0], [0, 1], [0, 0]], 5, False):
            try:
                opt = pos + mod
                if not np.all(opt >= 0):
                    raise IndexError
                if flat[opt[0], opt[1]] == 0:
                    newpos.append(opt)
            except IndexError:
                continue
    newstates = [
        (pos.copy() if isinstance(pos, np.ndarray) else pos, board.copy(), round)
        for pos in newpos
    ]
    return newstates, permid


def main1(data=None):
    board = format_data(data)
    nperms = np.product(board.shape[:-1])
    end = np.array([board.shape[0] - 1, board.shape[1] - 1])
    besttime = np.inf
    counter = 0
    stack = PriorityQueue()
    stack.put((sum(board.shape[:-1]) + 1, counter, np.zeros(2) - 1, board.copy(), 0, 0))
    looptracker = defaultdict(set)
    while not stack.empty():
        dis, _, pos, board, round, permid = stack.get()
        if (round + dis) >= besttime:
            continue
        if np.all(pos == end) and round < besttime:
            besttime = round
            continue
        newstates, permid = move_maker(pos, board, round, permid)
        for state in newstates:
            counter += 1
            looptracker[tuple(pos)].update([permid])
            if len(looptracker[tuple(pos)]) <= nperms:
                stack.put((dist(state[0], board), counter, *state, permid))
    answer = besttime + 1
    print(answer)
    return answer


def main2(data=None):
    pass


# assert main1(TEST_DATA_A) == TEST_RESULT_A
resa = main1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa

assert main2(TEST_DATA_B) == TEST_RESULT_B
# resb = main2(puz.input_data)
# print(f'solution: {resb}')
# puz.answer_b = resb
# %%
