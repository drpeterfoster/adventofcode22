# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle

import re
from tqdm import tqdm
from itertools import product
from collections import defaultdict
from scipy.spatial.distance import cdist


puz = Puzzle(year=2022, day=15)
print(puz.url)

# %%
puz.input_data
# %%
TEST_DATA_A = "Sensor at x=2, y=18: closest beacon is at x=-2, y=15\nSensor at x=9, y=16: closest beacon is at x=10, y=16\nSensor at x=13, y=2: closest beacon is at x=15, y=3\nSensor at x=12, y=14: closest beacon is at x=10, y=16\nSensor at x=10, y=20: closest beacon is at x=10, y=16\nSensor at x=14, y=17: closest beacon is at x=10, y=16\nSensor at x=8, y=7: closest beacon is at x=2, y=10\nSensor at x=2, y=0: closest beacon is at x=2, y=10\nSensor at x=0, y=11: closest beacon is at x=2, y=10\nSensor at x=20, y=14: closest beacon is at x=25, y=17\nSensor at x=17, y=20: closest beacon is at x=21, y=22\nSensor at x=16, y=7: closest beacon is at x=15, y=3\nSensor at x=14, y=3: closest beacon is at x=15, y=3\nSensor at x=20, y=1: closest beacon is at x=15, y=3"
TEST_Y = 10
TEST_RESULT_A = 26
TEST_DATA_B = None
TEST_RESULT_B = 56000011


def format_data(data):
    info = pd.DataFrame(
        [list(map(int, re.findall(r"-?\d+", line))) for line in data.split("\n")],
        columns=["sx", "sy", "bx", "by"],
    )
    info["dist"] = info.apply(lambda x: abs(x.sx - x.bx) + abs(x.sy - x.by), axis=1)
    return info


def main1_fullmatrix(data, y):
    """DEPRECATED: I jumped to this solution w/o looking at the input data sizes... oops."""
    info = format_data(data)
    max_dist = info.dist.max()
    mapp = pd.DataFrame(
        list(
            product(
                range(
                    min(info.sx.min(), info.bx.min()) - max_dist,
                    max(info.sx.max(), info.bx.max()) + max_dist,
                ),
                range(
                    min(info.sy.min(), info.by.min()) - max_dist,
                    max(info.sy.max(), info.by.max()) + max_dist,
                ),
            )
        ),
        columns=["x", "y"],
    )
    mapp["occupied"] = False
    dists = []
    for _, row in info.iterrows():
        dist = cdist([[row.sx, row.sy]], mapp.iloc[:, :2], "cityblock")
        dists.append(dist <= row.dist)
        mapp.loc[
            ((mapp.x == row.sx) & (mapp.y == row.sy))
            | ((mapp.x == row.bx) & (mapp.y == row.by)),
            "occupied",
        ] = True
    mapp["covered"] = np.vstack(dists).T.any(axis=1)
    answer = mapp.query(f"y == {y} and not occupied").covered.sum()
    return answer


def main1(data, y):
    info = format_data(data)
    covered_y = scan_line(y, info, True)
    answer = len(covered_y)
    return answer


def scan_line(y, info, clear=True):
    covered_y = set()
    for _, row in info.iterrows():
        yoffset = abs(row.sy - y)
        if row.dist >= yoffset:
            covered_y.update(
                list(
                    range(row.sx - row.dist + yoffset, row.sx + row.dist - yoffset + 1)
                )
            )
    if clear:
        for x in info.query(f"by == {y}").bx.values:
            if x in covered_y:
                covered_y.remove(x)
        for x in info.query(f"sy == {y}").sx.values:
            if x in covered_y:
                covered_y.remove(x)
    return covered_y


def main2_searchall(data, lims):
    """DEPREECATED: yea, kinda thought this would be too slow.  1.2 it/sec x 4e6"""
    info = format_data(data)
    for i in tqdm(range(lims[0], lims[1] + 1)):
        covered = scan_line(i, info, False)
        not_covered = set(range(lims[0], lims[1] + 1)).difference(covered)
        if not_covered:
            x = not_covered.pop()
            y = i
            break
    answer = x * 4_000_000 + y
    return answer


def main2(data, lims):
    info = format_data(data)
    unreached = defaultdict(int)
    for _, row in tqdm(info.iterrows()):
        locs = np.arange(row.dist + 2)
        locs = np.vstack([locs, locs[::-1]]).T
        locs = np.vstack([locs, locs * [[1, -1]], locs * [[-1, 1]], locs * [[-1, -1]]])
        locs += [[row.sx, row.sy]]
        locs = locs[0 : lims[1] + 1, 0 : lims[1] + 1]
        for row in np.unique(locs, axis=0):
            unreached[tuple(row)] += 1
    max_val = max(set(unreached.values()))
    maxes = [k for k, v in unreached.items() if v == max_val]
    fx, fy = 0, 0
    for loc in maxes:
        if (
            cdist([list(loc)], info[["sx", "sy"]], "cityblock") > info.dist.values
        ).all():
            fx, fy = loc
    answer = fx * 4_000_000 + fy
    return answer


assert main1(TEST_DATA_A, TEST_Y) == TEST_RESULT_A
resa = main1(puz.input_data, 2_000_000)
print(f"solution: {resa}")
puz.answer_a = resa

assert main2(TEST_DATA_A, lims=(0, 20)) == TEST_RESULT_B
resb = main2(puz.input_data, lims=(0, 4_000_000))
print(f"solution: {resb}")
puz.answer_b = resb
# %%
