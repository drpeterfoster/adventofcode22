# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle
from copy import deepcopy
from queue import PriorityQueue
from itertools import product

puz = Puzzle(year=2022, day=12)
print(puz.url)

# %%
puz.input_data
# %%
TEST_DATA_A = "Sabqponm\nabcryxxl\naccszExk\nacctuvwj\nabdefghi"
TEST_RESULT_A = 31
TEST_DATA_B = None
TEST_RESULT_B = None

LET2NUM = {chr(x): i for i, x in enumerate(range(97, 123))}
LET2NUM.update({"S": -1, "E": 26})


def format_inputs(data):
    lines = data.split("\n")
    arr = np.zeros((len(lines), len(lines[0])), dtype="int")
    for i, line in enumerate(lines):
        for j, val in enumerate(line):
            arr[i, j] = LET2NUM[val]
            match val:
                case "S":
                    start_pos = (i, j)
                case "E":
                    end_pos = (i, j)
    return arr, start_pos, end_pos


ACTIONS = [(0, -1), (-1, 0), (0, 1), (1, 0)]


def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)


# %%
def main1(data, fstart=None):
    mapp, start, end = format_inputs(data)
    if fstart is not None:
        start = fstart
    n, m = mapp.shape
    g_score = {pos: float("inf") for pos in product(range(n), range(m))}
    f_score = {k: v for k, v in g_score.items()}

    g_score[start] = 0
    f_score[start] = h(start, end)

    open = PriorityQueue()
    open.put((h(start, end), h(start, end), start))
    path = {}
    while not open.empty():
        current = open.get()[2]
        if current == end:
            break
        for action in ACTIONS:
            step = (action[0] + current[0], action[1] + current[1])
            if 0 <= step[0] < n and 0 <= step[1] < m:
                if mapp[step] <= mapp[current] + 1:
                    pass
                else:
                    continue

                temp_g_score = g_score[current] + 1
                temp_f_score = temp_g_score + h(step, end)

                if temp_f_score < f_score[step]:
                    g_score[step] = temp_g_score
                    f_score[step] = temp_f_score
                    open.put((temp_f_score, h(step, end), step))
                    path[step] = current
    fwdpath = {}
    current = end
    while current != start:
        fwdpath[path[current]] = current
        current = path[current]
    return fwdpath, len(fwdpath)


# print(main1(TEST_DATA_A))
assert main1(TEST_DATA_A)[1] == TEST_RESULT_A
path, resa = main1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa - 2  # i think my counting is off somewhere...

# %%
def main2(data):
    return min(main1(data, (i, 0))[1] for i in range(41))


# assert main2(TEST_DATA_B) == TEST_RESULT_B
resb = main2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb - 2  # yea...
# %%
