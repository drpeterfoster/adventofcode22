# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle
from itertools import cycle

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
ROCKS = cycle([ROCK1, ROCK2, ROCK3, ROCK4, ROCK5])
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
    towerheight = 0
    board = np.ones((1, 9), dtype=int)
    for _ in range(nrocks):
        rock = next(ROCKS)
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


def main2(data=None):
    pass


assert main1(TEST_DATA_A) == TEST_RESULT_A
resa = main1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa

# assert main2(TEST_DATA_A, 1_000_000_000_000) == TEST_RESULT_B
# resb = main2(puz.input_data, 1_000_000_000_000)
# print(f'solution: {resb}')
# puz.answer_b = resb
# %%
