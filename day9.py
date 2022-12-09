# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle

puz = Puzzle(year=2022, day=1)

# %%
# puz.input_data
# %%
TEST_DATA_A = "R 4\nU 4\nL 3\nD 1\nR 4\nD 1\nL 5\nR 2"
TEST_RESULT_A = 13
TEST_DATA_B = "R 5\nU 8\nL 8\nD 3\nR 17\nD 10\nL 25\nU 20"
TEST_RESULT_B = 36


def format_data(data):
    return [(line.split()[0], int(line.split()[1])) for line in data.split('\n')]

def righty(hy, ty):
    if hy>ty:
        return 'RU'
    elif hy<ty:
        return 'RD'
    else:
        return 'R'

def lefty(hy, ty):
    if hy>ty:
        return 'LU'
    elif hy<ty:
        return 'LD'
    else:
        return 'L'

def tail_instructor(H, T):
    hx, hy = H
    tx, ty = T
    if abs(hx-tx)>1 or abs(hy-ty)>1:
        if hx>tx:
            return righty(hy, ty)
        elif hx<tx:
            return lefty(hy, ty)
        elif hx==tx and hy-ty == 2:
            return 'U'
        elif hx==tx and hy-ty == -2:
            return 'D'
        else:
            raise ValueError('oops')
    else:
        return 'NA'

INSTRUCTORS = dict(
    R=lambda pos: (pos[0]+1, pos[1]),
    L=lambda pos: (pos[0]-1, pos[1]),
    U=lambda pos: (pos[0], pos[1]+1),
    D=lambda pos: (pos[0], pos[1]-1),
    RU=lambda pos: (pos[0]+1, pos[1]+1),
    RD=lambda pos: (pos[0]+1, pos[1]-1),
    LU=lambda pos: (pos[0]-1, pos[1]+1),
    LD=lambda pos: (pos[0]-1, pos[1]-1),
    NA=lambda pos: pos,
)

def main1(input_data, n):
    orders = format_data(input_data)
    H, TS = (0,0), [(0,0)] * n  # head + tail chain
    tail_record = [(0,0)]
    for direction, value in orders:
        for _ in range(value):  # step through the moves for each order
            H = INSTRUCTORS[direction](H)  # update head position
            h = H  # initialize the pseudo-head
            for i, t in enumerate(TS):  # step through each tail knot
                tail_direction = tail_instructor(h, t)
                TS[i] = INSTRUCTORS[tail_direction](t)
                h = TS[i]  # tail knot becomes the pseudo-head for the next
            tail_record.append(TS[i])  # the _last_ tail positions are recorded
    return len(set(tail_record))


assert main1(TEST_DATA_A, 1) == TEST_RESULT_A
resa = main1(puz.input_data, 1)
print(f'solution: {resa}')
# puz.answer_a = resa

assert main1(TEST_DATA_B, 9) == TEST_RESULT_B
resb = main1(puz.input_data, 9)
print(f'solution: {resb}')
# puz.answer_b = resb
# %%
