# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle

puz = Puzzle(year=2022, day=10)
print(puz.url)
# %%
puz.input_data
# %%

TEST_DATA_A = "addx 15\naddx -11\naddx 6\naddx -3\naddx 5\naddx -1\naddx -8\naddx 13\naddx 4\nnoop\naddx -1\naddx 5\naddx -1\naddx 5\naddx -1\naddx 5\naddx -1\naddx 5\naddx -1\naddx -35\naddx 1\naddx 24\naddx -19\naddx 1\naddx 16\naddx -11\nnoop\nnoop\naddx 21\naddx -15\nnoop\nnoop\naddx -3\naddx 9\naddx 1\naddx -3\naddx 8\naddx 1\naddx 5\nnoop\nnoop\nnoop\nnoop\nnoop\naddx -36\nnoop\naddx 1\naddx 7\nnoop\nnoop\nnoop\naddx 2\naddx 6\nnoop\nnoop\nnoop\nnoop\nnoop\naddx 1\nnoop\nnoop\naddx 7\naddx 1\nnoop\naddx -13\naddx 13\naddx 7\nnoop\naddx 1\naddx -33\nnoop\nnoop\nnoop\naddx 2\nnoop\nnoop\nnoop\naddx 8\nnoop\naddx -1\naddx 2\naddx 1\nnoop\naddx 17\naddx -9\naddx 1\naddx 1\naddx -3\naddx 11\nnoop\nnoop\naddx 1\nnoop\naddx 1\nnoop\nnoop\naddx -13\naddx -19\naddx 1\naddx 3\naddx 26\naddx -30\naddx 12\naddx -1\naddx 3\naddx 1\nnoop\nnoop\nnoop\naddx -9\naddx 18\naddx 1\naddx 2\nnoop\nnoop\naddx 9\nnoop\nnoop\nnoop\naddx -1\naddx 2\naddx -37\naddx 1\naddx 3\nnoop\naddx 15\naddx -21\naddx 22\naddx -6\naddx 1\nnoop\naddx 2\naddx 1\nnoop\naddx -10\nnoop\nnoop\naddx 20\naddx 1\naddx 2\naddx 2\naddx -6\naddx -11\nnoop\nnoop\nnoop"
TEST_RESULT_A = 13140
# TEST_DATA_B = None
TEST_RESULT_B = [
    "##..##..##..##..##..##..##..##..##..##..",
    "###...###...###...###...###...###...###.",
    "####....####....####....####....####....",
    "#####.....#####.....#####.....#####.....",
    "######......######......######......####",
    "#######.......#######.......#######.....",
]

TARGET_CYCLES = [20, 60, 100, 140, 180, 220]


def main1(data=None):
    output = decode_orders(data)
    result = sum([x * y for x, y in output if x in TARGET_CYCLES])
    return result


def decode_orders(data):
    X = 1
    c = 1
    program = data.split('\n')
    output = [(c, X)]
    while len(program) != 0:
        c += 1
        match program.pop(0).split():
            case ['noop']:
                output.append((c, X))
            case ['addx', v]:
                output.append((c, X))
                c += 1
                X += int(v)
                output.append((c, X))
    return output


def main2(data=None, show=True):
    orders = decode_orders(data)
    msg = ['#' if X-2 < ((c-1)%40) < X+2 else '.' for c, X in orders]
    result = np.array(msg[:-1]).reshape((6, 40))
    result = [''.join(x) for x in result]
    if show:
        for row in result:
            print(row)
    return result


assert main1(TEST_DATA_A) == TEST_RESULT_A
resa = main1(puz.input_data)
print(f'solution: {resa}')
puz.answer_a = resa

assert main2(TEST_DATA_A) == TEST_RESULT_B
print()
main2(puz.input_data)
resb = 'BACEKLHF'
print(f'solution: {resb}')
puz.answer_b = resb
# %%
