# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle

puz = Puzzle(year=2022, day=14)
print(puz.url)

# %%
puz.input_data
# %%
TEST_DATA_A = "498,4 -> 498,6 -> 496,6\n503,4 -> 502,4 -> 502,9 -> 494,9"
TEST_RESULT_A = 24
TEST_DATA_B = None
TEST_RESULT_B = 93


def format_data(data):
    survey = []
    x0, x1 = 500, 500
    y0, y1 = 0, 0
    for line in data.split("\n"):
        path = []
        for loc in line.split(" -> "):
            x, y = list(map(int, loc.split(",")))
            path.append((y, x))
            x0 = min(x0, x)
            x1 = max(x1, x)
            y0 = min(y0, y)
            y1 = max(y1, y)
        survey.append(path)
    return survey, (x0, x1), (y0, y1)


def cartographer(survey, xlims, ylims):
    mapp = np.zeros((ylims[1] + 2, xlims[1] + 500), dtype=bool)  # add abyss-space
    for path in survey:
        for id in range(len(path) - 1):
            ya, yb = list(sorted([path[id][0], path[id + 1][0]]))
            xa, xb = list(sorted([path[id][1], path[id + 1][1])
            for y in range(ya, yb + 1):
                mapp[y, path[id][1]] = True
            for x in range(xa, xb + 1):
                mapp[path[id][0], x] = True
    return mapp


def print_map(mapp, xlims, ylims):
    for row in mapp[ylims[0] :, xlims[0] - 1 :].astype(int):
        print("".join(map(str, row)))


def sand_action(mapp, sandloc):
    actions = [(1, 0), (1, -1), (1, 1)]
    abyss_i = mapp.shape[0] - 1
    can_move = [True] * 3
    done = False
    while any(can_move) and not done:
        for i, (ai, aj) in enumerate(actions):
            if ~mapp[sandloc[0] + ai, sandloc[1] + aj]:
                sandloc = (sandloc[0] + ai, sandloc[1] + aj)
                if sandloc[0] == abyss_i:
                    done = True
                    break
                can_move[i] = True
                break
            else:
                can_move[i] = False
    mapp[sandloc[0], sandloc[1]] = True
    return mapp, done


def main1(data=None):
    survey, xlims, ylims = format_data(data)
    mapp = cartographer(survey, xlims, ylims)
    seedloc = (0, 500)
    count = 0
    done = False
    while not done:
        count += 1
        mapp, done = sand_action(mapp, seedloc)
    return count - 1


def main2(data=None):
    survey, xlims, ylims = format_data(data)
    mapp = cartographer(survey, xlims, ylims)
    seedloc = (0, 500)
    count = 0
    while ~mapp[seedloc]:
        count += 1
        mapp, _ = sand_action(mapp, seedloc)
    return count


assert main1(TEST_DATA_A) == TEST_RESULT_A
resa = main1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa

assert main2(TEST_DATA_A) == TEST_RESULT_B
resb = main2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb
# %%
