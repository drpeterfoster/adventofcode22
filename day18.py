# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle

puz = Puzzle(year=2022, day=18)
print(puz.url)

# %%
puz.input_data
# %%
TEST_DATA_A = "2,2,2\n1,2,2\n3,2,2\n2,1,2\n2,3,2\n2,2,1\n2,2,3\n2,2,4\n2,2,6\n1,2,5\n3,2,5\n2,1,5\n2,3,5"
TEST_RESULT_A = 64
TEST_DATA_B = None
TEST_RESULT_B = 58


def format_data(data):
    return [list(map(int, line.split(","))) for line in data.split("\n")]


def make_array(info):
    x, y, z = list(zip(*info))
    arr = np.zeros((max(x) + 3, max(y) + 3, max(z) + 3), dtype=int)
    for x, y, z in info:
        arr[x + 1, y + 1, z + 1] = 1
    return arr


def count_faces(x):
    diffs = np.ediff1d(x)
    return sum(diffs != 0)


def count_all_faces(arr):
    faces = 0
    for i in range(3):
        faces += np.apply_along_axis(count_faces, i, arr).sum()
    return faces


def main1(data=None):
    info = format_data(data)
    arr = make_array(info)
    faces = count_all_faces(arr)
    return faces


def flood_fill(arr, start=(0, 0, 0)):
    arr = arr.copy()
    _x, _y, _z = arr.shape
    stack = [start]
    while len(stack) > 0:
        x, y, z = stack.pop()
        if (0 <= x < _x and 0 <= y < _y and 0 <= z < _z) and arr[x, y, z] == 0:
            arr[x, y, z] = 1
            stack.extend(
                [
                    (x + 1, y, z),
                    (x - 1, y, z),
                    (x, y + 1, z),
                    (x, y - 1, z),
                    (x, y, z + 1),
                    (x, y, z - 1),
                ]
            )
    return arr


def main2(data=None):
    info = format_data(data)
    arr = make_array(info)
    faces = count_all_faces(arr)
    arr_filled = flood_fill(arr)
    faces_filled = count_all_faces(arr_filled)
    answer = faces - faces_filled
    return int(answer)


assert main1(TEST_DATA_A) == TEST_RESULT_A
resa = main1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa

assert main2(TEST_DATA_A) == TEST_RESULT_B
resb = main2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb
# %%
