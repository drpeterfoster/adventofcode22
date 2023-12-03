# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle
from itertools import cycle
from tqdm import tqdm

puz = Puzzle(year=2022, day=17)
print(puz.url)

# %%
# puz.input_data
# %%
TEST_DATA_A = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
TEST_RESULT_A = 3068
TEST_DATA_B = None
TEST_RESULT_B = 1514285714288


ROCK1 = np.array([[1, 1, 1, 1]], dtype=int)
ROCK2 = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=int)
ROCK3 = np.array([[0, 0, 1], [0, 0, 1], [1, 1, 1]], dtype=int)
ROCK4 = np.array([[1], [1], [1], [1]], dtype=int)
ROCK5 = np.array([[1, 1], [1, 1]], dtype=int)
EMPTYROW = [1, 0, 0, 0, 0, 0, 0, 0, 1]


def check_valid(board):
    return board.max() == 1


def rockmover(board, rock, ri, rj, jet):
    # Left/Right
    newboard = board.copy()
    newboard[ri[0] : ri[1], rj[0] : rj[1]] -= rock
    match jet:
        case "<":
            rjx = rj - 1
            newboard[ri[0] : ri[1], rjx[0] : rjx[1]] += rock
            if check_valid(newboard):
                board = newboard
                rj = rjx
        case ">":
            rjx = rj + 1
            newboard[ri[0] : ri[1], rjx[0] : rjx[1]] += rock
            if check_valid(newboard):
                board = newboard
                rj = rjx
    # Down
    newboard = board.copy()
    newboard[ri[0] : ri[1], rj[0] : rj[1]] -= rock
    rix = ri + 1
    newboard[rix[0] : rix[1], rj[0] : rj[1]] += rock
    if check_valid(newboard):
        board = newboard
        ri = rix
        landed = False
    else:
        landed = True
    return board, ri, rj, landed


def main1(data=None, nrocks=2022):
    jets = cycle(list(data))
    rocks = cycle([ROCK1, ROCK2, ROCK3, ROCK4, ROCK5])
    towerheight = 0
    board = np.ones((1, 9), dtype=int)
    for _ in tqdm(range(nrocks)):
        rock = next(rocks)
        topindex = np.argwhere(board.sum(axis=1) - 2)[0, 0]
        board = np.vstack(
            [
                np.array([EMPTYROW for _ in range(rock.shape[0] + 3)]),
                board[topindex:, :],
            ]
        )
        ri, rj = np.array((0, rock.shape[0])), np.array((3, 3 + rock.shape[1]))
        board[ri[0] : ri[1], rj[0] : rj[1]] += rock
        landed = False
        while not landed:
            jet = next(jets)
            board, ri, rj, landed = rockmover(board, rock, ri, rj, jet)
        if _ % 100 == 0:
            botindex = (
                max([min(np.argwhere(board[:, i])) for i in range(board.shape[1])])[0]
                + 2
            )
            towerheight += max(0, board.shape[0] - botindex)
            board = board[:botindex, :]
    towertop = np.argwhere(board.sum(axis=1) - 2)[0, 0]
    towerheight = board.shape[0] - towertop + towerheight - 1
    print(towerheight)
    return towerheight


def highest_point(board):
    return board.shape[0] - np.argwhere(board.sum(axis=1) - 2)[0, 0] - 1


def main2(data=None, nrocks=2022):
    jets = cycle(list(enumerate(data)))
    rocks = cycle([(0, ROCK1), (1, ROCK2), (2, ROCK3), (3, ROCK4), (4, ROCK5)])
    towerheight = 0
    board = np.ones((1, 9), dtype=int)

    baserocks = 500
    baseheight = 0
    repeatrocks = len(data) * 5
    nrepeats = (nrocks - 500) // repeatrocks
    nrocks_mod = ((nrocks - 500) % repeatrocks) + 500 + repeatrocks

    rockjettracker = {}

    for i in tqdm(range(nrocks_mod)):
        irock, rock = next(rocks)
        topindex = np.argwhere(board.sum(axis=1) - 2)[0, 0]
        board = np.vstack(
            [
                np.array([EMPTYROW for _ in range(rock.shape[0] + 3)]),
                board[topindex:, :],
            ]
        )
        ri, rj = np.array((0, rock.shape[0])), np.array((3, 3 + rock.shape[1]))
        board[ri[0] : ri[1], rj[0] : rj[1]] += rock
        landed = False
        while not landed:
            ijet, jet = next(jets)
            board, ri, rj, landed = rockmover(board, rock, ri, rj, jet)
            rockjetpair = (irock, ijet)
            if landed:
                if rockjetpair not in rockjettracker:
                    rockjettracker[rockjetpair] = highest_point(board)
                else:
                    

        
        
        # part 2 ish
        if i + 1 == baserocks:
            baseheight = board.shape[0] - np.argwhere(board.sum(axis=1) - 2)[0, 0]
            pass
        if i + 1 == baserocks + repeatrocks:
            repeatheight = (
                board.shape[0] - np.argwhere(board.sum(axis=1) - 2)[0, 0] - baseheight
            )
            pass
    towerheight = board.shape[0] - np.argwhere(board.sum(axis=1) - 2)[0, 0] - 1
    towerheight += repeatheight * nrepeats
    print(towerheight)
    return towerheight


# assert main1(TEST_DATA_A) == TEST_RESULT_A
# resa = main1(puz.input_data, 10000)
# print(f"solution: {resa}")
# puz.answer_a = resa


def test_main2():
    res = main2(TEST_DATA_A, 1_000_000_000_000)
    print("test result:", res)
    print("real result:", TEST_RESULT_B)
    assert res == TEST_RESULT_B


test_main2()
# resb = main2(puz.input_data, 1_000_000_000_000)
# print(f'solution: {resb}')
# puz.answer_b = resb
# %%
