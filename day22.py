# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle
import re

puz = Puzzle(year=2022, day=22)
print(puz.url)

# %%
puz.input_data
# %%
TEST_DATA_A = "        ...#\n        .#..\n        #...\n        ....\n...#.......#\n........#...\n..#....#....\n..........#.\n        ...#....\n        .....#..\n        .#......\n        ......#.\n\n\n10R5L5R10L4R5L5"
TEST_RESULT_A = 6032
TEST_DATA_B = None
TEST_RESULT_B = None


def format_data(data):
    _mapp, _dirs = data.split("\n\n")
    mapp = [list(line) for line in _mapp.split("\n")]
    width = max([len(line) for line in mapp])
    mapp = [line + [" "] * (width - len(line)) for line in mapp]
    steps = list(map(int, re.findall(r"\d+", _dirs)))
    dirs = re.findall(r"[R,L]", _dirs)
    return mapp, steps, dirs


def answerer(xy, orient):
    return int(1000 * (xy[1] + 1) + 4 * (xy[0] + 1) + orient)


def stepper(xy, orient, step, mapp):
    xy = xy.copy()
    match orient:
        case 0:
            action = np.array([1, 0])
        case 1:
            action = np.array([0, 1])
        case 2:
            action = np.array([-1, 0])
        case 3:
            action = np.array([0, -1])
    lvx, lvy = xy
    while step > 0:
        x, y = xy + action
        if x >= len(mapp[0]):
            x = 0
        if x < 0:
            x = len(mapp[0]) - 1
        if y >= len(mapp):
            y = 0
        if y < 0:
            y = len(mapp) - 1
        look = mapp[y][x]
        match look:
            case " ":
                xy[0], xy[1] = x, y
                continue
            case ".":
                xy[0], xy[1] = lvx, lvy = x, y
                step -= 1
            case "#":
                if mapp[xy[1]][xy[0]] == " ":
                    xy[0], xy[1] = lvx, lvy
                break
    return xy


def main1(data=None):
    mapp, steps, dirs = format_data(data)
    xy, orient = np.zeros((2,), dtype=int), 0
    while len(steps) > 0:
        step = steps.pop(0)
        xy = stepper(xy, orient, step, mapp)
        try:
            rot = dirs.pop(0)
            orient = (orient + 1) % 4 if rot == "R" else (orient - 1) % 4
        except IndexError:
            pass
    answer = answerer(xy, orient)
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
