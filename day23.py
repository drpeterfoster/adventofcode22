# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle
from itertools import cycle
from collections import defaultdict

puz = Puzzle(year=2022, day=23)
# print(puz.url)

# puz.input_data
# %%
TEST_DATA_A = "....#..\n..###.#\n#...#.#\n.#...##\n#.###..\n##.#.##\n.#..#.."
FIRST_REC = ".....#...\n...#...#.\n.#..#.#..\n.....#..#\n..#.#.##.\n#..#.#...\n#.#.#.##.\n.........\n..#..#..."
FINAL_REC = "......#.....\n..........#.\n.#.#..#.....\n.....#......\n..#.....#..#\n#......##...\n....##......\n.#........#.\n...#.#..#...\n............\n...#..#..#.."
TEST_RESULT_A = 110
TEST_DATA_B = None
TEST_RESULT_B = 20


def format_data(data):
    lines = [[0 if x == "." else 1 for x in line] for line in data.split("\n")]
    arr = np.array(lines)[:, :, np.newaxis]
    arr = np.concatenate([arr, np.zeros((arr.shape[0], arr.shape[1], 2))], axis=2)
    return arr.astype(int)


def expand_board(arr):
    if arr[0, :, 0].sum() > 0:
        arr = np.concatenate([np.zeros((1, arr.shape[1], 3)), arr], axis=0)
    if arr[-1, :, 0].sum() > 0:
        arr = np.concatenate([arr, np.zeros((1, arr.shape[1], 3))], axis=0)
    if arr[:, 0, 0].sum() > 0:
        arr = np.concatenate([np.zeros((arr.shape[0], 1, 3)), arr], axis=1)
    if arr[:, -1, 0].sum() > 0:
        arr = np.concatenate([arr, np.zeros((arr.shape[0], 1, 3))], axis=1)
    return arr.astype(int)


def scanner(arr, i, j, scandir):
    match scandir:
        case "N":
            if arr[i - 1, j - 1 : j + 2].sum() > 0:
                return False, i, j
            else:
                return True, i - 1, j
        case "S":
            if arr[i + 1, j - 1 : j + 2].sum() > 0:
                return False, i, j
            else:
                return True, i + 1, j
        case "W":
            if arr[i - 1 : i + 2, j - 1].sum() > 0:
                return False, i, j
            else:
                return True, i, j - 1
        case "E":
            if arr[i - 1 : i + 2, j + 1].sum() > 0:
                return False, i, j
            else:
                return True, i, j + 1


def chooser(arr, start_dir):
    nomove = 0
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if arr[i, j, 0] == 1:
                elf_dirs = cycle("NSWE")
                scandir = next(elf_dirs)
                while scandir != start_dir:
                    scandir = next(elf_dirs)
                cango = []
                for _ in range(4):
                    scanresult = scanner(arr, i, j, scandir)
                    cango.append(scanresult)
                    scandir = next(elf_dirs)
                if all([x[0] for x in cango]) or not any([x[0] for x in cango]):
                    arr[i, j, 1:] = [i, j]
                    nomove += 1
                else:
                    arr[i, j, 1:] = [[x[1], x[2]] for x in cango if x[0]][0]
            else:
                arr[i, j, 1:] = [0, 0]
    stable = nomove == arr[:, :, 0].sum()
    return arr, stable


def colocafinder(arr):
    counts = defaultdict(int)
    locs = arr.reshape((arr.shape[0] * arr.shape[1], 3))[:, 1:]
    for coord in locs:
        counts[tuple(coord)] += 1
    counts.pop((0, 0))
    return [coord for coord, count in counts.items() if count > 1]


def move_negator(arr, colocs):
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if tuple(arr[i, j, 1:]) in colocs:
                arr[i, j, 1:] = [i, j]
    return arr


def elf_stepper(arr):
    newarr = np.zeros(arr.shape, dtype=int)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            val, ni, nj = arr[i, j, :]
            if bool(val):
                newarr[ni, nj, 0] = 1
    return newarr


def shrinker(arr):
    while arr[:, 0, 0].sum() == 0:
        arr = arr[:, 1:, :]
    while arr[:, -1, 0].sum() == 0:
        arr = arr[:, :-1, :]
    while arr[0, :, 0].sum() == 0:
        arr = arr[1:, :, :]
    while arr[-1, :, 0].sum() == 0:
        arr = arr[:-1, :, :]
    return arr


def answerer(arr):
    return arr.shape[0] * arr.shape[1] - arr[:, :, 0].sum()


def elf_diffuser(arr, scan_start_dirs):
    arr = expand_board(arr)
    scan_dir = next(scan_start_dirs)
    arr, stable = chooser(arr, scan_dir)
    colocs = colocafinder(arr)
    arr = move_negator(arr, colocs)
    arr = elf_stepper(arr)
    return arr, stable


def main1(data=None, rounds=10, tillstable=False):
    arr = format_data(data)
    scan_start_dirs = cycle("NSWE")
    if tillstable:
        stable = False
        r = 0
        while not stable:
            r += 1
            arr, stable = elf_diffuser(arr, scan_start_dirs)
    else:
        for r in range(rounds):
            arr, stable = elf_diffuser(arr, scan_start_dirs)
    arr = shrinker(arr)
    answer = answerer(arr)
    print(answer, r)
    return answer, arr, r


def test_main1(data=TEST_DATA_A):
    answer, board, _ = main1(data)
    expected_board = format_data(FINAL_REC)
    assert answer == TEST_RESULT_A
    assert np.all(board[:, :, 0] == expected_board[:, :, 0])


def main2(data=None):
    pass


test_main1()
resa, _, _ = main1(puz.input_data, tillstable=False)
print(f"solution: {resa}")
puz.answer_a = resa

assert main1(TEST_DATA_A, tillstable=True)[2] == TEST_RESULT_B
_, _, resb = main1(puz.input_data, tillstable=True)
print(f"solution: {resb}")
puz.answer_b = resb
# %%
